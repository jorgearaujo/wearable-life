#!/usr/bin/env python3
"""Turns a pulled log into a fixture that is safe to keep in the repo.

Usage: scripts/anonymize.py <raw folder> <fixture name>
Writes to <repo>/fixtures/<fixture name>/.

What changes:
- every timestamp moves back by the same random number of whole weeks (weekday and clock time are kept)
- record IDs become r1, r2, ...; client record IDs are dropped
- device manufacturer and model, phone model and time zone name are dropped
- the per-device ID at the end of the phone's own package name becomes `device`
What stays: app package names, device type, zone offsets, and the health values themselves.
"""
import json
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

INSTANT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z")
# On-device steps are written under a package name that ends in a per-device ID.
PHONE_ORIGIN = re.compile(r"(com\.android\.healthconnect\.phone)\.[0-9a-z]+")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    raw = Path(sys.argv[1])
    out = Path(__file__).resolve().parents[3] / "fixtures" / sys.argv[2]
    out.mkdir(parents=True, exist_ok=True)
    shift = timedelta(weeks=random.SystemRandom().randint(60, 400))
    ids = {}

    def shift_instant(match):
        text = match.group(0)
        moved = datetime.fromisoformat(text.replace("Z", "+00:00")) - shift
        fraction = text[19:-1]  # keep the original sub-second digits as written
        return moved.strftime("%Y-%m-%dT%H:%M:%S") + fraction + "Z"

    def new_id(old):
        return ids.setdefault(old, f"r{len(ids) + 1}")

    def clean(entry):
        entry.pop("zone", None)
        entry.pop("phone", None)
        if "id" in entry:
            entry["id"] = new_id(entry["id"])
        meta = entry.get("meta")
        if meta:
            meta["id"] = new_id(meta["id"])
            meta.pop("clientRecordId", None)
            meta.pop("clientRecordVersion", None)
            if "device" in meta:
                meta["device"] = {"type": meta["device"].get("type")}
        return entry

    for name in ("observations.jsonl", "runs.jsonl"):
        count = 0
        with open(raw / name) as src, open(out / name, "w") as dst:
            for line in src:
                if not line.strip():
                    continue
                cleaned = json.dumps(clean(json.loads(line)), separators=(",", ":"))
                cleaned = PHONE_ORIGIN.sub(r"\1.device", cleaned)
                dst.write(INSTANT.sub(shift_instant, cleaned) + "\n")
                count += 1
        print(f"{out / name}: {count} lines")


if __name__ == "__main__":
    main()
