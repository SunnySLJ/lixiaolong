#!/bin/bash
# gif.sh - 视频转GIF
# Usage: gif.sh input.mp4 --start 10 --duration 3 --fps 15 --width 480

INPUT="$1"
[ -z "$INPUT" ] && { echo "用法: gif.sh <视频> [选项]"; exit 1; }

START=""
DURATION=""
FPS=15
WIDTH=480

shift
while [[ $# -gt 0 ]]; do
  case $1 in
    --start|-s) START="$2"; shift 2 ;;
    --duration|-d) DURATION="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --width|-w) WIDTH="$2"; shift 2 ;;
    *) shift ;;
  esac
done

OUTPUT="${INPUT%.*}.gif"

OPTS=""
[ -n "$START" ] && OPTS="$OPTS -ss $START"
[ -n "$DURATION" ] && OPTS="$OPTS -t $DURATION"

echo "[GIF生成] FPS: $FPS | 宽度: ${WIDTH}px"
ffmpeg -i "$INPUT" $OPTS -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" "$OUTPUT"
echo "✓ GIF已生成: $OUTPUT"
