package dev.wearablelife.hclogger

import android.app.AlarmManager
import android.content.Context
import android.os.Build
import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.HealthConnectFeatures
import androidx.health.connect.client.changes.DeletionChange
import androidx.health.connect.client.changes.UpsertionChange
import androidx.health.connect.client.permission.HealthPermission
import androidx.health.connect.client.records.Record
import androidx.health.connect.client.request.ChangesTokenRequest
import androidx.health.connect.client.request.ReadRecordsRequest
import androidx.health.connect.client.time.TimeRangeFilter
import java.io.BufferedWriter
import java.io.File
import java.io.FileOutputStream
import java.time.Duration
import java.time.Instant
import java.time.ZoneId
import java.util.UUID
import kotlin.reflect.KClass
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

/**
 * Reads whatever is new in Health Connect and appends it to two JSONL files in app-private storage.
 *
 * - observations.jsonl: one line per record seen (or deleted), with the time the logger first saw it.
 * - runs.jsonl: one line per poll, including polls that found nothing or failed.
 *
 * Health values are written only to these files. They are never sent to logcat or anywhere else.
 */
object Poller {
    const val OBSERVATIONS_FILE = "observations.jsonl"
    const val RUNS_FILE = "runs.jsonl"
    const val PREFS = "poller"
    const val PREF_LAST_RUN = "lastRun"

    private const val BACKFILL_DAYS = 90L
    private const val PAGE_SIZE = 500
    private val mutex = Mutex()

    fun readPermissions(features: HealthConnectFeatures): Set<String> {
        val permissions = LOGGED_TYPES
            .filter { it.feature == null || features.isAvailable(it.feature) }
            .map { HealthPermission.getReadPermission(it.kClass) }
            .toMutableSet()
        if (features.isAvailable(HealthConnectFeatures.FEATURE_READ_HEALTH_DATA_IN_BACKGROUND)) {
            permissions += HealthPermission.PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND
        }
        if (features.isAvailable(HealthConnectFeatures.FEATURE_READ_HEALTH_DATA_HISTORY)) {
            permissions += HealthPermission.PERMISSION_READ_HEALTH_DATA_HISTORY
        }
        return permissions
    }

    /** Runs one poll and returns its summary (the same object written to runs.jsonl). */
    suspend fun poll(context: Context, trigger: String): JSONObject = mutex.withLock {
        withContext(Dispatchers.IO) {
            val app = context.applicationContext
            val startedAt = Instant.now()
            val run = JSONObject()
                .put("runId", UUID.randomUUID().toString().take(8))
                .put("at", startedAt.toString())
                .put("zone", ZoneId.systemDefault().id)
                .put("trigger", trigger)
                .put("phone", JSONObject().put("manufacturer", Build.MANUFACTURER).put("model", Build.MODEL).put("sdk", Build.VERSION.SDK_INT))
                .put("nextAlarm", nextAlarm(app)?.toString() ?: JSONObject.NULL)

            val sdkStatus = HealthConnectClient.getSdkStatus(app)
            run.put("sdkStatus", sdkStatus)
            if (sdkStatus == HealthConnectClient.SDK_AVAILABLE) {
                try {
                    pollTypes(app, run, trigger)
                } catch (e: Exception) {
                    run.put("error", describe(e))
                }
            }

            run.put("durationMs", Duration.between(startedAt, Instant.now()).toMillis())
            File(app.filesDir, RUNS_FILE).appendText(run.toString() + "\n")
            app.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(PREF_LAST_RUN, run.toString()).apply()
            run
        }
    }

    private suspend fun pollTypes(app: Context, run: JSONObject, trigger: String) {
        val client = HealthConnectClient.getOrCreate(app)
        val prefs = app.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val granted = client.permissionController.getGrantedPermissions()
        run.put("granted", JSONArray(granted.map { it.substringAfterLast('.') }.sorted()))
        run.put("features", JSONObject(LOGGED_FEATURES.mapValues { client.features.isAvailable(it.value) }))

        val types = JSONObject()
        run.put("types", types)
        val runId = run.getString("runId")

        BufferedWriter(FileOutputStream(File(app.filesDir, OBSERVATIONS_FILE), true).writer()).use { out ->
            for (type in LOGGED_TYPES) {
                val summary = JSONObject()
                types.put(type.name, summary)
                if (type.feature != null && !client.features.isAvailable(type.feature)) {
                    summary.put("skipped", "featureUnavailable")
                    continue
                }
                if (HealthPermission.getReadPermission(type.kClass) !in granted) {
                    summary.put("skipped", "noPermission")
                    continue
                }
                try {
                    val sink = Sink(out, runId, trigger, type.name)
                    pollType(client, prefs, type, sink, summary)
                    summary.put("upserts", sink.upserts).put("deletes", sink.deletes)
                    val totalKey = "total.${type.name}"
                    prefs.edit().putLong(totalKey, prefs.getLong(totalKey, 0) + sink.upserts).apply()
                } catch (e: Exception) {
                    summary.put("error", describe(e))
                }
                out.flush()
            }
        }
    }

