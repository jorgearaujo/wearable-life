import 'dart:math';
import 'dart:ui' as ui;

import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/post_process.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

const worldW = 360.0;
const worldH = 480.0;
const baseW = 180.0;
const cycleSeconds = 24.0;

/// Set with --dart-define=FIXED_TIME=0 to hold one time of day, in thousandths (0 = midnight, 500 = noon).
const fixedTime = int.fromEnvironment('FIXED_TIME', defaultValue: -1);

/// LIGHTS=off draws the plain grade; LIGHTS=nomask lights everything in range, sky included.
const lightsMode = String.fromEnvironment('LIGHTS', defaultValue: 'mask');

// Light sources in world (art pixel) coordinates.
final firePos = Vector2(196, 372);
final windowPos = Vector2(100, 358); // the cabin window already in ground.png

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  final program = await ui.FragmentProgram.fromAsset('shaders/grade.frag');
  // Give the game a box that is an exact whole multiple of the art size in physical pixels,
  // centred on a physical pixel. Without this, screens that 180 does not divide get uneven pixels.
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
            child: GameWidget(game: SpikeGame(program, fit)),
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

class SpikeGame extends FlameGame with PanDetector {
  SpikeGame(this.program, this.fit);

  final PixelFit fit;

  final ui.FragmentProgram program;
  late final GradePostProcess grade;
  late final TextComponent hud;
  final layers = <(SpriteComponent, double)>[];

  double camLeft = 90;
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
    // Integer scaling: the largest whole number of physical pixels per art pixel that fits 180 across.
    viewW = fit.viewW;
    final viewH = fit.viewH;

    for (final (name, factor) in [('sky', 0.0), ('hills', 0.3), ('trees', 0.6), ('ground', 1.0)]) {
      final layer = Layer(this, await loadSprite('$name.png'), lit: factor >= 0.6);
      layers.add((layer, factor));
      world.add(layer);
    }
    world.add(
      SpriteAnimationComponent.fromFrameData(
        await images.load('character.png'),
        SpriteAnimationData.sequenced(amount: 4, stepTime: 0.25, textureSize: Vector2(16, 24)),
        position: Vector2(150, 368),
        anchor: Anchor.center,
      ),
    );
    world.add(Props(this));
    world.add(Rain(this, await images.load('drop.png')));

    camera = CameraComponent.withFixedResolution(width: viewW, height: viewH, world: world);
    camera.viewfinder.anchor = Anchor.topLeft;
    camera.viewfinder.position = Vector2(camLeft, (worldH - viewH) / 2);
    grade = GradePostProcess(program);
    camera.postProcess = grade;

