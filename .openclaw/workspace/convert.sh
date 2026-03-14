#!/bin/bash
# convert.sh - 视频格式转换/压缩
# Usage: convert.sh input.mp4 [options]

INPUT="$1"
[ -z "$INPUT" ] && { echo "用法: convert.sh <视频> [选项]"; exit 1; }

QUALITY="medium"  # low, medium, high
FORMAT="mp4"
RESOLUTION=""

shift
while [[ $# -gt 0 ]]; do
  case $1 in
    --quality|-q)
      QUALITY="$2"
      shift 2
      ;;
    --format|-f)
      FORMAT="$2"
      shift 2
      ;;
    --resolution|-r)
      RESOLUTION="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Set encoding parameters based on quality
case $QUALITY in
  low)
    CRF=28
    PRESET="superfast"
    ;;
  high)
    CRF=18
    PRESET="slow"
    ;;
  *)
    CRF=23
    PRESET="fast"
    ;;
esac

OUTPUT="${INPUT%.*}_converted.${FORMAT}"

FFMPEG_OPTS="-i \"$INPUT\" -c:v libx264 -preset $PRESET -crf $CRF -c:a aac -b:a 128k"

[ -n "$RESOLUTION" ] && FFMPEG_OPTS="$FFMPEG_OPTS -vf scale=$RESOLUTION:force_original_aspect_ratio=decrease"

echo "[视频转换] 质量: $QUALITY | 格式: $FORMAT"
eval "ffmpeg $FFMPEG_OPTS \"$OUTPUT\""
echo "✓ 转换完成: $OUTPUT"
