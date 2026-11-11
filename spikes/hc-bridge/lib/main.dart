import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

/// Spike screen: everything about health goes through one platform channel to our own Kotlin.
const _health = MethodChannel('wearablelife/health');

void main() => runApp(const MaterialApp(home: BridgeScreen()));

class BridgeScreen extends StatefulWidget {
  const BridgeScreen({super.key});

  @override
  State<BridgeScreen> createState() => _BridgeScreenState();
}

class _BridgeScreenState extends State<BridgeScreen> with WidgetsBindingObserver {
  String status = '...';
  List<Map<String, dynamic>> reads = [];
  List<Map<String, dynamic>> stepDays = [];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _refresh();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) _refresh();
  }

  Future<void> _call(String method) async {
    try {
      await _health.invokeMethod<Object?>(method);
    } on PlatformException catch (e) {
      status = 'error: ${e.message}';
    }
    await _refresh();
  }

  Future<void> _refresh() async {
    try {
      final s = await _health.invokeMapMethod<String, dynamic>('status') ?? {};
      final lines = await _health.invokeListMethod<String>('history') ?? [];
      status = s['available'] == true
          ? 'permissions ${s['granted']} of ${s['wanted']}'
          : 'Health Connect not available';
      reads = [for (final l in lines.reversed) jsonDecode(l) as Map<String, dynamic>];
    } on PlatformException catch (e) {
      status = 'error: ${e.message}';
    }
    if (mounted) setState(() {});
  }

  Future<void> _compareSteps() async {
    try {
      final lines = await _health.invokeListMethod<String>('compareSteps') ?? [];
      stepDays = [for (final l in lines) jsonDecode(l) as Map<String, dynamic>];
    } on PlatformException catch (e) {
      status = 'error: ${e.message}';
    }
    if (mounted) setState(() {});
  }

  /// Ratios only: Health Connect's step total against each source's own total.
  String _stepLine(Map<String, dynamic> d) {
    if (d['error'] != null) return '${d['day']}  error: ${d['error']}';
    if (d['hasSteps'] != true) return '${d['day']}  no steps';
    final sources = (d['sources'] as List).cast<Map<String, dynamic>>();
    return '${d['day']}  sum/total ${d['sumOverTotal']}, largest/total ${d['largestOverTotal']}\n'
        '${[for (final s in sources) '  ${s['name']}: share ${s['shareOfTotal']}'
            '${s['equalsTotal'] == true ? ' (= total)' : ''}, ${s['records']} rec, raw/own ${s['rawOverOwn']}'].join('\n')}';
  }

  /// The whole result on one screen, so it can be read off the phone without pulling a file.
  String _summary() {
    if (reads.isEmpty) return 'no reads stored';
    final times = [for (final r in reads) DateTime.parse(r['at'] as String)]; // newest first
    var longest = Duration.zero;
    for (var i = 0; i + 1 < times.length; i++) {
      final gap = times[i].difference(times[i + 1]);
      if (gap > longest) longest = gap;
    }
    final background = reads.where((r) => r['trigger'] == 'background');
    return 'reads ${reads.length}, background ${background.length}, '
        'without Flutter ${background.where((r) => r['flutterAttached'] == false).length}, '
        'errors ${reads.where((r) => r['error'] != null).length}\n'
        'first ${times.last.toLocal()}\nlast ${times.first.toLocal()}\n'
        'longest gap ${longest.inMinutes} min, since last ${DateTime.now().difference(times.first).inMinutes} min';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(padding: const EdgeInsets.all(12), child: Text('$status\n${_summary()}')),
            Wrap(
              alignment: WrapAlignment.spaceEvenly,
              spacing: 8,
              children: [
                FilledButton(onPressed: () => _call('requestPermissions'), child: const Text('Grant')),
                FilledButton(onPressed: () => _call('readNow'), child: const Text('Read now')),
                OutlinedButton(onPressed: _refresh, child: const Text('Refresh')),
                OutlinedButton(onPressed: _compareSteps, child: const Text('Compare steps')),
              ],
            ),
            Expanded(
              child: ListView(
                children: [
                  if (stepDays.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.all(12),
                      child: Text(stepDays.map(_stepLine).join('\n'), style: const TextStyle(fontSize: 12)),
                    ),
                  for (final r in reads)
                    ListTile(
                      dense: true,
                      title: Text('${r['at']}  ${r['trigger']}'),
                      // Counts of records only; no health values reach this screen.
                      subtitle: Text(
                        r['error'] != null
                            ? 'error: ${r['error']}'
                            : 'records in 24 h: steps ${r['steps']}, sleep ${r['sleep']}, hrv ${r['hrv']}\n'
                                'Flutter running: ${r['flutterAttached']}, process age ${r['processAgeS']} s, '
                                '${r['durationMs']} ms',
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
