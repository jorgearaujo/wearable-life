#!/usr/bin/env python3
"""Summarizes a pulled log: what each app writes to Health Connect, and how late.

Usage: scripts/summarize.py [folder]     (default: newest folder in data/raw/)

Prints counts and delays only, never health values.
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def read(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def minutes(a, b):
    return (b - a).total_seconds() / 60


def pct(values, p):
    values = sorted(values)
    return values[min(len(values) - 1, int(len(values) * p))]


def fmt(mins):
    if mins >= 2880:
        return f"{mins / 1440:.1f}d"
    if mins >= 120:
        return f"{mins / 60:.1f}h"
    return f"{mins:.0f}m"


def delays(values):
    if not values:
        return "-"
    return f"{fmt(pct(values, 0.5))} / {fmt(pct(values, 0.9))} / {fmt(max(values))}"


def main():
    root = Path(__file__).resolve().parent.parent / "data" / "raw"
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else max(p for p in root.iterdir() if p.is_dir())
    runs = read(folder / "runs.jsonl")
    obs = read(folder / "observations.jsonl")
    print(f"Folder: {folder}")

    # --- Polls ---
    print(f"\nPolls: {len(runs)}, from {runs[0]['at']} to {runs[-1]['at']}")
    print("  by trigger:", dict(Counter(r["trigger"] for r in runs)))
    times = [parse(r["at"]) for r in runs]
    gaps = [minutes(a, b) for a, b in zip(times, times[1:])]
    if gaps:
        print(f"  gap between polls (median / p90 / max): {delays(gaps)}")
        print(f"  gaps over 1 hour: {sum(g > 60 for g in gaps)}")
    last = runs[-1]
    print("  features:", last.get("features"))
    print("  alarm set at poll time:", f"{sum(r.get('nextAlarm') is not None for r in runs)} of {len(runs)} polls")
    errors = Counter()
    skipped = {}
    for r in runs:
        if r.get("error"):
            errors[f"poll ({r['trigger']}): {r['error']}"] += 1
        for name, t in (r.get("types") or {}).items():
            if t.get("error"):
                errors[f"{name} ({r['trigger']}): {t['error']}"] += 1
    for name, t in (last.get("types") or {}).items():
        if t.get("skipped"):
            skipped[name] = t["skipped"]
    if skipped:
        print("  skipped in last poll:", skipped)
    for message, count in errors.most_common():
        print(f"  ERROR x{count}: {message}")

    # --- Records per app and type ---
    groups = defaultdict(lambda: {"ids": defaultdict(set), "write": [], "seen": [], "first": None, "last": None, "devices": set(), "methods": Counter()})
    deletes = Counter()
    for o in obs:
        if o["op"] == "delete":
            deletes[o["type"]] += 1
            continue
        meta, data = o["meta"], o["data"]
        g = groups[(meta["origin"], o["type"])]
        g["ids"][meta["id"]].add(meta["lastModified"])
        g["methods"][meta["recordingMethod"]] += 1
        device = meta.get("device")
        if device:
            g["devices"].add(f"{device.get('manufacturer')} {device.get('model')} (type {device.get('type')})")
        end = parse(data.get("end") or data["time"])
        g["first"] = min(g["first"] or end, end)
        g["last"] = max(g["last"] or end, end)
        if o["via"] == "change":  # backfilled records say nothing about delay
            modified = parse(meta["lastModified"])
            g["write"].append(max(0.0, minutes(end, modified)))
            g["seen"].append(max(0.0, minutes(modified, parse(o["seenAt"]))))

    print("\nRecords per app and type")
    print("  write delay = record end -> written to Health Connect; seen delay = written -> read by the logger")
    print("  delays are median / p90 / max, live records only\n")
    header = f"  {'app':38} {'type':26} {'records':>8} {'rewritten':>9}  {'write delay':22} {'seen delay':22} data from..to"
    print(header)
    for (origin, type_name), g in sorted(groups.items()):
        rewritten = sum(len(v) > 1 for v in g["ids"].values())
        span = f"{g['first']:%Y-%m-%d}..{g['last']:%Y-%m-%d}"
        print(f"  {origin[:38]:38} {type_name:26} {len(g['ids']):>8} {rewritten:>9}  {delays(g['write']):22} {delays(g['seen']):22} {span}")
    print("\nDevices and recording methods per app (method: 0 unknown, 1 active, 2 automatic, 3 manual)")
    by_origin = defaultdict(lambda: (set(), Counter()))
    for (origin, _), g in groups.items():
        by_origin[origin][0].update(g["devices"])
        by_origin[origin][1].update(g["methods"])
    for origin, (devices, methods) in sorted(by_origin.items()):
        print(f"  {origin}: {sorted(devices) or 'no device info'}; methods {dict(methods)}")
    if deletes:
        print("\nDeletions seen:", dict(deletes))

    # --- Sleep stages ---
    sleep = [o for o in obs if o["op"] == "upsert" and o["type"] == "SleepSession"]
    if sleep:
        print("\nSleep sessions with stage detail, per app (stage codes: 1 awake, 4 light, 5 deep, 6 REM)")
        per = defaultdict(lambda: [0, 0, Counter()])
        for o in {o["meta"]["id"]: o for o in sleep}.values():
            entry = per[o["meta"]["origin"]]
            entry[0] += 1
            stages = o["data"].get("stages") or []
            entry[1] += bool(stages)
            entry[2].update(s[2] for s in stages)
        for origin, (total, with_stages, codes) in sorted(per.items()):
            print(f"  {origin}: {with_stages} of {total} sessions have stages; codes used {sorted(codes)}")


if __name__ == "__main__":
    main()
