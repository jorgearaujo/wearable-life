import 'dart:math';
import 'dart:ui' as ui;

import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
// ignore: deprecated_member_use
import 'package:flame/input.dart' show TapDetector;
import 'package:flame/post_process.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

const worldW = 240.0;
const worldH = 280.0;
const baseW = 120.0;
const cycleSeconds = 40.0;
const bankY = 196.0; // top of the bank the character stands on
const waterY = 208.0;

/// Set with --dart-define=FIXED_TIME=0 to hold one time of day, in thousandths (0 = midnight, 500 = noon).
const fixedTime = int.fromEnvironment('FIXED_TIME', defaultValue: -1);

// Light sources in world (art pixel) coordinates.
final firePos = Vector2(166, bankY - 8);
final windowPos = Vector2(83, bankY - 17); // the cabin window in ground.png

/// Tap to step through these: (name, time of day, weather). "cycle" runs a whole day in [cycleSeconds].
/// Weather: 0 clear, 1 rain, 2 fog. --dart-define=HOLD=5 starts on one of them.
const holds = <(String, double, int)>[
  ('cycle', -1, 0),
  ('night', 0, 0),
  ('dawn', 0.27, 0),
  ('day', 0.5, 0),
  ('dusk', 0.74, 0),
  ('day rain', 0.5, 1),
  ('dusk rain', 0.74, 1),
  ('night rain', 0, 1),
  ('dawn fog', 0.27, 2),
  ('night fog', 0, 2),
];

/// Palette rows: 0 night, 1 dawn, 2 day, 3 dusk. Each key is (time of day, row); between keys the two
/// rows are mixed, so day and night hold steady and dawn and dusk pass through.
const paletteKeys = <(double, double)>[(0, 0), (0.2, 0), (0.27, 1), (0.36, 2), (0.64, 2), (0.74, 3), (0.82, 0), (1, 0)];
const rowDarkness = [1.0, 0.5, 0.0, 0.6];
// Fog and rain are ordinary colours, not palette indices, so they need their own colour per palette row.
const fogColours = [Color(0xFF46598C), Color(0xFFFADCD7), Color(0xFFE1EBF0), Color(0xFFC896AA)];
const rainColours = [Color(0xFF8CA0D2), Color(0xFFFFF0EB), Color(0xFFF0F5FA), Color(0xFFF0C8D2)];

final hudText = ValueNotifier('...');

