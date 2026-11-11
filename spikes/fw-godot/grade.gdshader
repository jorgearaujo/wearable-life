shader_type canvas_item;

// Full-screen color grade over the shared art: day is untouched, dusk is warm, night is a blue ramp.
uniform sampler2D screen : hint_screen_texture, filter_nearest;
uniform float time_of_day = 0.5; // 0 = midnight, 0.5 = noon

void fragment() {
	vec3 c = texture(screen, SCREEN_UV).rgb;
	float lum = dot(c, vec3(0.299, 0.587, 0.114));
	float sun = 0.5 - 0.5 * cos(time_of_day * TAU);
	float night = 1.0 - smoothstep(0.15, 0.45, sun);
	float dusk = smoothstep(0.1, 0.35, sun) * (1.0 - smoothstep(0.35, 0.7, sun));
	vec3 dusk_c = c * vec3(1.15, 0.85, 0.7) + vec3(0.06, 0.0, 0.03);
	vec3 night_c = mix(vec3(0.04, 0.05, 0.14), vec3(0.45, 0.55, 0.85), lum);
	c = mix(c, dusk_c, dusk * 0.8);
	c = mix(c, night_c, night * 0.9);
	COLOR = vec4(c, 1.0);
}
