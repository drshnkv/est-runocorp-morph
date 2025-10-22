#!/usr/bin/env python3
"""
View complete annotated Estonian runosong poems from the morphological corpus

This script allows querying and viewing complete poems with their morphological
annotations preserved, including lemmas, POS tags, morphological forms, and
confidence scores.

Usage examples:
    # View a specific poem
    python view_poem.py 89248

    # View with detailed annotation display
    python view_poem.py 89248 --detailed

    # View multiple poems
    python view_poem.py 89248 89249 89250

    # Search poems with specific criteria
    python view_poem.py --min-confidence 0.9 --random 5

    # Export poem to JSON
    python view_poem.py 89248 --export poem_89248.json
"""

import json
import gzip
import argparse
import random
from pathlib import Path
from collections import defaultdict


def load_poem_index(index_path='../poems_index.json.gz'):
    """Load the compressed poem index"""
    print(f"Loading poem index from {index_path}...")
    with gzip.open(index_path, 'rt', encoding='utf-8') as f:
        index = json.load(f)
    print(f"✅ Loaded {index['metadata']['total_poems']:,} poems")
    return index


def format_word_annotation(word_data, detailed=False):
    """Format a single word's annotation"""
    if detailed:
        parts = [
            f"{word_data['original']}",
            f"lemma={word_data['lemma']}",
            f"pos={word_data['pos']}" if word_data['pos'] else None,
            f"form={word_data['form']}" if word_data['form'] else None,
            f"method={word_data['method']}",
            f"conf={word_data['confidence']:.2f}"
        ]
        return " [" + " ".join(p for p in parts if p) + "]"
    else:
        # Compact format: word/lemma(POS)
        if word_data['pos']:
            return f"{word_data['original']}/{word_data['lemma']}({word_data['pos']})"
        else:
            return f"{word_data['original']}/{word_data['lemma']}"


def display_poem(poem_id, poem_data, detailed=False):
    """Display a poem with its annotations"""
    print("\n" + "="*80)
    print(f"POEM ID: {poem_id}")
    print("="*80)

    # Metadata
    print(f"Source batch: {poem_data['batch']}")
    print(f"Row index: {poem_data['row_index']}")
    print(f"Number of words: {poem_data['num_words']}")

    # Statistics
    avg_conf = sum(w['confidence'] for w in poem_data['words']) / len(poem_data['words'])
    print(f"Average confidence: {avg_conf:.3f}")

    pos_dist = defaultdict(int)
    method_dist = defaultdict(int)
    for word in poem_data['words']:
        if word['pos']:
            pos_dist[word['pos']] += 1
        method_dist[word['method']] += 1

    print(f"POS distribution: {dict(pos_dist)}")
    print(f"Method distribution: {dict(method_dist)}")

    # Original text
    print("\n" + "-"*80)
    print("ORIGINAL TEXT:")
    print("-"*80)
    print(poem_data['text'])

    # Annotated text
    print("\n" + "-"*80)
    if detailed:
        print("DETAILED ANNOTATIONS:")
    else:
        print("ANNOTATED TEXT (word/lemma(POS)):")
    print("-"*80)

    if detailed:
        # Line-by-line detailed view
        for i, word_data in enumerate(poem_data['words'], 1):
            print(f"{i:3}. {format_word_annotation(word_data, detailed=True)}")
    else:
        # Compact inline format
        annotated_words = [format_word_annotation(w, detailed=False) for w in poem_data['words']]
        # Wrap at reasonable line length
        line = ""
        for word in annotated_words:
            if len(line) + len(word) + 1 > 80:
                print(line)
                line = word
            else:
                line = line + " " + word if line else word
        if line:
            print(line)

    print("="*80)


