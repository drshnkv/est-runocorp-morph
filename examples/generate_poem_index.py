#!/usr/bin/env python3
"""
Generate poem-level index from batch JSON files

This script processes batch files containing morphologically annotated
Estonian runosongs and creates a poem-level index that preserves word
order and annotations. The output enables viewing complete annotated texts.

Usage:
    python generate_poem_index.py --batch-dir ../../ --output ../poems_index.json.gz

Output structure:
    {
        "89248": {
            "text": "piiri pääri pääsuke kus su kullas pesake...",
            "words": [
                {
                    "original": "piiri",
                    "lemma": "piir",
                    "pos": "S",
                    "form": "sg_g",
                    "method": "estnltk+dict",
                    "confidence": 1.0
                },
                ...
            ],
            "batch": "batch_00001",
            "row_index": 0
        },
        ...
    }
"""

import json
import gzip
import argparse
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm


def process_batch_file(batch_path):
    """Extract poem data from a single batch file"""
    poems = {}

    try:
        with open(batch_path, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)

        batch_name = batch_path.stem

        for item in batch_data.get('items', []):
            poem_id = str(item.get('poem_id'))
            row_index = item.get('row_index')
            results = item.get('results', [])

            # Build word list with annotations
            words = []
            original_words = []

            for word_data in results:
                words.append({
                    'original': word_data.get('original_word', ''),
                    'lemma': word_data.get('best_lemma', ''),
                    'pos': word_data.get('pos', ''),
                    'form': word_data.get('form', ''),
                    'method': word_data.get('method', ''),
                    'confidence': word_data.get('confidence_score', 0.0)
                })
                original_words.append(word_data.get('original_word', ''))

            # Create poem entry
            poems[poem_id] = {
                'text': ' '.join(original_words),
                'words': words,
                'batch': batch_name,
                'row_index': row_index,
                'num_words': len(words)
            }

    except Exception as e:
        print(f"Error processing {batch_path}: {e}")

    return poems


def generate_poem_index(batch_dir, output_path, sample_size=None):
    """
    Generate complete poem index from batch files

    Args:
        batch_dir: Directory containing batch_*.json files
        output_path: Output path for poems_index.json.gz
        sample_size: If set, only process this many batches (for testing)
    """
    batch_dir = Path(batch_dir)

    # Only process canonical batch files (exclude BACKUP, MODIFIED, etc.)
    all_batch_files = sorted(batch_dir.glob('batch_*.json'))
    batch_files = [
        f for f in all_batch_files
        if not any(x in f.name.upper() for x in ['BACKUP', 'MODIFIED', 'OLD', 'TMP'])
    ]

    print(f"Found {len(all_batch_files)} total batch files, filtered to {len(batch_files)} canonical files")

    if sample_size:
        batch_files = batch_files[:sample_size]
        print(f"Processing sample of {len(batch_files)} batches...")
    else:
        print(f"Found {len(batch_files)} batch files to process...")

    all_poems = {}
    stats = defaultdict(int)

    # Process each batch file
    for batch_path in tqdm(batch_files, desc="Processing batches"):
        poems = process_batch_file(batch_path)

        # Merge poems (shouldn't have duplicates, but check)
        for poem_id, poem_data in poems.items():
            if poem_id in all_poems:
                stats['duplicates'] += 1
                print(f"Warning: Duplicate poem_id {poem_id} found")
            else:
                all_poems[poem_id] = poem_data
                stats['total_poems'] += 1
                stats['total_words'] += poem_data['num_words']

    # Create index with metadata
    index = {
        'metadata': {
            'version': 'v1',
            'created_from': f'{len(batch_files)} batch files',
            'total_poems': stats['total_poems'],
            'total_words': stats['total_words'],
            'avg_words_per_poem': stats['total_words'] / max(stats['total_poems'], 1),
            'duplicates_found': stats['duplicates']
        },
        'poems': all_poems
    }

    # Save compressed
    print(f"\nSaving poem index to {output_path}...")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with gzip.open(output_path, 'wt', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    # Print statistics
    print("\n" + "="*60)
    print("POEM INDEX GENERATION COMPLETE")
    print("="*60)
    print(f"Total poems indexed: {stats['total_poems']:,}")
    print(f"Total words: {stats['total_words']:,}")
    print(f"Average words per poem: {stats['total_words'] / max(stats['total_poems'], 1):.1f}")
    print(f"Output file: {output_path}")
    print(f"Output size: {output_path.stat().st_size / (1024**2):.1f} MB")
    print("="*60)

    return index


def main():
    parser = argparse.ArgumentParser(
        description='Generate poem-level index from batch annotation files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--batch-dir',
        default='../../',
        help='Directory containing batch_*.json files (default: ../../)'
    )

    parser.add_argument(
        '--output',
        default='../poems_index.json.gz',
        help='Output path for poem index (default: ../poems_index.json.gz)'
    )

    parser.add_argument(
        '--sample',
        type=int,
        help='Process only first N batches (for testing)'
    )

    args = parser.parse_args()

    # Validate batch directory
    batch_dir = Path(args.batch_dir)
    if not batch_dir.exists():
        print(f"Error: Batch directory not found: {batch_dir}")
        return 1

    batch_files = list(batch_dir.glob('batch_*.json'))
    if not batch_files:
        print(f"Error: No batch_*.json files found in {batch_dir}")
        return 1

    # Generate index
    generate_poem_index(batch_dir, args.output, args.sample)

    return 0


if __name__ == '__main__':
    exit(main())
