#!/bin/bash
# Reassemble poems_index_v2.json.gz from split parts
#
# Usage: ./assemble.sh
# Output: ../poems_index_v2.json.gz

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_FILE="$SCRIPT_DIR/../poems_index_v2.json.gz"

echo "=== Reassembling poems_index_v2.json.gz ==="
echo "Working directory: $SCRIPT_DIR"

# Count parts
PARTS=$(ls "$SCRIPT_DIR"/poems_index_v2.json.gz.* 2>/dev/null | wc -l | tr -d ' ')
echo "Found $PARTS parts"

if [ "$PARTS" -eq 0 ]; then
    echo "ERROR: No parts found matching poems_index_v2.json.gz.*"
    exit 1
fi

# Concatenate parts
echo "Concatenating parts..."
cat "$SCRIPT_DIR"/poems_index_v2.json.gz.* > "$OUTPUT_FILE"

# Verify gzip integrity
echo "Verifying gzip integrity..."
if gzip -t "$OUTPUT_FILE" 2>/dev/null; then
    echo "✓ gzip integrity check PASSED"
else
    echo "✗ ERROR: gzip integrity check FAILED"
    rm -f "$OUTPUT_FILE"
    exit 1
fi

# Check MD5 if checksum file exists
if [ -f "$SCRIPT_DIR/checksum.md5" ]; then
    echo ""
    echo "Verifying MD5 checksum..."
    EXPECTED_MD5=$(cat "$SCRIPT_DIR/checksum.md5" | awk '{print $NF}')
    ACTUAL_MD5=$(md5 -q "$OUTPUT_FILE" 2>/dev/null || md5sum "$OUTPUT_FILE" | awk '{print $1}')

    if [ "$EXPECTED_MD5" = "$ACTUAL_MD5" ]; then
        echo "✓ MD5 checksum PASSED: $ACTUAL_MD5"
    else
        echo "✗ ERROR: MD5 checksum FAILED"
        echo "  Expected: $EXPECTED_MD5"
        echo "  Actual:   $ACTUAL_MD5"
        exit 1
    fi
fi

# Report file size
SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
echo ""
echo "=== Assembly Complete ==="
echo "Output: $OUTPUT_FILE"
echo "Size: $SIZE"
