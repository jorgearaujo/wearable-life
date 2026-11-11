package dev.wearablelife.hc_bridge

import android.content.Context
import android.os.Process
import android.os.SystemClock
import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.permission.HealthPermission
import androidx.health.connect.client.records.HeartRateVariabilityRmssdRecord
import androidx.health.connect.client.records.Record
import androidx.health.connect.client.records.SleepSessionRecord
import androidx.health.connect.client.records.StepsRecord
import androidx.health.connect.client.records.metadata.DataOrigin
import androidx.health.connect.client.request.AggregateRequest
import androidx.health.connect.client.request.ReadRecordsRequest
import androidx.health.connect.client.time.TimeRangeFilter
import java.io.File
import java.time.Duration
import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId
import kotlin.reflect.KClass
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

/**
 * The one place that reads Health Connect. Called by the background worker and, over the platform
 * channel, by the Flutter screen. Each read appends one line to a file in app-private storage.
 *
 * Spike only: the line holds record counts and the time of the read. No health values are stored,
 * and nothing is written to logcat. The step comparison returns ratios only and stores nothing.
 */
object HealthReader {
    private const val STORE = "reads.jsonl"

    private val types: List<Pair<String, KClass<out Record>>> = listOf(
        "steps" to StepsRecord::class,
        "sleep" to SleepSessionRecord::class,
        "hrv" to HeartRateVariabilityRmssdRecord::class,
    )

    /** True while a Flutter engine is attached to the activity. Lets a read say who was running. */
    @Volatile
    var flutterAttached = false

    // The worker and the screen share one process, so one lock is enough to keep reads apart.
    private val mutex = Mutex()

    val permissions: Set<String> =
        types.map { HealthPermission.getReadPermission(it.second) }.toSet() +
            HealthPermission.PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND

    suspend fun read(context: Context, trigger: String): String = mutex.withLock {
        withContext(Dispatchers.IO) {
            val app = context.applicationContext
            val startedAt = Instant.now()
            val line = JSONObject()
                .put("at", startedAt.toString())
                .put("trigger", trigger)
                .put("flutterAttached", flutterAttached)
                .put("processAgeS", (SystemClock.elapsedRealtime() - Process.getStartElapsedRealtime()) / 1000)
            try {
                val client = HealthConnectClient.getOrCreate(app)
                val lastDay = TimeRangeFilter.between(startedAt.minus(Duration.ofHours(24)), startedAt)
                for ((name, type) in types) {
                    line.put(name, count(client, type, lastDay))
                }
            } catch (e: Exception) {
                line.put("error", e.javaClass.simpleName)
            }
            line.put("durationMs", Duration.between(startedAt, Instant.now()).toMillis())
            File(app.filesDir, STORE).appendText(line.toString() + "\n")
            line.toString()
        }
    }

    /** Every stored read, oldest first, one JSON object per entry. */
    suspend fun history(context: Context): List<String> = mutex.withLock {
        withContext(Dispatchers.IO) {
            val file = File(context.applicationContext.filesDir, STORE)
            if (file.exists()) file.readLines().filter { it.isNotBlank() } else emptyList()
        }
    }

    /**
     * For each of the last 7 local days: Health Connect's own step total next to each source's
     * total. Only ratios and record counts leave this function; no step count is returned, stored
     * or logged. Nothing is written to disk.
     */
    suspend fun compareSteps(context: Context): List<String> = mutex.withLock {
        withContext(Dispatchers.IO) {
            val client = HealthConnectClient.getOrCreate(context.applicationContext)
            val zone = ZoneId.systemDefault()
            val now = Instant.now()
            val today = LocalDate.now(zone)
            (0L..6L).map { back ->
                val day = today.minusDays(back)
                val start = day.atStartOfDay(zone).toInstant()
                val end = minOf(day.plusDays(1).atStartOfDay(zone).toInstant(), now)
                val range = TimeRangeFilter.between(start, end)
                val line = JSONObject().put("day", day.toString())
                try {
                    val total = stepTotal(client, range, emptySet())
                    // Raw records per source: how many, and what they add up to without any merging.
                    val records = HashMap<String, Int>()
                    val rawSum = HashMap<String, Long>()
                    var pageToken: String? = null
                    do {
                        val page = client.readRecords(
                            ReadRecordsRequest(StepsRecord::class, range, pageSize = 5000, pageToken = pageToken)
                        )
                        for (r in page.records) {
                            val origin = r.metadata.dataOrigin.packageName
                            records[origin] = (records[origin] ?: 0) + 1
                            rawSum[origin] = (rawSum[origin] ?: 0L) + r.count
                        }
                        pageToken = page.pageToken
                    } while (pageToken != null)

                    val sources = JSONArray()
                    var sumOfSources = 0L
                    var largest = 0L
                    for (origin in records.keys.sorted()) {
                        val own = stepTotal(client, range, setOf(DataOrigin(origin)))
                        sumOfSources += own
                        largest = maxOf(largest, own)
                        sources.put(
                            JSONObject()
                                .put("name", label(origin))
                                .put("records", records[origin])
                                .put("shareOfTotal", ratio(own, total))
                                .put("rawOverOwn", ratio(rawSum[origin] ?: 0L, own))
                                .put("equalsTotal", total > 0 && own == total)
                        )
                    }
                    line.put("hasSteps", total > 0)
                        .put("sources", sources)
                        .put("sumOverTotal", ratio(sumOfSources, total))
                        .put("largestOverTotal", ratio(largest, total))
                } catch (e: Exception) {
                    line.put("error", e.javaClass.simpleName)
                }
                line.toString()
            }
        }
    }

    private suspend fun stepTotal(client: HealthConnectClient, range: TimeRangeFilter, origins: Set<DataOrigin>): Long =
        client.aggregate(AggregateRequest(setOf(StepsRecord.COUNT_TOTAL), range, origins))[StepsRecord.COUNT_TOTAL] ?: 0L

    private fun ratio(part: Long, whole: Long): Any =
        if (whole > 0) Math.round(part * 100.0 / whole) / 100.0 else JSONObject.NULL

    /** The phone's own counter carries a per-device name; show it as "phone". */
    private fun label(origin: String): String =
        if (origin == "android" || origin.startsWith("com.android.healthconnect.phone")) "phone" else origin

    private suspend fun count(client: HealthConnectClient, type: KClass<out Record>, range: TimeRangeFilter): Int {
        var total = 0
        var pageToken: String? = null
        do {
            val page = client.readRecords(ReadRecordsRequest(type, range, pageSize = 1000, pageToken = pageToken))
            total += page.records.size
            pageToken = page.pageToken
        } while (pageToken != null)
        return total
    }
}
