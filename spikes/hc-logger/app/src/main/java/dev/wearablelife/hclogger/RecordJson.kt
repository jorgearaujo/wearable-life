package dev.wearablelife.hclogger

import androidx.health.connect.client.records.ActiveCaloriesBurnedRecord
import androidx.health.connect.client.records.BodyTemperatureRecord
import androidx.health.connect.client.records.DistanceRecord
import androidx.health.connect.client.records.ExerciseSessionRecord
import androidx.health.connect.client.records.HeartRateRecord
import androidx.health.connect.client.records.HeartRateVariabilityRmssdRecord
import androidx.health.connect.client.records.MindfulnessSessionRecord
import androidx.health.connect.client.records.OxygenSaturationRecord
import androidx.health.connect.client.records.Record
import androidx.health.connect.client.records.RespiratoryRateRecord
import androidx.health.connect.client.records.RestingHeartRateRecord
import androidx.health.connect.client.records.SkinTemperatureRecord
import androidx.health.connect.client.records.SleepSessionRecord
import androidx.health.connect.client.records.StepsRecord
import androidx.health.connect.client.records.TotalCaloriesBurnedRecord
import java.time.Instant
import java.time.ZoneOffset
import org.json.JSONArray
import org.json.JSONObject

/** Metadata common to every record: who wrote it, when it was last changed, and how it was recorded. */
fun metadataJson(record: Record): JSONObject {
    val m = record.metadata
    val json = JSONObject()
        .put("id", m.id)
        .put("origin", m.dataOrigin.packageName)
        .put("lastModified", m.lastModifiedTime.toString())
        .put("recordingMethod", m.recordingMethod)
        .put("clientRecordId", m.clientRecordId ?: JSONObject.NULL)
        .put("clientRecordVersion", m.clientRecordVersion)
    m.device?.let { d ->
        json.put(
            "device",
            JSONObject()
                .put("type", d.type)
                .put("manufacturer", d.manufacturer ?: JSONObject.NULL)
                .put("model", d.model ?: JSONObject.NULL),
        )
    }
    return json
}

/** The record's own times and values. Sample series are written as compact [time, value] pairs. */
fun dataJson(record: Record): JSONObject = when (record) {
    is StepsRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("count", record.count)

    is SleepSessionRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put(
                "stages",
                JSONArray(record.stages.map { JSONArray(listOf(it.startTime.toString(), it.endTime.toString(), it.stage)) }),
            )

    is HeartRateRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("samples", JSONArray(record.samples.map { JSONArray(listOf(it.time.toString(), it.beatsPerMinute)) }))

    is RestingHeartRateRecord ->
        instant(record.time, record.zoneOffset).put("bpm", record.beatsPerMinute)

    is HeartRateVariabilityRmssdRecord ->
        instant(record.time, record.zoneOffset).put("rmssdMillis", record.heartRateVariabilityMillis)

    is RespiratoryRateRecord ->
        instant(record.time, record.zoneOffset).put("breathsPerMinute", record.rate)

    is OxygenSaturationRecord ->
        instant(record.time, record.zoneOffset).put("percent", record.percentage.value)

    is SkinTemperatureRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("baselineCelsius", record.baseline?.inCelsius ?: JSONObject.NULL)
            .put("measurementLocation", record.measurementLocation)
            .put("deltas", JSONArray(record.deltas.map { JSONArray(listOf(it.time.toString(), it.delta.inCelsius)) }))

    is BodyTemperatureRecord ->
        instant(record.time, record.zoneOffset)
            .put("celsius", record.temperature.inCelsius)
            .put("measurementLocation", record.measurementLocation)

    is ExerciseSessionRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("exerciseType", record.exerciseType)
            .put("hasTitle", record.title != null)
            .put("segments", record.segments.size)
            .put("laps", record.laps.size)

    is ActiveCaloriesBurnedRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("kcal", record.energy.inKilocalories)

    is TotalCaloriesBurnedRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("kcal", record.energy.inKilocalories)

    is DistanceRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("meters", record.distance.inMeters)

    is MindfulnessSessionRecord ->
        interval(record.startTime, record.startZoneOffset, record.endTime, record.endZoneOffset)
            .put("sessionType", record.mindfulnessSessionType)

    else -> JSONObject().put("unhandled", record::class.simpleName)
}

private fun interval(start: Instant, startOffset: ZoneOffset?, end: Instant, endOffset: ZoneOffset?): JSONObject =
    JSONObject()
        .put("start", start.toString())
        .put("startOffset", startOffset?.id ?: JSONObject.NULL)
        .put("end", end.toString())
        .put("endOffset", endOffset?.id ?: JSONObject.NULL)

private fun instant(time: Instant, offset: ZoneOffset?): JSONObject =
    JSONObject()
        .put("time", time.toString())
        .put("offset", offset?.id ?: JSONObject.NULL)