def filter_poems(index, min_confidence=None, max_words=None, min_words=None,
                 pos_contains=None, method=None):
    """Filter poems based on criteria"""
    filtered = {}

    for poem_id, poem_data in index['poems'].items():
        # Skip empty poems
        if not poem_data['words'] or poem_data['num_words'] == 0:
            continue

        # Calculate average confidence
        avg_conf = sum(w['confidence'] for w in poem_data['words']) / len(poem_data['words'])

        # Apply filters
        if min_confidence and avg_conf < min_confidence:
            continue
        if max_words and poem_data['num_words'] > max_words:
            continue
        if min_words and poem_data['num_words'] < min_words:
            continue

        if pos_contains:
            has_pos = any(w['pos'] == pos_contains for w in poem_data['words'])
            if not has_pos:
                continue

        if method:
            has_method = any(w['method'] == method for w in poem_data['words'])
            if not has_method:
                continue

        filtered[poem_id] = poem_data

    return filtered


def export_poem(poem_id, poem_data, output_path):
    """Export poem to JSON file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    export_data = {
        'poem_id': poem_id,
        **poem_data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported poem {poem_id} to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='View complete annotated Estonian runosong poems',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'poem_ids',
        nargs='*',
        help='Poem IDs to display'
    )

    parser.add_argument(
        '--index',
        default='../poems_index.json.gz',
        help='Path to poem index file (default: ../poems_index.json.gz)'
    )

    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed line-by-line annotations'
    )

    parser.add_argument(
        '--random',
        type=int,
        metavar='N',
        help='Display N random poems (optionally filtered)'
    )

    parser.add_argument(
        '--min-confidence',
        type=float,
        help='Filter poems by minimum average confidence'
    )

    parser.add_argument(
        '--max-words',
        type=int,
        help='Filter poems by maximum word count'
    )

    parser.add_argument(
        '--min-words',
        type=int,
        help='Filter poems by minimum word count'
    )

    parser.add_argument(
        '--pos-contains',
        help='Filter poems containing specific POS tag (e.g., V, S, A)'
    )

    parser.add_argument(
        '--method',
        help='Filter poems containing specific annotation method'
    )

    parser.add_argument(
        '--list-stats',
        action='store_true',
        help='List corpus statistics and exit'
    )

    parser.add_argument(
        '--export',
        help='Export poem to JSON file'
    )

    args = parser.parse_args()

    # Load index
    index = load_poem_index(args.index)

    # Show statistics
    if args.list_stats:
        print("\n" + "="*80)
        print("CORPUS STATISTICS")
        print("="*80)
        for key, value in index['metadata'].items():
            if isinstance(value, float):
                print(f"{key}: {value:.1f}")
            else:
                print(f"{key}: {value:,}" if isinstance(value, int) else f"{key}: {value}")
        print("="*80)
        return 0

    # Apply filters if specified
    if any([args.min_confidence, args.max_words, args.min_words,
            args.pos_contains, args.method]):
        poems = filter_poems(
            index,
            min_confidence=args.min_confidence,
            max_words=args.max_words,
            min_words=args.min_words,
            pos_contains=args.pos_contains,
            method=args.method
        )
        print(f"✅ Filtered to {len(poems):,} poems matching criteria")
    else:
        poems = index['poems']

    # Handle random selection
    if args.random:
        selected_ids = random.sample(list(poems.keys()), min(args.random, len(poems)))
        print(f"✅ Randomly selected {len(selected_ids)} poems")
    elif args.poem_ids:
        selected_ids = args.poem_ids
    else:
        print("Error: Please specify poem IDs or use --random")
        print("Example: python view_poem.py 89248")
        print("         python view_poem.py --random 5")
        return 1

    # Display poems
    for poem_id in selected_ids:
        poem_id = str(poem_id)  # Ensure string
        if poem_id not in poems:
            print(f"❌ Poem {poem_id} not found in index")
            continue

        poem_data = poems[poem_id]
        display_poem(poem_id, poem_data, detailed=args.detailed)

        # Export if requested
        if args.export:
            if len(selected_ids) == 1:
                export_poem(poem_id, poem_data, args.export)
            else:
                # Multiple poems: create separate files
                base_path = Path(args.export)
                export_path = base_path.parent / f"{base_path.stem}_{poem_id}{base_path.suffix}"
                export_poem(poem_id, poem_data, export_path)

    return 0


if __name__ == '__main__':
    exit(main())
