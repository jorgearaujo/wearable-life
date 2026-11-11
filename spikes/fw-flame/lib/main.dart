import 'dart:math';
import 'dart:ui' as ui;

import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/post_process.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health/health.dart';

const worldW = 360.0;
const worldH = 480.0;
const baseW = 180.0;
const cycleSeconds = 24.0;

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
  String stepsText = 'steps: reading';

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
      final layer = SpriteComponent(sprite: await loadSprite('$name.png'));
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

    _readSteps();
  }

  @override
  void update(double dt) {
    super.update(dt);
    elapsed += dt;
    worstMs = max(worstMs, dt * 1000.0); // frame-to-frame gap, same measure as the Godot spike
    sinceTouch += dt;
    grade.timeOfDay = (elapsed / cycleSeconds) % 1.0;
    if (sinceTouch > 3) {
      _pan(autoDir * 12 * dt);
    }

    frames++;
    window += dt;
    if (frames % 30 == 0) {
      fps = 30 / window;
      window = 0;
      hud.text = '${fps.round()} fps  worst ${worstMs.round()} ms\n$stepsText\n'
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

  Future<void> _readSteps() async {
    try {
      final health = Health();
      await health.configure();
      if (await health.hasPermissions([HealthDataType.STEPS]) != true) {
        stepsText = 'steps: no permission';
        return;
      }
      final now = DateTime.now();
      final total = await health.getTotalStepsInInterval(DateTime(now.year, now.month, now.day), now);
      stepsText = 'steps: ${total ?? 0}';
    } catch (e) {
      stepsText = 'steps: ${e.runtimeType}';
    }
  }
}

/// Renders the world into a low-resolution image, then draws it through the grade shader.
class GradePostProcess extends PostProcess {
  GradePostProcess(ui.FragmentProgram program) : shader = program.fragmentShader(), super(pixelRatio: 1);

  final ui.FragmentShader shader;
  double timeOfDay = 0.5;

  @override
  void postProcess(Vector2 size, Canvas canvas) {
    final scene = rasterizeSubtree();
    shader
      ..setFloat(0, size.x)
      ..setFloat(1, size.y)
      ..setFloat(2, scene.width.toDouble())
      ..setFloat(3, scene.height.toDouble())
      ..setFloat(4, timeOfDay)
      ..setImageSampler(0, scene);
    canvas.drawRect(Offset.zero & size.toSize(), Paint()..shader = shader);
    scene.dispose();
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