    hud = TextComponent(
      text: '...',
      position: Vector2(3, 24),
      textRenderer: TextPaint(style: const TextStyle(fontSize: 8, color: Color(0xFFFFFFFF))),
    );
    camera.viewport.add(hud);

  }

  @override
  void update(double dt) {
    super.update(dt);
    elapsed += dt;
    worstMs = max(worstMs, dt * 1000.0); // frame-to-frame gap, same measure as the Godot spike
    sinceTouch += dt;
    grade.timeOfDay = fixedTime >= 0 ? fixedTime / 1000 : (elapsed / cycleSeconds) % 1.0;
    // Flicker in steps, about 8 times a second, so the glow jumps like pixel art and does not pulse smoothly.
    final step = (elapsed * 8).floor();
    final flicker = 0.85 + 0.15 * sin(step * 12.9898).abs();
    final origin = camera.viewfinder.position;
    grade.lights[0].setValues(firePos.x - origin.x, firePos.y - origin.y, 46 * flicker, lightsMode == 'off' ? 0 : 1);
    grade.lights[1].setValues(windowPos.x - origin.x, windowPos.y - origin.y, 26, lightsMode == 'off' ? 0 : 0.8);
    if (sinceTouch > 3) {
      _pan(autoDir * 12 * dt);
    }

    frames++;
    window += dt;
    if (frames % 30 == 0) {
      fps = 30 / window;
      window = 0;
      hud.text = '${fps.round()} fps  worst ${worstMs.round()} ms\n'
          'view ${viewW.round()}x${camera.viewport.virtualSize.y.round()}';
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

/// Renders the world into a low-resolution image, then draws it through the grade shader.
/// A second low-resolution image, the light mask, holds only the layers that lights may reach.
class GradePostProcess extends PostProcess {
  GradePostProcess(ui.FragmentProgram program) : shader = program.fragmentShader(), super(pixelRatio: 1);

  final ui.FragmentShader shader;
  double timeOfDay = 0.5;
  bool maskPass = false;

  /// x, y in view pixels, radius in art pixels, strength 0 to 1.
  final lights = [Vector4.zero(), Vector4.zero()];

  @override
  void postProcess(Vector2 size, Canvas canvas) {
    final scene = rasterizeSubtree();
    maskPass = lightsMode == 'mask';
    final mask = maskPass ? rasterizeSubtree() : scene;
    maskPass = false;
    shader
      ..setFloat(0, size.x)
      ..setFloat(1, size.y)
      ..setFloat(2, scene.width.toDouble())
      ..setFloat(3, scene.height.toDouble())
      ..setFloat(4, timeOfDay);
    var i = 5;
    for (final l in lights) {
      shader
        ..setFloat(i++, l.x)
        ..setFloat(i++, l.y)
        ..setFloat(i++, l.z)
        ..setFloat(i++, l.w);
    }
    shader
      ..setImageSampler(0, scene)
      ..setImageSampler(1, mask);
    canvas.drawRect(Offset.zero & size.toSize(), Paint()..shader = shader);
    if (!identical(mask, scene)) {
      mask.dispose();
    }
    scene.dispose();
  }
}

/// A parallax layer. Far layers (sky, hills) are skipped while the light mask is drawn.
class Layer extends SpriteComponent {
  Layer(this.game, Sprite sprite, {required this.lit}) : super(sprite: sprite);

  final SpikeGame game;
  final bool lit;

  @override
  void render(Canvas canvas) {
    if (game.grade.maskPass && !lit) {
      return;
    }
    super.render(canvas);
  }
}

/// Placeholder campfire, drawn as rectangles so the spike needs no new art.
class Props extends Component {
  Props(this.game);

  final SpikeGame game;

  static Paint _c(int argb) => Paint()..color = Color(argb);
  final _log = _c(0xFF4A3222), _flame = _c(0xFFFF8A2A), _core = _c(0xFFFFE27A);

  @override
  void render(Canvas canvas) {
    canvas.drawRect(Rect.fromLTWH(firePos.x - 6, firePos.y + 6, 12, 2), _log);
    final tall = (game.elapsed * 8).floor().isEven ? 7.0 : 5.0;
    canvas.drawRect(Rect.fromLTWH(firePos.x - 3, firePos.y + 6 - tall, 6, tall), _flame);
    canvas.drawRect(Rect.fromLTWH(firePos.x - 1, firePos.y + 3, 2, 3), _core);
  }
}

/// Rain written by hand: 140 drops recycled in a band that follows the camera.
class Rain extends Component {
  Rain(this.game, this.drop);

  final SpikeGame game;
  final ui.Image drop;
  final _random = Random(7);
  late final List<Vector2> drops = List.generate(140, (_) => Vector2(_random.nextDouble() * 440, _random.nextDouble() * 600));
  final _paint = Paint();

  @override
  void update(double dt) {
    for (final d in drops) {
      d.y += 240 * dt;
      d.x -= 36 * dt;
      if (d.y > 600) {
        d.y -= 600;
        d.x = _random.nextDouble() * 440;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    final left = game.camLeft.roundToDouble() - 20;
    for (final d in drops) {
      canvas.drawImage(drop, Offset(left + d.x.roundToDouble(), d.y.roundToDouble() - 60), _paint);
    }
  }
}
