import 'package:fw_flame/daylight.dart';
import 'package:test/test.dart';

void main() {
  test('midnight is dark', () => expect(sunHeight(0), closeTo(0, 1e-9)));
  test('noon is bright', () => expect(sunHeight(0.5), closeTo(1, 1e-9)));
  test('dawn is half', () => expect(sunHeight(0.25), closeTo(0.5, 1e-9)));
}
