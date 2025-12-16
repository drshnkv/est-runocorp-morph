#!/bin/bash
# Assemble poems_index_v3.json.gz from split parts
# Usage: ./assemble.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Assembling poems_index_v3.json.gz from split parts..."

# Combine parts
cat poems_index_v3.json.gz.aa poems_index_v3.json.gz.ab poems_index_v3.json.gz.ac > ../poems_index_v3.json.gz

# Verify checksum if available
if [ -f checksum.md5 ]; then
    echo "Verifying checksum..."
    cd ..
    if md5 -q poems_index_v3.json.gz | grep -q "$(cat poems_index_v3/checksum.md5 | cut -d' ' -f1)"; then
        echo "Checksum verified: OK"
    else
        echo "WARNING: Checksum mismatch!"
        exit 1
    fi
    cd poems_index_v3
fi

# Verify gzip integrity
echo "Verifying gzip integrity..."
gunzip -t ../poems_index_v3.json.gz
echo "Gzip integrity: OK"

echo ""
echo "Successfully assembled: ../poems_index_v3.json.gz"
echo "To decompress: gunzip -k ../poems_index_v3.json.gz"
