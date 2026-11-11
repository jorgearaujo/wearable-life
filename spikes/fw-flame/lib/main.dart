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

/// Tap to step through these; "cycle" runs a whole day in [cycleSeconds].
const holds = <(String, double)>[('cycle', -1), ('night', 0), ('dawn', 0.27), ('day', 0.5), ('dusk', 0.74)];

/// Palette rows: 0 night, 1 dawn, 2 day, 3 dusk. Each key is (time of day, row); between keys the two
/// rows are mixed, so day and night hold steady and dawn and dusk pass through.
const paletteKeys = <(double, double)>[(0, 0), (0.2, 0), (0.27, 1), (0.36, 2), (0.64, 2), (0.74, 3), (0.82, 0), (1, 0)];
const rowDarkness = [1.0, 0.5, 0.0, 0.6];

final hudText = ValueNotifier('...');

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
              children: [
                GameWidget(game: SpikeGame(program, fit, palette)),
                // Debug text sits outside the game: inside it, the shader would read it as palette indices.
                Padding(
                  padding: const EdgeInsets.fromLTRB(12, 48, 0, 0),
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
  int hold = 0;

  final ui.FragmentProgram program;
  late final GradePostProcess grade;
  final layers = <(SpriteComponent, double)>[];

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
    }
    world.add(
      SpriteAnimationComponent.fromFrameData(
        await images.load('character.png'),
        SpriteAnimationData.sequenced(amount: 4, stepTime: 0.25, textureSize: Vector2(16, 30)),
        position: Vector2(112, bankY),
        anchor: Anchor.bottomCenter,
      ),
    );
    world.add(Props(this));

    camera = CameraComponent.withFixedResolution(width: viewW, height: viewH, world: world);
    camera.viewfinder.anchor = Anchor.topLeft;
    // Anchored to the bottom, so the water is always in view and a taller screen shows more sky.
    camera.viewfinder.position = Vector2(camLeft, worldH - viewH);
    grade = GradePostProcess(program, palette);
    camera.postProcess = grade;
    _pan(0);
  }

  @override
  void onTap() => hold = (hold + 1) % holds.length;

  @override
  void update(double dt) {
    super.update(dt);
    elapsed += dt;
    worstMs = max(worstMs, dt * 1000.0); // frame-to-frame gap, same measure as the Godot spike
    sinceTouch += dt;
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
      ..dark = rowDarkness[rowA.toInt()] * (1 - mix) + rowDarkness[rowB.toInt()] * mix;
    // Flicker in steps, about 8 times a second, so the glow jumps like pixel art and does not pulse smoothly.
    final step = (elapsed * 8).floor();
    final flicker = 0.85 + 0.15 * sin(step * 12.9898).abs();
    final origin = camera.viewfinder.position;
    grade
      ..step = step.toDouble()
      ..waterline = waterY - origin.y;
    grade.lights[0].setValues(firePos.x - origin.x, firePos.y - origin.y, 40 * flicker, 1);
    grade.lights[1].setValues(windowPos.x - origin.x, windowPos.y - origin.y, 20, 0.67);
    if (sinceTouch > 3) {
      _pan(autoDir * 12 * dt);
    }

    frames++;
    window += dt;
    if (frames % 30 == 0) {
      fps = 30 / window;
      window = 0;
      hudText.value = '${fps.round()} fps  worst ${worstMs.round()} ms\n'
          'view ${viewW.round()}x${fit.viewH.round()}  ${holds[hold].$1} (tap to change)';
      worstMs = 0;
    }
  }

  @override
  void onPanUpdate(DragUpdateInfo info) {
    sinceTouch = 0;
    _pan(-info.delta.global.x / (size.x / viewW));
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
class GradePostProcess extends PostProcess {
  GradePostProcess(ui.FragmentProgram program, this.palette) : shader = program.fragmentShader(), super(pixelRatio: 1);

  final ui.FragmentShader shader;
  final ui.Image palette;
  double rowA = 2, rowB = 2, mix = 0, dark = 0, waterline = 0, step = 0;

  /// x, y in view pixels, radius in art pixels, strength 0 to 1.
  final lights = [Vector4.zero(), Vector4.zero()];

  @override
  void postProcess(Vector2 size, Canvas canvas) {
    final scene = rasterizeSubtree();
    var i = 0;
    for (final v in [size.x, size.y, scene.width.toDouble(), scene.height.toDouble(), rowA, rowB, mix, dark, waterline, step]) {
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
    scene.dispose();
  }
}

/// Placeholder campfire, drawn as rectangles in palette-index colours (red = index * 4).
class Props extends Component {
  Props(this.game);

  final SpikeGame game;

  static Paint _index(int index) => Paint()
    ..color = Color.fromARGB(255, index * 4, 0, 0)
    ..isAntiAlias = false;
  final _log = _index(34), _flame = _index(35), _core = _index(36);

  @override
  void render(Canvas canvas) {
    canvas.drawRect(Rect.fromLTWH(firePos.x - 6, bankY - 2, 12, 2), _log);
    final tall = (game.elapsed * 8).floor().isEven ? 8.0 : 6.0;
    canvas.drawRect(Rect.fromLTWH(firePos.x - 3, bankY - 2 - tall, 6, tall), _flame);
    canvas.drawRect(Rect.fromLTWH(firePos.x - 1, bankY - 6, 2, 4), _core);
  }
}
