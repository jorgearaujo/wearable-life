@tool
extends EditorPlugin

var export_plugin: AndroidExport


func _enter_tree() -> void:
	export_plugin = AndroidExport.new()
	add_export_plugin(export_plugin)


func _exit_tree() -> void:
	remove_export_plugin(export_plugin)
	export_plugin = null


class AndroidExport extends EditorExportPlugin:
	func _get_name() -> String:
		return "HcBridge"

	func _supports_platform(platform: EditorExportPlatform) -> bool:
		return platform is EditorExportPlatformAndroid

	func _get_android_libraries(_platform: EditorExportPlatform, _debug: bool) -> PackedStringArray:
		return PackedStringArray(["hc_bridge/hcbridge.aar"])

	func _get_android_dependencies(_platform: EditorExportPlatform, _debug: bool) -> PackedStringArray:
		return PackedStringArray(["androidx.health.connect:connect-client:1.1.0"])

	# Health Connect revokes health permissions from apps that do not declare where
	# their privacy rationale is shown, so the app needs these two entries.
	func _get_android_manifest_activity_element_contents(_platform: EditorExportPlatform, _debug: bool) -> String:
		return """
			<intent-filter>
				<action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" />
			</intent-filter>
		"""

	func _get_android_manifest_application_element_contents(_platform: EditorExportPlatform, _debug: bool) -> String:
		return """
			<activity-alias
				android:name="ViewPermissionUsageActivity"
				android:exported="true"
				android:targetActivity="com.godot.game.GodotApp"
				android:permission="android.permission.START_VIEW_PERMISSION_USAGE">
				<intent-filter>
					<action android:name="android.intent.action.VIEW_PERMISSION_USAGE" />
					<category android:name="android.intent.category.HEALTH_PERMISSIONS" />
				</intent-filter>
			</activity-alias>
		"""
