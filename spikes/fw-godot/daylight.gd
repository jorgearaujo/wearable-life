class_name Daylight
## Stand-in for "pure logic": no nodes, no engine state. 0 = midnight, 0.5 = noon.

static func sun_height(time_of_day: float) -> float:
	return 0.5 - 0.5 * cos(time_of_day * TAU)
