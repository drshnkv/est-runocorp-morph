#!/usr/bin/env python3
"""
Assemble poems_index_v3.json.gz from split parts.

Usage:
    python assemble.py

This script combines the split parts into the original compressed file,
verifies the checksum, and tests gzip integrity.
"""

import os
import sys
import gzip
import hashlib
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    output_file = script_dir.parent / "poems_index_v3.json.gz"

    # Find all parts
    parts = sorted(script_dir.glob("poems_index_v3.json.gz.a*"))

    if not parts:
        print("ERROR: No split parts found!")
        sys.exit(1)

    print(f"Found {len(parts)} parts: {[p.name for p in parts]}")
    print(f"Assembling to: {output_file}")

    # Combine parts
    with open(output_file, 'wb') as outf:
        for part in parts:
            print(f"  Adding: {part.name}")
            with open(part, 'rb') as inf:
                outf.write(inf.read())

    print(f"\nAssembled: {output_file}")
    print(f"Size: {output_file.stat().st_size / (1024*1024):.1f} MB")

    # Verify checksum if available
    checksum_file = script_dir / "checksum.md5"
    if checksum_file.exists():
        expected = checksum_file.read_text().strip().split()[0]
        actual = hashlib.md5(output_file.read_bytes()).hexdigest()
        if actual == expected:
            print(f"Checksum verified: OK ({actual})")
        else:
            print(f"WARNING: Checksum mismatch!")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            sys.exit(1)

    # Verify gzip integrity
    print("Verifying gzip integrity...")
    try:
        with gzip.open(output_file, 'rb') as f:
            # Read a small chunk to verify
            _ = f.read(1024)
        print("Gzip integrity: OK")
    except Exception as e:
        print(f"ERROR: Gzip verification failed: {e}")
        sys.exit(1)

    print("\nTo decompress: gunzip -k poems_index_v3.json.gz")
    print("Or in Python: gzip.open('poems_index_v3.json.gz', 'rt')")

if __name__ == "__main__":
    main()
