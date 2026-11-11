extends SceneTree
## Minimal headless test runner: `godot --headless --path . -s tests/run.gd`. Exit code 1 on failure.

func _init() -> void:
	var failures := 0
	failures += _check("midnight is dark", is_equal_approx(Daylight.sun_height(0.0), 0.0))
	failures += _check("noon is bright", is_equal_approx(Daylight.sun_height(0.5), 1.0))
	failures += _check("dawn is half", is_equal_approx(Daylight.sun_height(0.25), 0.5))
	quit(1 if failures > 0 else 0)


func _check(name: String, ok: bool) -> int:
	print(("PASS " if ok else "FAIL ") + name)
	return 0 if ok else 1
