#!/usr/bin/env python3
"""
Update corpus metadata to reflect correct version and description.

Updates corpus_unknown_reduced.json metadata to accurately describe the version.
"""

import json
import gzip
from datetime import datetime
from pathlib import Path


def update_metadata(corpus_file: Path, output_file: Path = None):
    """Update corpus metadata with correct version information."""

    # Determine if file is gzipped
    is_gzipped = corpus_file.suffix == '.gz'

    # Load corpus
    print(f"Loading corpus from: {corpus_file}")
    if is_gzipped:
        with gzip.open(corpus_file, 'rt', encoding='utf-8') as f:
            corpus = json.load(f)
    else:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            corpus = json.load(f)

    print(f"  ✓ Loaded {len(corpus.get('words', {})):,} word forms")

    # Current metadata
    old_metadata = corpus.get('metadata', {})
    print("\nCurrent metadata:")
    for key, value in old_metadata.items():
        print(f"  {key}: {value}")

    # Update metadata
    new_metadata = old_metadata.copy()

    # Update version
    new_metadata['version'] = 'v5_unknown_reduced'

    # Update description
    new_metadata['description'] = (
        'Estonian runosong corpus v5 with unknown words reduced via Neurotõlge VRO improvements. '
        'Built from batches_v2_neurotolge_vro with 35,874 VRO dialectal corrections applied, '
        'reducing unknown words from 42,070 to 6,190 (85.3% reduction).'
    )

    # Update created timestamp to reflect modification
    new_metadata['modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add neurotolge info
    new_metadata['neurotolge_vro_applied'] = True
    new_metadata['neurotolge_corrections'] = 35874
    new_metadata['unknown_reduction'] = {
        'before': 42070,
        'after': 6190,
        'reduction_pct': 85.3
    }

    # Add features if not already present
    if 'features' not in new_metadata:
        new_metadata['features'] = []

    if 'neurotolge_vro_corrections' not in new_metadata['features']:
        new_metadata['features'].append('neurotolge_vro_corrections')

    # Update corpus metadata
    corpus['metadata'] = new_metadata

    # Determine output file
    if output_file is None:
        output_file = corpus_file

    # Save updated corpus
    print(f"\nSaving updated corpus to: {output_file}")

    if output_file.suffix == '.gz':
        with gzip.open(output_file, 'wt', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)

    print("  ✓ Saved")

    # Display new metadata
    print("\nUpdated metadata:")
    for key, value in new_metadata.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        elif isinstance(value, list):
            print(f"  {key}: {value[:3]}..." if len(value) > 3 else f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")

    return corpus


def main():
    print("=" * 80)
    print("CORPUS METADATA UPDATE")
    print("=" * 80)
    print()

    # Files to update
    json_file = Path("corpus_unknown_reduced.json")
    gz_file = Path("corpus_unknown_reduced.json.gz")

    # Check which files exist
    files_to_update = []
    if json_file.exists():
        files_to_update.append(json_file)
    if gz_file.exists():
        files_to_update.append(gz_file)

    if not files_to_update:
        print("❌ Error: No corpus files found (corpus_unknown_reduced.json or .gz)")
        return 1

    print(f"Found {len(files_to_update)} file(s) to update:")
    for f in files_to_update:
        print(f"  - {f}")
    print()

    # Update each file
    for corpus_file in files_to_update:
        print(f"\nUpdating: {corpus_file}")
        print("-" * 80)
        update_metadata(corpus_file)
        print()

    print("=" * 80)
    print("✅ METADATA UPDATE COMPLETE")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    exit(main())