/// Made-up meter levels out of 5 (Sleep, Energy, Activity); a tap that changes the time also changes these.
const meterSets = [
  [4, 3, 2],
  [5, 4, 1],
  [2, 2, 4],
  [3, 5, 5],
];
const meterReasons = [
  'Sleep is high: a long, steady night.',
  'Energy starts lower today: your resting heart rate is higher than usual.',
  'Activity is filling up: a good walk this morning.',
];
const cabinReasons = [
  'The cabin is under its cover for now. Nothing is lost.',
  'The cabin is open again.',
  'A good week: the flowers by the door have opened.',
];
const fireReasons = ['The fire is resting. The logs are still there.', 'The fire is lit again.'];

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  final program = await ui.FragmentProgram.fromAsset('shaders/grade.frag');
  final paletteData = await rootBundle.load('assets/images/palette.png');
  final palette = (await (await ui.instantiateImageCodec(paletteData.buffer.asUint8List())).getNextFrame()).image;
  // Give the game a box that is an exact whole multiple of the art size in physical pixels,
  // centred on a physical pixel. Without this, screens that 120 does not divide get uneven pixels.
  final view = ui.PlatformDispatcher.instance.views.first;
  final fit = PixelFit(view.physicalSize);
  final dpr = view.devicePixelRatio;
  runApp(
    ColoredBox(
      color: const Color(0xFF000000),
      child: Align(
        alignment: Alignment.topLeft,
        child: Padding(
          padding: EdgeInsets.only(left: fit.left / dpr, top: fit.top / dpr),
          child: SizedBox(
            width: fit.viewW * fit.scale / dpr,
            height: fit.viewH * fit.scale / dpr,
            child: Stack(
              alignment: Alignment.topLeft, // the default needs a text direction, which nothing here provides
              children: [
                GameWidget(game: SpikeGame(program, fit, palette)),
                // Debug text sits outside the game: inside it, the shader would read it as palette indices.
                Positioned(
                  left: 12,
                  bottom: 16,
                  child: ValueListenableBuilder(
                    valueListenable: hudText,
                    builder: (_, text, _) => Text(
                      text,
                      textDirection: TextDirection.ltr,
                      style: const TextStyle(fontSize: 12, color: Color(0xFFFFFFFF), decoration: TextDecoration.none),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

/// Whole-number scale and a view size in whole art pixels for a given screen.
class PixelFit {
  PixelFit(ui.Size physical)
    : scale = max(1, (physical.width / baseW).floor()),
      viewW = 0,
      viewH = 0,
      left = 0,
      top = 0 {
    viewW = (physical.width / scale).floorToDouble();
    viewH = min(worldH, (physical.height / scale).floorToDouble());
    left = ((physical.width - viewW * scale) / 2).floorToDouble();
    top = ((physical.height - viewH * scale) / 2).floorToDouble();
  }

  final int scale;
  double viewW, viewH, left, top;
}

// ignore: deprecated_member_use
class SpikeGame extends FlameGame with PanDetector, TapDetector {
  SpikeGame(this.program, this.fit, this.palette);

  final PixelFit fit;
  final ui.Image palette;
  int hold = const int.fromEnvironment('HOLD');

  final ui.FragmentProgram program;
  late final GradePostProcess grade;
  final layers = <(SpriteComponent, double)>[];
  late final SpriteComponent sun, moon, tarp, flowers;
  late final List<Sprite> moonFrames;
  int moonPhase = 4; // 0 new, 2 first quarter, 4 full, 6 last quarter
  late final List<Sprite> flowerFrames;
  late final Hud hud;
  late final Hero hero;
  late final Stones stones;
  late final Dog dog;

  /// 0 dormant (under a tarp), 1 open, 2 flourishing (flowers open). Tap the cabin to step through.
  int cabin = 1;
  bool fireLit = true; // tap the fire
  double fireGlow = 1, windowGlow = 1;

  double camLeft = 60;
  double viewW = baseW;
  double autoDir = 1;
  double sinceTouch = 10;
  double elapsed = 0;

  // Frame timing straight from the engine, so it includes raster time.
  int frames = 0;
  double worstMs = 0;
  double fps = 0;
  double window = 0;

  @override
  Color backgroundColor() => const Color(0xFF000000);

  @override
  Future<void> onLoad() async {
    // Integer scaling: the largest whole number of physical pixels per art pixel that fits 120 across.
    viewW = fit.viewW;
    final viewH = fit.viewH;

    for (final (name, factor) in [('sky', 0.0), ('hills', 0.3), ('trees', 0.6), ('ground', 1.0)]) {
      final layer = SpriteComponent(sprite: await loadSprite('$name.png'));
      layers.add((layer, factor));
      world.add(layer);
      if (name == 'sky') {
        // Sun and moon sit between the sky and the hills, so they rise and set behind the ridge.
        sun = SpriteComponent(sprite: await loadSprite('sun.png'));
        final moonSheet = await images.load('moon.png');
        moonFrames = [
          for (var f = 0; f < 8; f++) Sprite(moonSheet, srcPosition: Vector2(35.0 * f, 0), srcSize: Vector2.all(35)),
        ];
        moon = SpriteComponent(sprite: moonFrames[moonPhase]);
        world.addAll([Stars(this), sun, moon]);
      }
    }
    final flowerSheet = await images.load('flowers.png');
    flowerFrames = [
      for (var f = 0; f < 2; f++) Sprite(flowerSheet, srcPosition: Vector2(70.0 * f, 0), srcSize: Vector2(70, 8)),
    ];
    flowers = SpriteComponent(sprite: flowerFrames[0], position: Vector2(38, bankY - 7));
    tarp = SpriteComponent(sprite: await loadSprite('tarp.png'), position: Vector2(40, bankY - 53))..opacity = 0;
    world.addAll([tarp, flowers]);
    hero = Hero(this, await images.load('character.png'));
    stones = Stones(this);
    dog = Dog(this, await images.load('dog.png'));
    world.addAll([dog, hero]);
    world.add(Props(this));
    world.add(Wildlife(this, await images.load('duck.png'), await images.load('squirrel.png')));
    world.add(stones);

    camera = CameraComponent.withFixedResolution(width: viewW, height: viewH, world: world);
    camera.viewfinder.anchor = Anchor.topLeft;
    // Anchored to the bottom, so the water is always in view and a taller screen shows more sky.
    camera.viewfinder.position = Vector2(camLeft, worldH - viewH);
    grade = GradePostProcess(program, palette);
    camera.postProcess = grade;
    // The interface is an ordinary component outside the camera, so the shader never touches it.
    final sheet = await images.load('ui.png');
    hud = Hud(this, sheet, await Hud.measure(sheet));
    // Flame gives the camera the highest priority, so it would draw over everything else in the game.
    camera.priority = 0;
    add(hud..priority = 10);
    _pan(0);
  }

  @override
  void onTapDown(TapDownInfo info) {
    sinceTouch = 0; // a tap holds the view still for a moment, like a drag does
    // canvasSize is the widget on screen; `size` is the camera's view in art pixels.
    final scale = canvasSize.x / viewW;
    final vx = info.eventPosition.widget.x / scale, vy = info.eventPosition.widget.y / scale;
    final wx = vx + camera.viewfinder.position.x, wy = vy + camera.viewfinder.position.y;
    final row = ((vy - Hud.metersTop) / 9).floor();
    if (vx < 48 && row >= 0 && row < 3) {
      hud.say(meterReasons[row]);
    } else if (moon.opacity > 0 && (wx - moon.x - 17).abs() < 14 && (wy - moon.y - 17).abs() < 14) {
      // The real phase comes from the date; here a tap steps through the eight drawn frames.
      moonPhase = (moonPhase + 1) % 8;
      moon.sprite = moonFrames[moonPhase];
    } else if (wx > 40 && wx < 106 && wy > bankY - 53 && wy < bankY) {
      cabin = (cabin + 1) % 3;
      tarp.opacity = cabin == 0 ? 1 : 0; // all or nothing: half-transparent indices would be wrong colours
      flowers.sprite = flowerFrames[cabin == 2 ? 1 : 0];
      hud.say(cabinReasons[cabin]);
    } else if ((wx - firePos.x).abs() < 14 && wy > bankY - 24 && wy < bankY + 6) {
      fireLit = !fireLit;
      hud.say(fireReasons[fireLit ? 1 : 0]);
    } else if (wx > dogX && wx < dogX + 24 && wy > bankY - 19 && wy < bankY) {
      // Pet the dog: the character walks round to its head first. A toy; no meter changes.
      hero.go(dogX + 28, Act.pet);
    } else if (wy > waterY + 3) {
      // Skip a stone to where the water was tapped: walk to a spot a throw away, pick one up, throw.
      final dir = wx >= hero.x ? 1.0 : -1.0;
      hero.aim = Vector2(wx.clamp(6.0, worldW - 6), wy.floorToDouble());
      hero.aimDir = dir;
      var spot = (hero.aim.x - dir * 34).clamp(10.0, worldW - 10);
      // Not on top of the dog: stand just beside it instead.
      if (spot > dogX - 10 && spot < dogX + 34) spot = spot < dogX + 12 ? dogX - 10 : dogX + 34;
      hero.go(spot, Act.pick);
    } else {
      hold = (hold + 1) % holds.length;
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    elapsed += dt;
    worstMs = max(worstMs, dt * 1000.0); // frame-to-frame gap, same measure as the Godot spike
    sinceTouch += dt;
    // Move the camera first: everything below is placed relative to it. Placed before the move, the sun,
    // the moon and the lights sat one pixel off for a frame at every camera step, which looked like shaking.
    if (hero.busy) {
      // While the character is doing something, the camera follows it instead of drifting.
      sinceTouch = 0;
      _pan((hero.x - viewW / 2 - camLeft).clamp(-40 * dt, 40 * dt));
    } else if (sinceTouch > 3) {
      _pan(autoDir * 12 * dt);
    }
    final held = holds[hold].$2;
    final t = fixedTime >= 0
        ? fixedTime / 1000
        : held >= 0
        ? held
        : (elapsed / cycleSeconds + 0.3) % 1.0;
    var k = 0;
    while (t > paletteKeys[k + 1].$1) {
      k++;
    }
    final (t0, rowA) = paletteKeys[k];
    final (t1, rowB) = paletteKeys[k + 1];
    final mix = (t - t0) / (t1 - t0);
    grade
      ..rowA = rowA
      ..rowB = rowB
      ..mix = mix
      ..dark = rowDarkness[rowA.toInt()] * (1 - mix) + rowDarkness[rowB.toInt()] * mix
      ..fogColour = Color.lerp(fogColours[rowA.toInt()], fogColours[rowB.toInt()], mix)!
      ..rainColour = Color.lerp(rainColours[rowA.toInt()], rainColours[rowB.toInt()], mix)!
      ..elapsed = elapsed
      ..camX = camera.viewfinder.position.x;
    // Weather fades in and out over about a second.
    final weather = holds[hold].$3;
    grade.rain = (grade.rain + (weather == 1 ? dt : -dt)).clamp(0.0, 1.0);
    grade.fog = (grade.fog + (weather == 2 ? dt : -dt)).clamp(0.0, 1.0);
    // Flicker in steps, about 8 times a second, so the glow jumps like pixel art and does not pulse smoothly.
    final step = (elapsed * 8).floor();
    final flicker = 0.85 + 0.15 * sin(step * 12.9898).abs();
    final origin = camera.viewfinder.position;
    grade
      ..step = step.toDouble()
      ..waterline = waterY - origin.y;
    // Lights go out and come back over half a second when the fire or cabin changes state.
    fireGlow = (fireGlow + (fireLit ? 2 : -2) * dt).clamp(0.0, 1.0);
    windowGlow = (windowGlow + (cabin > 0 ? 2 : -2) * dt).clamp(0.0, 1.0);
    grade.lights[0].setValues(firePos.x - origin.x, firePos.y - origin.y, 40 * flicker, fireGlow);
    // The window is a flat lit shape with one thin ring around it; the dark scene does the rest.
    grade.lights[1].setValues(windowPos.x - origin.x, windowPos.y - origin.y, 9, 0.34 * windowGlow);
    // Sun and moon each cross the sky on an arc and set behind the hills. Rain clouds hide them.
    _arc(sun, (t - 0.22) / 0.56, 112, origin.x);
    _arc(moon, ((t - 0.72) % 1.0) / 0.56, 100, origin.x);
    frames++;
    window += dt;
    if (frames % 30 == 0) {
      fps = 30 / window;
      window = 0;
      hudText.value =
          '${fps.round()} fps  worst ${worstMs.round()} ms\n'
          'view ${viewW.round()}x${fit.viewH.round()}  ${holds[hold].$1}\n'
          'tap: the dog, the water, a meter, the cabin,\nthe fire, the moon, or the sky';
      worstMs = 0;
    }
  }

  @override
  void onPanUpdate(DragUpdateInfo info) {
    sinceTouch = 0;
    _pan(-info.delta.global.x / (canvasSize.x / viewW));
  }

  /// Places a sky body along its arc; [s] runs 0 to 1 from rising to setting, anything else is below ground.
  void _arc(SpriteComponent body, double s, double height, double left) {
    final up = s >= 0 && s <= 1 && grade.rain < 0.5;
    body.opacity = up ? 1 : 0;
    // Top-left of a 35 pixel sprite, on whole pixels: a centre anchor would land on half pixels.
    body.position = Vector2(left + (92 * s).roundToDouble() - 3, (135 - sin(pi * s) * height).roundToDouble());
  }

  void _pan(double dx) {
    final target = (camLeft + dx).clamp(0.0, worldW - viewW);
    if (target == camLeft && dx != 0) {
      autoDir = -autoDir;
    }
    camLeft = target;
    // Whole art pixels only: fractional positions are what cause seams and shimmer.
    final snapped = camLeft.roundToDouble();
    camera.viewfinder.position = Vector2(snapped, camera.viewfinder.position.y);
    for (final (layer, factor) in layers) {
      layer.x = (snapped * (1 - factor)).roundToDouble();
    }
  }
}

/// Renders the world once into a low-resolution image of palette indices, then draws it through the
/// shader, which turns indices into colours for the time of day, adds the lights and mirrors the water.
/// Rain and fog are then drawn on top as ordinary translucent shapes, in art pixels: the indexed scene
/// cannot blend, but anything drawn after the shader can.
class GradePostProcess extends PostProcess {
  GradePostProcess(ui.FragmentProgram program, this.palette) : shader = program.fragmentShader(), super(pixelRatio: 1);

  final ui.FragmentShader shader;
  final ui.Image palette;
  double rowA = 2, rowB = 2, mix = 0, dark = 0, waterline = 0, step = 0;
  double rain = 0, fog = 0, elapsed = 0, camX = 0;
  Color fogColour = fogColours[2], rainColour = rainColours[2];

  // Fixed random sets: (x, y, speed) per rain streak and (x, y, width, drift) per fog wisp.
  static final _rng = Random(7);
  final _streaks = List.generate(70, (_) => (_rng.nextDouble(), _rng.nextDouble(), 150 + _rng.nextDouble() * 70));
  final _wisps = List.generate(
    9,
    (_) => (_rng.nextDouble(), _rng.nextDouble(), 40 + _rng.nextDouble() * 50, 2 + _rng.nextDouble() * 4),
  );

  /// x, y in view pixels, radius in art pixels, strength 0 to 1.
  final lights = [Vector4.zero(), Vector4.zero()];

  @override
  void postProcess(Vector2 size, Canvas canvas) {
    final scene = rasterizeSubtree();
    var i = 0;
    for (final v in [
      size.x,
      size.y,
      scene.width.toDouble(),
      scene.height.toDouble(),
      rowA,
      rowB,
      mix,
      dark,
      waterline,
      step,
      max(rain, fog),
    ]) {
      shader.setFloat(i++, v);
    }
    for (final l in lights) {
      for (final v in [l.x, l.y, l.z, l.w]) {
        shader.setFloat(i++, v);
      }
    }
    shader
      ..setImageSampler(0, scene)
      ..setImageSampler(1, palette);
    canvas.drawRect(Offset.zero & size.toSize(), Paint()..shader = shader);
    if (rain > 0 || fog > 0) {
      _weather(canvas, size, scene.width.toDouble(), scene.height.toDouble());
    }
    scene.dispose();
  }

  /// A repeatable random number from 0 to 1 for a pair of whole numbers.
  static double _hash(int a, int b) {
    var x = (a * 374761393 + b * 668265263) & 0x7fffffff;
    x = ((x ^ (x >> 13)) * 1274126177) & 0x7fffffff;
    return ((x ^ (x >> 16)) & 0xffff) / 65536;
  }

  void _weather(Canvas canvas, Vector2 size, double w, double h) {
    canvas.save();
    canvas.scale(size.x / w, size.y / h); // from here on, one unit is one art pixel
    if (fog > 0) {
      final paint = Paint()..isAntiAlias = false;
      // A thin veil over everything, a thicker one low down, then drifting wisps that stack up.
      canvas.drawRect(Rect.fromLTWH(0, 0, w, h), paint..color = fogColour.withValues(alpha: 0.16 * fog));
      canvas.drawRect(
        Rect.fromLTWH(0, waterline - 70, w, 70 + h),
        paint..color = fogColour.withValues(alpha: 0.18 * fog),
      );
      paint.color = fogColour.withValues(alpha: 0.2 * fog);
      for (final (x, y, width, drift) in _wisps) {
        final span = w + width;
        final left = ((x * span + elapsed * drift - camX * 0.8) % span - width).floorToDouble();
        final top = (waterline - 78 + y * 84).floorToDouble();
        canvas.drawRect(Rect.fromLTWH(left, top, width, 5), paint);
        canvas.drawRect(Rect.fromLTWH(left + 6, top - 2, width - 16, 9), paint);
      }
    }
    if (rain > 0) {
      final paint = Paint()
        ..isAntiAlias = false
        ..color = rainColour.withValues(alpha: 0.38 * rain);
      for (final (x, y, speed) in _streaks) {
        // Fine slanted streaks: five pixels tall, one wide, stepping left once on the way down.
        final py = ((y * (h + 8) + elapsed * speed) % (h + 8) - 8).floorToDouble();
        final px = ((x * w - py * 0.25 - camX) % w).floorToDouble();
        canvas.drawRect(Rect.fromLTWH(px, py, 1, 3), paint);
        canvas.drawRect(Rect.fromLTWH(px - 1, py + 3, 1, 2), paint);
      }
      // Drops landing on the water: a bright dot, then a flat ring that widens and fades in three more steps.
      // Each ripple picks a new spot every time it restarts; spots are fixed to the world, not the screen.
      const life = 0.48;
      for (var i = 0; i < 30; i++) {
        final phase = elapsed / life + i * 0.37;
        final cycle = phase.floor();
        final stage = ((phase - cycle) * 4).floor();
        final x = (_hash(i, cycle) * worldW - camX).floorToDouble();
        final y = (waterline + 2 + _hash(i, cycle + 9999) * (h - waterline - 3)).floorToDouble();
        if (x < -8 || x > w + 8 || y >= h) {
          continue;
        }
        paint.color = rainColour.withValues(alpha: const [0.9, 0.7, 0.45, 0.22][stage] * rain);
        if (stage == 0) {
          canvas.drawRect(Rect.fromLTWH(x, y - 1, 1, 2), paint);
        } else {
          // A flat ellipse outline: top and bottom arcs, one pixel at each side.
          final reach = stage * 2.0;
          canvas.drawRect(Rect.fromLTWH(x - reach + 1, y - 1, reach * 2 - 1, 1), paint);
          canvas.drawRect(Rect.fromLTWH(x - reach + 1, y + 1, reach * 2 - 1, 1), paint);
          canvas.drawRect(Rect.fromLTWH(x - reach, y, 1, 1), paint);
          canvas.drawRect(Rect.fromLTWH(x + reach, y, 1, 1), paint);
        }
      }
    }
    canvas.restore();
  }
}

/// Placeholder campfire, drawn as rectangles in palette-index colours (red = index * 4).
Paint indexPaint(int index) => Paint()
  ..color = Color.fromARGB(255, index * 4, 0, 0)
  ..isAntiAlias = false;

double _noise(int a, int b) => (sin(a * 12.9898 + b * 78.233) * 43758.5453).abs() % 1.0;

/// Stars as single pixels drawn by the game, not painted into the sky. Each has its own moment to come
/// out as the sky darkens (the bright ones first), and each blinks now and then, in steps.
class Stars extends Component {
  Stars(this.game) {
    final rng = Random(5);
    while (_stars.length < 34) {
      // More of them toward the top; none low enough to sit on the clouds.
      final x = 3 + rng.nextInt(114), y = 16 + (70 * pow(rng.nextDouble(), 1.4)).floor();
      if (_stars.any((s) => (s.$1 - x).abs() < 6 && (s.$2 - y).abs() < 6)) {
        continue;
      }
      final n = _stars.length;
      final kind = n < 4 ? 2 : n < 15 ? 1 : 0; // 2 a cross, 1 bright, 0 dim
      final out = kind == 2 ? 0.3 + 0.05 * n : kind == 1 ? 0.45 + 0.02 * n : 0.62 + 0.017 * (n - 15);
      _stars.add((x, y, kind, out));
    }
  }

  final SpikeGame game;
  final _stars = <(int, int, int, double)>[];
  final _bright = indexPaint(6), _dim = indexPaint(46);

  @override
  void render(Canvas canvas) {
    final grade = game.grade;
    if (grade.rain >= 0.5) {
      return; // rain clouds hide them, as they hide the sun and moon
    }
    final left = game.camera.viewfinder.position.x; // the sky does not scroll
    final beat = (game.elapsed * 3).floor();
    for (var i = 0; i < _stars.length; i++) {
      final (x, y, kind, out) = _stars[i];
      if (grade.dark <= out || (kind == 0 && grade.fog >= 0.5)) {
        continue;
      }
      final blink = _noise(i, beat) > 0.9;
      void dot(int dx, int dy, Paint paint) => canvas.drawRect(Rect.fromLTWH(left + x + dx, y + dy + 0.0, 1, 1), paint);
      if (kind == 0) {
        if (!blink) dot(0, 0, _dim);
      } else {
        dot(0, 0, blink ? _dim : _bright);
        if (kind == 2 && !blink) {
          for (final (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]) {
            dot(dx, dy, _dim);
          }
        }
      }
    }
  }
}

/// A duck on the water and a squirrel on the bank. Both are indexed sprites in colours the scene already
/// has, so they follow the time of day and the firelight like everything else.
class Wildlife extends Component {
  Wildlife(this.game, this.duck, this.squirrel);

  final SpikeGame game;
  final ui.Image duck, squirrel;
  final _rng = Random(3);
  final _paint = Paint()
    ..filterQuality = FilterQuality.none
    ..isAntiAlias = false;

  double duckX = 60, duckDir = 1;
  double squirrelX = 205, squirrelTo = 205, pause = 1.5;
  bool squirrelLeft = false;

  @override
  void update(double dt) {
    // The duck paddles slowly from one side of the water to the other.
    duckX += duckDir * 4 * dt;
    if (duckX < 8 || duckX > worldW - 20) {
      duckDir = -duckDir;
    }
    // The squirrel dashes, stops and sits up. At night and in rain it goes off to the right and stays away:
    // hidden, not gone.
    final away = game.grade.dark > 0.7 || game.grade.rain > 0.5;
    if (away) {
      squirrelTo = worldW + 14;
      pause = 0;
    } else if (squirrelTo > worldW) {
      squirrelTo = 200;
    }
    if (pause > 0) {
      pause -= dt;
    } else if ((squirrelTo - squirrelX).abs() < 1) {
      if (!away) {
        pause = 1 + _rng.nextDouble() * 2.5;
        squirrelTo = 180 + _rng.nextDouble() * 52;
      }
    } else {
      squirrelLeft = squirrelTo < squirrelX;
      squirrelX += (squirrelLeft ? -34 : 34) * dt;
    }
  }

  @override
  void render(Canvas canvas) {
    final beat = (game.elapsed * 2).floor();
    canvas.drawImageRect(
      duck,
      Rect.fromLTWH(beat.isEven ? 0 : 12, duckDir > 0 ? 0 : 8, 12, 8),
      Rect.fromLTWH(duckX.floorToDouble(), waterY + 30, 12, 8),
      _paint,
    );
    final moving = pause <= 0 && (squirrelTo - squirrelX).abs() >= 1;
    final frame = moving ? 2 + (game.elapsed * 8).floor() % 2 : (beat % 5 == 0 ? 1 : 0);
    canvas.drawImageRect(
      squirrel,
      Rect.fromLTWH(frame * 12.0, squirrelLeft ? 10 : 0, 12, 10),
      Rect.fromLTWH(squirrelX.floorToDouble() - 6, bankY - 10, 12, 10),
      _paint,
    );
  }
}

const dogX = 125.0; // left edge of the dog's sprite

enum Act { idle, walk, pet, pick, wind, release }

/// The character. It always shows the action it is doing: it walks to where the action happens first.
/// Positions are kept as fractions and drawn on whole pixels.
class Hero extends Component {
  Hero(this.game, this.sheet);

  final SpikeGame game;
  final ui.Image sheet;
  final _paint = Paint()
    ..filterQuality = FilterQuality.none
    ..isAntiAlias = false;

  double x = 112, target = 112, t = 0, aimDir = 1;
  bool left = false;
  Act act = Act.idle, next = Act.idle;
  Vector2 aim = Vector2.zero();

  bool get busy => act != Act.idle;

  /// Walk to [to], then do [then]. A new request replaces the one in progress.
  void go(double to, Act then) {
    target = to;
    next = then;
    act = Act.walk;
  }

  void _begin(Act a) {
    act = a;
    t = 0;
    if (a == Act.pet) left = true; // the dog faces right; its head is to the character's left
    if (a == Act.pick) left = aimDir < 0;
  }

  @override
  void update(double dt) {
    t += dt;
    switch (act) {
      case Act.idle:
        break;
      case Act.walk:
        final d = target - x;
        if (d.abs() < 0.5) {
          x = target;
          _begin(next);
        } else {
          left = d < 0;
          x += d.sign * min(d.abs(), 30 * dt);
        }
      case Act.pet:
        if (t > 2.4) {
          _begin(Act.idle);
          game.dog.lovedAt = game.elapsed; // the dog answers: a heart, and it stays happy for a moment
        }
      case Act.pick:
        if (t > 0.45) _begin(Act.wind);
      case Act.wind:
        if (t > 0.25) {
          _begin(Act.release);
          game.stones.throwFrom(Vector2(x.floorToDouble() + aimDir * 10, bankY - 16), aim, aimDir);
        }
      case Act.release:
        if (t > 0.4) _begin(Act.idle);
    }
  }

  @override
  void render(Canvas canvas) {
    final frame = switch (act) {
      Act.idle => (game.elapsed * 2).floor() % 2,
      Act.walk => 2 + (x / 3).floor() % 4,
      Act.pet => 6 + (t * 5).floor() % 2,
      Act.pick => 8,
      Act.wind => 9,
      Act.release => 10,
    };
    canvas.drawImageRect(
      sheet,
      Rect.fromLTWH(frame * 24.0, left ? 30 : 0, 24, 30),
      Rect.fromLTWH(x.floorToDouble() - 12, bankY - 30, 24, 30),
      _paint,
    );
  }
}

/// The dog sits where it sat in the ground art, and wags its tail while it is being petted.
class Dog extends Component {
  Dog(this.game, this.sheet);

  final SpikeGame game;
  final ui.Image sheet;
  final _paint = Paint()
    ..filterQuality = FilterQuality.none
    ..isAntiAlias = false;

  double lovedAt = -10; // the heart itself is drawn by the Hud, above the colour pass, so it can fade

  @override
  void render(Canvas canvas) {
    final since = game.elapsed - lovedAt;
    final happy = since < 1.6;
    final wag = (game.hero.act == Act.pet || happy) && (game.elapsed * 6).floor().isOdd;
    // A happy dog bobs up a pixel twice.
    final hop = happy && (since * 5).floor() % 4 == 1 ? 1.0 : 0.0;
    canvas.drawImageRect(sheet, Rect.fromLTWH(wag ? 24 : 0, 0, 24, 17), Rect.fromLTWH(dogX, bankY - 17 - hop, 24, 17), _paint);
  }
}

/// Skipping stones: a stone flies from the hand to the tapped spot on the water, skips a few times in
/// shorter and lower hops, and leaves a ring at every touch. Stone and rings below the waterline carry
/// the "afloat" flag (blue), like the duck, so the shader shows them instead of the reflection.
class Stones extends Component {
  Stones(this.game);

  final SpikeGame game;
  static Paint _flag(int index, bool afloat) => Paint()
    ..color = Color.fromARGB(255, index * 4, 0, afloat ? 255 : 0)
    ..isAntiAlias = false;
  final _stone = _flag(6, false), _wet = _flag(6, true), _ring = _flag(63, true);

  // Each hop: from, to, height, duration. One stone at a time is enough for a toy.
  final _hops = <(Vector2, Vector2, double, double)>[];
  final _rings = <(double, double, double, double)>[]; // x, y, time it appeared, widest radius
  int hop = 0;
  double t = 0;

  void throwFrom(Vector2 hand, Vector2 touch, double dir) {
    _hops
      ..clear()
      ..add((hand, touch, 9, 0.5));
    var from = touch;
    for (final (length, height, time) in [(14.0, 5.0, 0.3), (9.0, 3.0, 0.22), (5.0, 2.0, 0.16), (3.0, 1.0, 0.12)]) {
      final to = Vector2((from.x + dir * length).clamp(1.0, worldW - 2), from.y);
      _hops.add((from, to, height, time));
      from = to;
    }
    hop = 0;
    t = 0;
  }

  @override
  void update(double dt) {
    _rings.removeWhere((r) => game.elapsed - r.$3 > 0.9);
    if (hop >= _hops.length) return;
    t += dt;
    while (hop < _hops.length && t >= _hops[hop].$4) {
      t -= _hops[hop].$4;
      final at = _hops[hop].$2;
      _rings.add((at.x, at.y, game.elapsed, max(4.0, 10.0 - hop * 2)));
      hop++;
    }
  }

  @override
  void render(Canvas canvas) {
    for (final (x, y, born, widest) in _rings) {
      final age = game.elapsed - born;
      if (age < 0.1) {
        // The splash: a short column of spray where the stone touches.
        canvas.drawRect(Rect.fromLTWH(x, y - 2, 2, 3), _ring);
        canvas.drawRect(Rect.fromLTWH(x - 2, y, 6, 1), _ring);
        continue;
      }
      // A flat oval that widens in three steps: closed rows above and below, open ends on the middle row.
      final r = (widest * (age < 0.3 ? 0.45 : age < 0.6 ? 0.75 : 1)).floorToDouble();
      canvas.drawRect(Rect.fromLTWH(x - r + 2, y - 1, 2 * r - 2, 1), _ring);
      canvas.drawRect(Rect.fromLTWH(x - r + 2, y + 1, 2 * r - 2, 1), _ring);
      canvas.drawRect(Rect.fromLTWH(x - r, y, 2, 1), _ring);
      canvas.drawRect(Rect.fromLTWH(x + r, y, 2, 1), _ring);
    }
    if (hop >= _hops.length) return;
    final (from, to, height, time) = _hops[hop];
    final s = t / time;
    final x = (from.x + (to.x - from.x) * s).floorToDouble();
    final y = (from.y + (to.y - from.y) * s - height * 4 * s * (1 - s)).floorToDouble();
    canvas.drawRect(Rect.fromLTWH(x, y - 1, 2, 2), y - 1 >= waterY ? _wet : _stone);
  }
}

class Props extends Component {
  Props(this.game);

  final SpikeGame game;

  static Paint _index(int index) => Paint()
    ..color = Color.fromARGB(255, index * 4, 0, 0)
    ..isAntiAlias = false;
  final _log = _index(34), _flame = _index(35), _core = _index(36), _ash = _index(42);

  @override
  void render(Canvas canvas) {
    canvas.drawRect(Rect.fromLTWH(firePos.x - 6, bankY - 2, 12, 2), _log);
    if (!game.fireLit) {
      // Dormant: the logs stay, under a little ash.
      canvas.drawRect(Rect.fromLTWH(firePos.x - 4, bankY - 3, 8, 1), _ash);
      canvas.drawRect(Rect.fromLTWH(firePos.x - 2, bankY - 4, 4, 1), _ash);
      return;
    }
    final tall = (game.elapsed * 8).floor().isEven ? 8.0 : 6.0;
    canvas.drawRect(Rect.fromLTWH(firePos.x - 3, bankY - 2 - tall, 6, tall), _flame);
    canvas.drawRect(Rect.fromLTWH(firePos.x - 1, bankY - 6, 2, 4), _core);
  }
}

/// Meters and the one-line reason, drawn in ordinary colours on the art-pixel grid, after the shader.
/// Three rows of five icons, filled or left as a dark shape: no numbers, no bars, no panel.
class Hud extends Component {
  Hud(this.game, this.sheet, this.widths);

  final SpikeGame game;
  final ui.Image sheet;
  final List<int> widths;

  static const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,'!?-:";
  static const wrap = 104, pitch = 10.0; // widest line of text and distance between lines, in art pixels
  static const metersTop = 10.0;
  static const _cream = Color(0xFFFAF0D6), _ink = Color(0xFF2C2438);
  final _paint = Paint()
    ..filterQuality = FilterQuality.none
    ..isAntiAlias = false;

  List<String> lines = [];
  double left = 0; // seconds the bubble stays up

  /// Width of each glyph, read from the sheet: glyphs sit left-aligned in 6x10 cells from row 8 down.
  static Future<List<int>> measure(ui.Image sheet) async {
    final data = (await sheet.toByteData())!;
    return [
      for (var i = 0; i < chars.length; i++)
        [
          for (var x = 0; x < 6; x++)
            for (var y = 0; y < 10; y++)
              if (data.getUint8(((8 + i ~/ 16 * 10 + y) * sheet.width + i % 16 * 6 + x) * 4 + 3) > 0) x + 1,
        ].fold(0, max),
    ];
  }

  int _width(String text) => text.split('').fold(0, (w, ch) => w + (ch == ' ' ? 3 : widths[chars.indexOf(ch)] + 1)) - 1;

  void say(String sentence) {
    lines = [];
    for (final word in sentence.split(' ')) {
      if (lines.isNotEmpty && _width('${lines.last} $word') <= wrap) {
        lines.last = '${lines.last} $word';
      } else {
        lines.add(word);
      }
    }
    left = 6;
  }

  /// The heart after petting. The scene below is palette numbers, where "half transparent" has no
  /// meaning, so the heart is drawn up here in a real colour: it rises on whole pixels and fades out.
  void _heart(Canvas canvas) {
    final since = game.elapsed - game.dog.lovedAt;
    if (since < 0 || since >= 1.6) return;
    final fade = since < 0.4 ? 1.0 : 1 - (since - 0.4) / 1.2;
    final paint = Paint()
      ..color = const Color(0xFFEE8096).withValues(alpha: fade)
      ..isAntiAlias = false;
    final hx = dogX + 13 - game.camLeft.roundToDouble();
    final hy = bankY - 24 - (since * 8).floorToDouble() - (worldH - game.fit.viewH);
    const rows = ['xx.xx', 'xxxxx', '.xxx.', '..x..'];
    for (var r = 0; r < 4; r++) {
      for (var c = 0; c < 5; c++) {
        if (rows[r][c] == 'x') canvas.drawRect(Rect.fromLTWH(hx + c, hy + r, 1, 1), paint);
      }
    }
  }

  @override
  void update(double dt) => left -= dt;

  @override
  void render(Canvas canvas) {
    canvas.save();
    canvas.scale(game.canvasSize.x / game.viewW); // one unit is one art pixel
    final levels = meterSets[game.hold % meterSets.length];
    for (var m = 0; m < 3; m++) {
      for (var i = 0; i < 5; i++) {
        final src = Rect.fromLTWH(m * 14.0 + (i < levels[m] ? 0 : 7), 0, 7, 7);
        canvas.drawImageRect(sheet, src, Rect.fromLTWH(4 + i * 8.0, metersTop + m * 9, 7, 7), _paint);
      }
    }
    if (left > 0) {
      _bubble(canvas);
    }
    _heart(canvas);
    canvas.restore();
  }

  /// A speech bubble above the character, kept inside the view; its tail follows the character.
  void _bubble(Canvas canvas) {
    final origin = game.camera.viewfinder.position;
    final w = lines.map(_width).fold(0, max) + 8.0, h = lines.length * pitch + 5;
    final tail = (game.hero.x.floorToDouble() - origin.x).clamp(8.0, game.viewW - 8);
    final x = (tail - w / 2).floorToDouble().clamp(2.0, game.viewW - 2 - w);
    final y = bankY - 36 - origin.y - h;
    void box(double inset, Color colour) {
      _paint.color = colour;
      canvas.drawRect(Rect.fromLTWH(x + inset + 1, y + inset, w - inset * 2 - 2, h - inset * 2), _paint);
      canvas.drawRect(Rect.fromLTWH(x + inset, y + inset + 1, w - inset * 2, h - inset * 2 - 2), _paint);
    }

    box(0, _ink);
    box(1, _cream);
    _paint.color = _ink;
    canvas.drawRect(Rect.fromLTWH(tail - 2, y + h - 1, 5, 2), _paint);
    canvas.drawRect(Rect.fromLTWH(tail - 1, y + h + 1, 3, 1), _paint);
    canvas.drawRect(Rect.fromLTWH(tail, y + h + 2, 1, 1), _paint);
    _paint.color = _cream;
    canvas.drawRect(Rect.fromLTWH(tail - 1, y + h - 1, 3, 2), _paint);
    canvas.drawRect(Rect.fromLTWH(tail, y + h + 1, 1, 1), _paint);
    _paint.color = const Color(0xFFFFFFFF);
    for (var l = 0; l < lines.length; l++) {
      var cx = x + 4;
      for (final ch in lines[l].split('')) {
        if (ch == ' ') {
          cx += 3;
          continue;
        }
        final i = chars.indexOf(ch), gw = widths[i].toDouble();
        final src = Rect.fromLTWH(i % 16 * 6.0, 8 + i ~/ 16 * 10.0, gw, 9);
        canvas.drawImageRect(sheet, src, Rect.fromLTWH(cx, y + 3 + l * pitch, gw, 9), _paint);
        cx += gw + 1;
      }
    }
  }
}
