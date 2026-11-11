import 'dart:math';

/// Stand-in for "pure logic": plain Dart, no Flutter or Flame imports. 0 = midnight, 0.5 = noon.
double sunHeight(double timeOfDay) => 0.5 - 0.5 * cos(timeOfDay * 2 * pi);
