#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OUT="$(cd .. && pwd)"
mkdir -p "$OUT/frames"
# 1080 x 1920, 900 frames, 30 fps. Preview: SCALE=25 STEP=10 then encode at 3 fps.
blender -b -t 3 -P build.py
python3 finish.py audio
python3 finish.py video "$OUT/frames" "$OUT/silent.mp4" 30
ffmpeg -y -i "$OUT/silent.mp4" -i "$OUT/sound_effects.wav" -c:v copy -c:a aac -b:a 256k -movflags +faststart "$OUT/complete.mp4"
blender -b -t 3 -P bake.py
