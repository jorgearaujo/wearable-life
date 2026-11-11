package dev.wearablelife.hc_bridge

import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.PermissionController
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch

/**
 * Hosts Flutter and answers its calls on one platform channel. FlutterFragmentActivity, not
 * FlutterActivity, because the Health Connect permission screen needs an activity-result launcher.
 */
class MainActivity : FlutterFragmentActivity() {
    private val scope: CoroutineScope = MainScope()
    private var pendingPermissionResult: MethodChannel.Result? = null

    private val permissionRequest =
        registerForActivityResult(PermissionController.createRequestPermissionResultContract()) { granted ->
            pendingPermissionResult?.success(granted.size)
            pendingPermissionResult = null
        }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        HealthReader.flutterAttached = true
        ReadWorker.schedule(this)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "wearablelife/health")
            .setMethodCallHandler { call, result ->
                scope.launch {
                    try {
                        when (call.method) {
                            "status" -> result.success(status())
                            "requestPermissions" -> {
                                pendingPermissionResult = result
                                permissionRequest.launch(HealthReader.permissions)
                            }
                            "readNow" -> result.success(HealthReader.read(this@MainActivity, "screen"))
                            "history" -> result.success(HealthReader.history(this@MainActivity))
                            "compareSteps" -> result.success(HealthReader.compareSteps(this@MainActivity))
                            else -> result.notImplemented()
                        }
                    } catch (e: Exception) {
                        result.error("bridge", e.javaClass.simpleName, null)
                    }
                }
            }
    }

    override fun onDestroy() {
        HealthReader.flutterAttached = false
        scope.cancel()
        super.onDestroy()
    }

    private suspend fun status(): Map<String, Any> {
        val sdkStatus = HealthConnectClient.getSdkStatus(this)
        val granted = if (sdkStatus == HealthConnectClient.SDK_AVAILABLE) {
            HealthConnectClient.getOrCreate(this).permissionController.getGrantedPermissions()
                .intersect(HealthReader.permissions).size
        } else {
            0
        }
        return mapOf(
            "available" to (sdkStatus == HealthConnectClient.SDK_AVAILABLE),
            "granted" to granted,
            "wanted" to HealthReader.permissions.size,
        )
    }
}
