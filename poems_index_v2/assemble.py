#!/usr/bin/env python3
"""
Cross-platform reassembly script for poems_index_v2.json.gz

This script concatenates split parts back into the original file
and verifies integrity using both gzip validation and MD5 checksum.

Usage:
    python assemble.py

Output:
    ../poems_index_v2.json.gz (relative to this script)
"""

import os
import sys
import glob
import gzip
import hashlib
from pathlib import Path


def get_md5(filepath: Path) -> str:
    """Calculate MD5 hash of a file."""
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()


def main():
    print("=== Reassembling poems_index_v2.json.gz ===\n")

    # Get script directory
    script_dir = Path(__file__).parent.resolve()
    output_file = script_dir.parent / "poems_index_v2.json.gz"

    print(f"Working directory: {script_dir}")

    # Find all parts
    pattern = str(script_dir / "poems_index_v2.json.gz.*")
    parts = sorted(glob.glob(pattern))

    if not parts:
        print("ERROR: No parts found matching poems_index_v2.json.gz.*")
        sys.exit(1)

    print(f"Found {len(parts)} parts:")
    for part in parts:
        size_mb = Path(part).stat().st_size / (1024 * 1024)
        print(f"  - {Path(part).name} ({size_mb:.1f} MB)")

    # Concatenate parts
    print("\nConcatenating parts...")
    total_bytes = 0
    with open(output_file, 'wb') as out:
        for part in parts:
            with open(part, 'rb') as f:
                data = f.read()
                total_bytes += len(data)
                out.write(data)

    print(f"Written {total_bytes:,} bytes ({total_bytes / (1024*1024):.1f} MB)")

    # Verify gzip integrity
    print("\nVerifying gzip integrity...")
    try:
        with gzip.open(output_file, 'rb') as f:
            # Read first and last chunks to verify structure
            f.read(1024)
            f.seek(-1024, 2)  # Seek to end
            f.read(1024)
        print("✓ gzip integrity check PASSED")
    except Exception as e:
        print(f"✗ ERROR: gzip integrity check FAILED: {e}")
        output_file.unlink(missing_ok=True)
        sys.exit(1)

    # Verify MD5 checksum
    checksum_file = script_dir / "checksum.md5"
    if checksum_file.exists():
        print("\nVerifying MD5 checksum...")

        # Read expected MD5 (handle both formats: "hash" or "MD5 (file) = hash")
        content = checksum_file.read_text().strip()
        if '=' in content:
            expected_md5 = content.split('=')[-1].strip()
        else:
            expected_md5 = content.split()[0]

        actual_md5 = get_md5(output_file)

        if expected_md5 == actual_md5:
            print(f"✓ MD5 checksum PASSED: {actual_md5}")
        else:
            print("✗ ERROR: MD5 checksum FAILED")
            print(f"  Expected: {expected_md5}")
            print(f"  Actual:   {actual_md5}")
            sys.exit(1)

    # Final report
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print("\n=== Assembly Complete ===")
    print(f"Output: {output_file}")
    print(f"Size: {size_mb:.1f} MB")


if __name__ == '__main__':
    main()
