#!/bin/sh
# Copies the logger's two files from the phone (USB, debug build) into a git-ignored folder.
# Usage: scripts/pull.sh            (run from spikes/hc-logger)
set -eu
cd "$(dirname "$0")/.."
PKG=dev.wearablelife.hclogger
OUT="data/raw/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
for f in observations.jsonl runs.jsonl; do
  adb exec-out run-as "$PKG" cat "files/$f" > "$OUT/$f"
  echo "$OUT/$f: $(wc -l < "$OUT/$f" | tr -d ' ') lines"
done
