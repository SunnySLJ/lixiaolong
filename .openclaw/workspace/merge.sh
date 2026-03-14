#!/bin/bash
# merge.sh - 合并多个视频
# Usage: merge.sh file1.mp4 file2.mp4 ... --output merged.mp4

OUTPUT="merged.mp4"
FILES=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --output|-o)
      OUTPUT="$2"
      shift 2
      ;;
    *)
      FILES+=("$1")
      shift
      ;;
  esac
done

if [ ${#FILES[@]} -eq 0 ]; then
  echo "用法: merge.sh <视频1> <视频2> ... --output 输出.mp4"
  exit 1
fi

# Create temp file list
TEMP_LIST=$(mktemp)
for f in "${FILES[@]}"; do
  echo "file '$f'" >> "$TEMP_LIST"
done

echo "[视频合并] 正在合并 ${#FILES[@]} 个视频..."
ffmpeg -f concat -safe 0 -i "$TEMP_LIST" -c copy "$OUTPUT"

rm "$TEMP_LIST"
echo "✓ 合并完成: $OUTPUT"