    private suspend fun pollType(
        client: HealthConnectClient,
        prefs: android.content.SharedPreferences,
        type: LoggedType,
        sink: Sink,
        summary: JSONObject,
    ) {
        val tokenKey = "token.${type.name}"
        val lastOkKey = "lastOk.${type.name}"
        val pollStart = Instant.now()
        var token = prefs.getString(tokenKey, null)

        if (token == null) {
            // First poll for this type: take the token first so nothing written during the backfill is missed.
            token = client.getChangesToken(ChangesTokenRequest(setOf(type.kClass)))
            summary.put("mode", "backfill")
            backfill(client, type.kClass, pollStart.minus(Duration.ofDays(BACKFILL_DAYS)), sink)
        } else {
            summary.put("mode", "changes")
            var hasMore = true
            while (hasMore) {
                val response = client.getChanges(token!!)
                if (response.changesTokenExpired) {
                    // Tokens expire after about 30 days without use. Re-read from the last good poll.
                    summary.put("mode", "tokenExpiredBackfill")
                    token = client.getChangesToken(ChangesTokenRequest(setOf(type.kClass)))
                    val since = Instant.ofEpochMilli(prefs.getLong(lastOkKey, pollStart.toEpochMilli())).minus(Duration.ofDays(1))
                    backfill(client, type.kClass, since, sink)
                    break
                }
                for (change in response.changes) {
                    when (change) {
                        is UpsertionChange -> sink.upsert(change.record, "change")
                        is DeletionChange -> sink.delete(change.recordId)
                    }
                }
                token = response.nextChangesToken
                hasMore = response.hasMore
            }
        }
        prefs.edit().putString(tokenKey, token).putLong(lastOkKey, pollStart.toEpochMilli()).apply()
    }

    @Suppress("UNCHECKED_CAST")
    private suspend fun backfill(client: HealthConnectClient, kClass: KClass<out Record>, since: Instant, sink: Sink) {
        var pageToken: String? = null
        do {
            val response = client.readRecords(
                ReadRecordsRequest(
                    recordType = kClass as KClass<Record>,
                    timeRangeFilter = TimeRangeFilter.after(since),
                    pageSize = PAGE_SIZE,
                    pageToken = pageToken,
                ),
            )
            response.records.forEach { sink.upsert(it, "backfill") }
            pageToken = response.pageToken
        } while (pageToken != null)
    }

    private class Sink(val out: BufferedWriter, val runId: String, val trigger: String, val type: String) {
        var upserts = 0
        var deletes = 0

        fun upsert(record: Record, via: String) {
            line(via, "upsert").put("meta", metadataJson(record)).put("data", dataJson(record)).write()
            upserts++
        }

        fun delete(recordId: String) {
            line("change", "delete").put("id", recordId).write()
            deletes++
        }

        private fun line(via: String, op: String) = JSONObject()
            .put("seenAt", Instant.now().toString())
            .put("runId", runId)
            .put("trigger", trigger)
            .put("via", via)
            .put("op", op)
            .put("type", type)

        private fun JSONObject.write() {
            out.write(toString())
            out.newLine()
        }
    }

    private fun nextAlarm(context: Context): Instant? =
        context.getSystemService(AlarmManager::class.java)?.nextAlarmClock?.let { Instant.ofEpochMilli(it.triggerTime) }

    /** Exception class and message only. Health Connect error messages do not contain record values. */
    private fun describe(e: Exception): String = "${e::class.simpleName}: ${e.message?.take(300)}"
}

fun HealthConnectFeatures.isAvailable(feature: Int): Boolean =
    getFeatureStatus(feature) == HealthConnectFeatures.FEATURE_STATUS_AVAILABLE
