extends Node2D

const WORLD_W := 360.0
const CYCLE_SECONDS := 24.0
const FPS_CAPS := [0, 30, 15] # 0 = uncapped (vsync)

@onready var cam: Camera2D = $Camera
@onready var grade: ShaderMaterial = $Grade/Rect.material
@onready var label: Label = $Hud/Label

var steps_text := "steps: no bridge"
var cap_index := 0
var last_touch_ms := -10000
var auto_dir := 1.0
var cam_x := 0.0
var worst_ms := 0.0
var frames := 0


func _ready() -> void:
	$Character.play("idle")
	cam_x = cam.position.x
	if Engine.has_singleton("HcBridge"):
		var bridge := Engine.get_singleton("HcBridge")
		bridge.connect("steps_read", _on_steps_read)
		steps_text = "steps: reading"
		bridge.readTodaySteps()
	var shot := _arg("--shot=")
	if shot != "":
		_screenshots(shot)


func _process(delta: float) -> void:
	var seconds := Time.get_ticks_msec() / 1000.0
	var forced := _arg("--time=")
	var t := float(forced) if forced != "" else fmod(seconds / CYCLE_SECONDS, 1.0)
	grade.set_shader_parameter("time_of_day", t)

	if Time.get_ticks_msec() - last_touch_ms > 3000:
		_pan(auto_dir * 12.0 * delta)

	frames += 1
	worst_ms = max(worst_ms, delta * 1000.0)
	if frames % 30 == 0:
		label.text = "%d fps  worst %d ms  cap %s\n%s\nview %dx%d" % [
			Engine.get_frames_per_second(), worst_ms, FPS_CAPS[cap_index], steps_text,
			get_viewport_rect().size.x, get_viewport_rect().size.y,
		]
		worst_ms = 0.0


func _unhandled_input(event: InputEvent) -> void:
	# Touch arrives as emulated mouse events too, so one branch covers phone and desktop.
	if event is InputEventMouseMotion and event.button_mask & MOUSE_BUTTON_MASK_LEFT:
		last_touch_ms = Time.get_ticks_msec()
		_pan(-event.relative.x)
	elif event is InputEventMouseButton and event.pressed and event.double_click:
		cap_index = (cap_index + 1) % FPS_CAPS.size()
		Engine.max_fps = FPS_CAPS[cap_index]


func _pan(dx: float) -> void:
	var half := get_viewport_rect().size.x / 2.0
	var target := clampf(cam_x + dx, half, WORLD_W - half)
	if target == cam_x and dx != 0.0:
		auto_dir = -auto_dir
	cam_x = target
	cam.position.x = cam_x


func _on_steps_read(total: int, error: String) -> void:
	steps_text = "steps: %d" % total if error == "" else "steps: " + error


func _arg(prefix: String) -> String:
	for a in OS.get_cmdline_user_args():
		if a.begins_with(prefix):
			return a.trim_prefix(prefix)
	return ""


## Desktop check only: `godot --path . -- --shot=<folder>` saves noon, dusk and night frames, then quits.
func _screenshots(folder: String) -> void:
	set_process(false)
	for shot in [["noon", 0.5, 90.0], ["dusk", 0.74, 180.0], ["night", 0.0, 270.0]]:
		grade.set_shader_parameter("time_of_day", shot[1])
		cam.position.x = shot[2]
		for i in 20:
			await get_tree().process_frame
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("%s/%s.png" % [folder, shot[0]])
	get_tree().quit()
