#!/usr/bin/env python3
"""
Apply POS Substitutions to Corpus Files

This script applies the verified POS substitutions from final_substitutions.csv to:
1. poems_index_v2.json → poems_index_v3.json
2. corpus_full_source_poems.json → corpus_full_source_poems_v2.json

The substitutions correct POS tagging errors identified through systematic
analysis of 214 substitution combinations with 5 verse examples each.

Usage:
    python apply_substitutions.py
    python apply_substitutions.py --dry-run  # Preview changes without writing

Author: Claude (with human review)
Date: 2025-12-16
"""

import json
import csv
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_substitutions(filepath: str) -> dict:
    """Load substitutions from CSV into lookup dictionary.

    Returns dict mapping (lemma, current_pos) -> correct_pos
    """
    substitutions = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('category') == 'apply':
                key = (row['lemma'], row['current_pos'])
                substitutions[key] = {
                    'correct_pos': row['correct_pos'],
                    'source': row['source'],
                    'notes': row.get('notes', '')
                }
    return substitutions


def apply_to_poems_index(input_path: str, output_path: str,
                         substitutions: dict, dry_run: bool = False) -> dict:
    """Apply substitutions to poems_index file.

    Args:
        input_path: Path to poems_index_v2.json
        output_path: Path for output poems_index_v3.json
        substitutions: Dict of (lemma, current_pos) -> {correct_pos, source, notes}
        dry_run: If True, only count changes without writing

    Returns:
        Statistics about changes made
    """
    print(f"Loading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = {
        'total_poems': 0,
        'poems_with_changes': 0,
        'total_words': 0,
        'words_changed': 0,
        'changes_by_substitution': defaultdict(int),
        'manual_override_words': 0
    }

    print("Applying substitutions to poems...")
    for poem_id, poem in data['poems'].items():
        stats['total_poems'] += 1
        poem_changed = False

        for word in poem.get('words', []):
            stats['total_words'] += 1

            # Only modify manual_override entries
            if word.get('method') != 'manual_override':
                continue

            stats['manual_override_words'] += 1

            lemma = word.get('lemma', '').lower()
            current_pos = word.get('pos', '')
            key = (lemma, current_pos)

            if key in substitutions:
                correct_pos = substitutions[key]['correct_pos']
                if current_pos != correct_pos:
                    word['pos'] = correct_pos
                    stats['words_changed'] += 1
                    stats['changes_by_substitution'][f"{lemma}|{current_pos}→{correct_pos}"] += 1
                    poem_changed = True

        if poem_changed:
            stats['poems_with_changes'] += 1

    # Update metadata
    data['metadata']['version'] = 'v3'
    data['metadata']['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['metadata']['created_from'] = 'poems_index_v2 + final_substitutions.csv'
    data['metadata']['pos_corrections_applied'] = stats['words_changed']
    data['metadata']['substitution_combinations'] = len(substitutions)

    if not dry_run:
        print(f"Writing {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}")

    return stats


def apply_to_corpus(input_path: str, output_path: str,
                    substitutions: dict, dry_run: bool = False) -> dict:
    """Apply substitutions to corpus_full_source_poems.json.

    This file has aggregated word data. We need to:
    1. Update pos_tags for each affected lemma
    2. Recalculate totals

    Args:
        input_path: Path to corpus_full_source_poems.json
        output_path: Path for output corpus_full_source_poems_v2.json
        substitutions: Dict of (lemma, current_pos) -> {correct_pos, source, notes}
        dry_run: If True, only count changes without writing

    Returns:
        Statistics about changes made
    """
    print(f"Loading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = {
        'total_words': 0,
        'lemmas_changed': 0,
        'pos_counts_updated': 0
    }

    # Build reverse lookup: lemma -> list of (current_pos, correct_pos)
    lemma_subs = defaultdict(list)
    for (lemma, current_pos), sub_info in substitutions.items():
        lemma_subs[lemma].append((current_pos, sub_info['correct_pos']))

    print("Applying substitutions to corpus...")
    for word_form, word_data in data['words'].items():
        stats['total_words'] += 1

        # Check each lemma for this word form
        for lemma in word_data.get('lemmas', []):
            lemma_lower = lemma.lower()

            if lemma_lower in lemma_subs:
                # This lemma has substitutions
                pos_tags = word_data.get('pos_tags', {}).get(lemma, {})

                for current_pos, correct_pos in lemma_subs[lemma_lower]:
                    if current_pos in pos_tags:
                        count = pos_tags.pop(current_pos)
                        pos_tags[correct_pos] = pos_tags.get(correct_pos, 0) + count
                        stats['pos_counts_updated'] += count
                        stats['lemmas_changed'] += 1

    # Update metadata
    data['metadata']['version'] = 'v7_pos_corrected'
    data['metadata']['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['metadata']['pos_corrections_applied'] = stats['pos_counts_updated']

    if not dry_run:
        print(f"Writing {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}")

    return stats


def print_stats(poems_stats: dict, corpus_stats: dict):
    """Print summary statistics."""
    print("\n" + "=" * 60)
    print("SUBSTITUTION APPLICATION SUMMARY")
    print("=" * 60)

    print("\n📚 poems_index_v3.json:")
    print(f"   Total poems: {poems_stats['total_poems']:,}")
    print(f"   Poems with changes: {poems_stats['poems_with_changes']:,}")
    print(f"   Total words: {poems_stats['total_words']:,}")
    print(f"   Manual override words: {poems_stats['manual_override_words']:,}")
    print(f"   Words corrected: {poems_stats['words_changed']:,}")
    pct = poems_stats['words_changed'] / poems_stats['manual_override_words'] * 100 if poems_stats['manual_override_words'] > 0 else 0
    print(f"   Correction rate: {pct:.1f}% of manual_override")

    print("\n📁 corpus_full_source_poems_v2.json:")
    print(f"   Total word forms: {corpus_stats['total_words']:,}")
    print(f"   Lemma entries updated: {corpus_stats['lemmas_changed']:,}")
    print(f"   POS counts transferred: {corpus_stats['pos_counts_updated']:,}")

    print("\n🔝 Top 10 substitutions by frequency:")
    top_10 = sorted(poems_stats['changes_by_substitution'].items(),
                    key=lambda x: -x[1])[:10]
    for sub, count in top_10:
        print(f"   {sub}: {count:,}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Apply POS substitutions to corpus files'
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without writing files')
    parser.add_argument('--substitutions', default='final_substitutions.csv',
                       help='Path to substitutions CSV file')
    parser.add_argument('--poems-input', default='poems_index_v2.json',
                       help='Input poems index file')
    parser.add_argument('--poems-output', default='poems_index_v3.json',
                       help='Output poems index file')
    parser.add_argument('--corpus-input', default='corpus_full_source_poems.json',
                       help='Input corpus file')
    parser.add_argument('--corpus-output', default='corpus_full_source_poems_v2.json',
                       help='Output corpus file')

    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be written\n")

    # Load substitutions
    print(f"Loading substitutions from {args.substitutions}...")
    substitutions = load_substitutions(args.substitutions)
    print(f"Loaded {len(substitutions)} substitution rules\n")

    # Apply to poems index
    poems_stats = apply_to_poems_index(
        args.poems_input,
        args.poems_output,
        substitutions,
        args.dry_run
    )

    # Apply to corpus
    corpus_stats = apply_to_corpus(
        args.corpus_input,
        args.corpus_output,
        substitutions,
        args.dry_run
    )

    # Print summary
    print_stats(poems_stats, corpus_stats)

    if args.dry_run:
        print("\n💡 Run without --dry-run to apply changes")


if __name__ == '__main__':
    main()
