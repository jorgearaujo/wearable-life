package dev.wearablelife.hclogger

import androidx.health.connect.client.HealthConnectFeatures
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
import kotlin.reflect.KClass

/** One Health Connect record type the logger reads. [feature] is set when the type is not on every phone. */
class LoggedType(
    val name: String,
    val kClass: KClass<out Record>,
    val feature: Int? = null,
)

val LOGGED_TYPES: List<LoggedType> = listOf(
    LoggedType("Steps", StepsRecord::class),
    LoggedType("SleepSession", SleepSessionRecord::class),
    LoggedType("HeartRate", HeartRateRecord::class),
    LoggedType("RestingHeartRate", RestingHeartRateRecord::class),
    LoggedType("HeartRateVariabilityRmssd", HeartRateVariabilityRmssdRecord::class),
    LoggedType("RespiratoryRate", RespiratoryRateRecord::class),
    LoggedType("OxygenSaturation", OxygenSaturationRecord::class),
    LoggedType("SkinTemperature", SkinTemperatureRecord::class, HealthConnectFeatures.FEATURE_SKIN_TEMPERATURE),
    LoggedType("BodyTemperature", BodyTemperatureRecord::class),
    LoggedType("ExerciseSession", ExerciseSessionRecord::class),
    LoggedType("ActiveCaloriesBurned", ActiveCaloriesBurnedRecord::class),
    LoggedType("TotalCaloriesBurned", TotalCaloriesBurnedRecord::class),
    LoggedType("Distance", DistanceRecord::class),
    LoggedType("MindfulnessSession", MindfulnessSessionRecord::class, HealthConnectFeatures.FEATURE_MINDFULNESS_SESSION),
)

val LOGGED_FEATURES: Map<String, Int> = mapOf(
    "backgroundRead" to HealthConnectFeatures.FEATURE_READ_HEALTH_DATA_IN_BACKGROUND,
    "historyRead" to HealthConnectFeatures.FEATURE_READ_HEALTH_DATA_HISTORY,
    "skinTemperature" to HealthConnectFeatures.FEATURE_SKIN_TEMPERATURE,
    "mindfulnessSession" to HealthConnectFeatures.FEATURE_MINDFULNESS_SESSION,
)
