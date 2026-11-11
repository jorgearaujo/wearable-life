package dev.wearablelife.hcseeder

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.records.ActiveCaloriesBurnedRecord
import androidx.health.connect.client.records.BodyTemperatureRecord
import androidx.health.connect.client.records.DistanceRecord
import androidx.health.connect.client.records.ExerciseSessionRecord
import androidx.health.connect.client.records.HeartRateRecord
import androidx.health.connect.client.records.HeartRateVariabilityRmssdRecord
import androidx.health.connect.client.records.MindfulnessSessionRecord
import androidx.health.connect.client.records.OxygenSaturationRecord
import androidx.health.connect.client.records.RespiratoryRateRecord
import androidx.health.connect.client.records.RestingHeartRateRecord
import androidx.health.connect.client.records.SkinTemperatureRecord
import androidx.health.connect.client.records.SleepSessionRecord
import androidx.health.connect.client.records.StepsRecord
import androidx.health.connect.client.records.TotalCaloriesBurnedRecord
import androidx.health.connect.client.records.metadata.Device
import androidx.health.connect.client.records.metadata.Metadata
import androidx.health.connect.client.units.Energy
import androidx.health.connect.client.units.Length
import androidx.health.connect.client.units.Percentage
import androidx.health.connect.client.units.Temperature
import androidx.health.connect.client.units.TemperatureDelta
import androidx.lifecycle.lifecycleScope
import java.time.Duration
import java.time.Instant
import java.time.ZoneOffset
import kotlinx.coroutines.launch

/**
 * Writes synthetic records. Driven from adb:
 *   adb shell am start -n dev.wearablelife.hcseeder/.SeedActivity --es action insert|update|delete
 *   ... --es action steps --el count 100 --el shift 0   (three 10-minute step records)
 * insert: one record of every type. update: rewrites the steps record. delete: removes the sleep session.
 */
class SeedActivity : ComponentActivity() {
    private val watch = Device(type = Device.TYPE_WATCH, manufacturer = "Synthetic", model = "Seeder")
    private val utc = ZoneOffset.UTC

    private fun meta(clientId: String, version: Long = 1) = Metadata.autoRecorded(watch, clientId, version)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val action = intent.getStringExtra("action") ?: "insert"
        val client = HealthConnectClient.getOrCreate(this)
        lifecycleScope.launch {
            try {
                when (action) {
                    "insert" -> insertAll(client)
                    "update" -> client.insertRecords(listOf(steps(4321, version = 2)))
                    "delete" -> client.deleteRecords(SleepSessionRecord::class, emptyList(), listOf("seed-sleep"))
                    // Three 10-minute step records; "shift" moves them, so two copies of this app
                    // (see -PseederId) can write partly overlapping steps as two sources.
                    "steps" -> {
                        val count = intent.getLongExtra("count", 100)
                        val shift = intent.getLongExtra("shift", 0)
                        client.insertRecords(
                            listOf(90L, 80L, 30L).map { start ->
                                StepsRecord(
                                    ago(start + shift), utc, ago(start + shift - 10), utc, count,
                                    meta("seed-steps-$start-${now.epochSecond}"),
                                )
                            },
                        )
                    }
                }
                Log.i("HcSeeder", "$action ok")
            } catch (e: Exception) {
                Log.e("HcSeeder", "$action failed", e)
            }
            finish()
        }
    }

    private val now: Instant = Instant.now()
    private fun ago(minutes: Long): Instant = now.minus(Duration.ofMinutes(minutes))

    private fun steps(count: Long, version: Long) =
        StepsRecord(ago(120), utc, ago(60), utc, count, meta("seed-steps", version))

    private suspend fun insertAll(client: HealthConnectClient) {
        val sleepStart = ago(600)
        val sleepEnd = ago(180)
        client.insertRecords(
            listOf(
                steps(1234, version = 1),
                SleepSessionRecord(
                    startTime = sleepStart, startZoneOffset = utc, endTime = sleepEnd, endZoneOffset = utc,
                    metadata = meta("seed-sleep"),
                    stages = listOf(
                        SleepSessionRecord.Stage(sleepStart, sleepStart.plusSeconds(7200), SleepSessionRecord.STAGE_TYPE_LIGHT),
                        SleepSessionRecord.Stage(sleepStart.plusSeconds(7200), sleepStart.plusSeconds(12600), SleepSessionRecord.STAGE_TYPE_DEEP),
                        SleepSessionRecord.Stage(sleepStart.plusSeconds(12600), sleepEnd, SleepSessionRecord.STAGE_TYPE_REM),
                    ),
                ),
                HeartRateRecord(
                    ago(60), utc, ago(50), utc,
                    (0L..9L).map { HeartRateRecord.Sample(ago(60 - it), 60 + it) },
                    meta("seed-hr"),
                ),
                RestingHeartRateRecord(sleepEnd, utc, 52, meta("seed-rhr")),
                HeartRateVariabilityRmssdRecord(sleepEnd, utc, 48.5, meta("seed-hrv")),
                RespiratoryRateRecord(sleepEnd, utc, 14.2, meta("seed-rr")),
                OxygenSaturationRecord(sleepEnd, utc, Percentage(96.0), meta("seed-spo2")),
                SkinTemperatureRecord(
                    startTime = sleepStart, startZoneOffset = utc, endTime = sleepEnd, endZoneOffset = utc,
                    metadata = meta("seed-skin"),
                    deltas = listOf(SkinTemperatureRecord.Delta(sleepStart.plusSeconds(3600), TemperatureDelta.celsius(0.3))),
                    baseline = Temperature.celsius(33.1),
                ),
                BodyTemperatureRecord(sleepEnd, utc, meta("seed-body"), Temperature.celsius(36.6)),
                ExerciseSessionRecord(
                    startTime = ago(170), startZoneOffset = utc, endTime = ago(130), endZoneOffset = utc,
                    metadata = meta("seed-exercise"),
                    exerciseType = ExerciseSessionRecord.EXERCISE_TYPE_RUNNING,
                ),
                ActiveCaloriesBurnedRecord(ago(170), utc, ago(130), utc, Energy.kilocalories(310.0), meta("seed-active")),
                TotalCaloriesBurnedRecord(ago(170), utc, ago(130), utc, Energy.kilocalories(360.0), meta("seed-total")),
                DistanceRecord(ago(170), utc, ago(130), utc, Length.meters(6200.0), meta("seed-distance")),
                MindfulnessSessionRecord(
                    startTime = ago(40), startZoneOffset = utc, endTime = ago(30), endZoneOffset = utc,
                    metadata = meta("seed-mindful"),
                    mindfulnessSessionType = MindfulnessSessionRecord.MINDFULNESS_SESSION_TYPE_BREATHING,
                ),
            ),
        )
    }
}
