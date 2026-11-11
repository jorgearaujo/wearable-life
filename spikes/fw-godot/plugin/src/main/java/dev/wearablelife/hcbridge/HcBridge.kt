package dev.wearablelife.hcbridge

import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.permission.HealthPermission
import androidx.health.connect.client.records.StepsRecord
import androidx.health.connect.client.request.AggregateRequest
import androidx.health.connect.client.time.TimeRangeFilter
import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import org.godotengine.godot.Godot
import org.godotengine.godot.plugin.GodotPlugin
import org.godotengine.godot.plugin.SignalInfo
import org.godotengine.godot.plugin.UsedByGodot

/**
 * Minimal bridge for the framework spike: GDScript calls readTodaySteps() and gets a
 * steps_read(total, error) signal back. Nothing is logged and nothing leaves the phone.
 * The permission is granted over adb for the spike; a real bridge would show the permission screen.
 */
class HcBridge(godot: Godot) : GodotPlugin(godot) {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    override fun getPluginName() = "HcBridge"

    override fun getPluginSignals() =
        setOf(SignalInfo("steps_read", Long::class.javaObjectType, String::class.java))

    @UsedByGodot
    fun readTodaySteps() {
        val context = activity?.applicationContext ?: return
        scope.launch {
            try {
                if (HealthConnectClient.getSdkStatus(context) != HealthConnectClient.SDK_AVAILABLE) {
                    emitSignal("steps_read", -1L, "Health Connect unavailable")
                    return@launch
                }
                val client = HealthConnectClient.getOrCreate(context)
                val permission = HealthPermission.getReadPermission(StepsRecord::class)
                if (permission !in client.permissionController.getGrantedPermissions()) {
                    emitSignal("steps_read", -1L, "no permission")
                    return@launch
                }
                val startOfDay = LocalDate.now().atStartOfDay(ZoneId.systemDefault()).toInstant()
                val result = client.aggregate(
                    AggregateRequest(
                        metrics = setOf(StepsRecord.COUNT_TOTAL),
                        timeRangeFilter = TimeRangeFilter.between(startOfDay, Instant.now()),
                    ),
                )
                emitSignal("steps_read", result[StepsRecord.COUNT_TOTAL] ?: 0L, "")
            } catch (e: Exception) {
                emitSignal("steps_read", -1L, e.javaClass.simpleName)
            }
        }
    }
}
