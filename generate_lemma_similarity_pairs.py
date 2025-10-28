#!/usr/bin/env python3
"""
Generate Lemma Similarity Pairs CSV for Merge Review

Finds lemma pairs with Levenshtein distance = 1 to identify potential typos
or variants that could be merged.

Based on generate_lemma_overview_v2.py structure.
"""

import json
import gzip
import csv
from collections import Counter, defaultdict
from pathlib import Path


def levenshtein_distance(s1, s2):
    """Calculate Levenshtein distance between two strings"""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def detect_edit_type_and_position(s1, s2):
    """
    Detect the type and position of edit between two strings with distance=1
    Returns: (edit_type, position_category)
    edit_type: 'insertion', 'deletion', 'substitution'
    position_category: 'start', 'middle', 'end'
    """
    if len(s1) < len(s2):
        shorter, longer = s1, s2
        edit_type = 'insertion'
    elif len(s1) > len(s2):
        shorter, longer = s2, s1
        edit_type = 'deletion'
    else:
        edit_type = 'substitution'
        # Find position of difference
        for i, (c1, c2) in enumerate(zip(s1, s2)):
            if c1 != c2:
                if i == 0:
                    return (edit_type, 'start')
                elif i == len(s1) - 1:
                    return (edit_type, 'end')
                else:
                    return (edit_type, 'middle')

    # For insertion/deletion, find where they differ
    if edit_type in ('insertion', 'deletion'):
        for i in range(len(shorter)):
            if i >= len(longer) or shorter[i] != longer[i]:
                if i == 0:
                    return (edit_type, 'start')
                elif i >= len(shorter) - 1:
                    return (edit_type, 'end')
                else:
                    return (edit_type, 'middle')
        # Difference at the end
        return (edit_type, 'end')

    return (edit_type, 'unknown')


def find_similar_pairs_efficient(lemma_list):
    """
    Efficiently find pairs of lemmas with Levenshtein distance = 1

    Strategy: Only compare lemmas with length difference <= 1
    and that share a common prefix/suffix
    """
    print("Finding similar lemma pairs...")

    # Group by length for efficiency
    by_length = defaultdict(list)
    for lemma in lemma_list:
        by_length[len(lemma)].append(lemma)

    pairs = set()
    processed = 0
    total = len(lemma_list)

    # For each lemma, only compare with lemmas of similar length
    for lemma in lemma_list:
        processed += 1
        if processed % 5000 == 0:
            print(f"  Processed {processed:,} / {total:,} lemmas ({processed/total*100:.1f}%)")

        l = len(lemma)
        # Compare with same length and length +/- 1
        candidates = by_length[l] + by_length[l-1] + by_length[l+1]

        for other in candidates:
            if lemma < other:  # Avoid duplicates and self-comparison
                # Quick length check
                if abs(len(lemma) - len(other)) > 1:
                    continue

                # Calculate distance
                if levenshtein_distance(lemma, other) == 1:
                    pairs.add((lemma, other))

    print(f"✓ Found {len(pairs):,} similar pairs")
    return list(pairs)


def get_lemma_stats(lemma, lemma_data, words_data, ambiguous_data):
    """Extract comprehensive statistics for a lemma"""
    stats = {
        'total_occurrences': lemma_data.get('total_occurrences', 0),
        'num_word_forms': len(lemma_data.get('word_forms', [])),
        'word_forms': lemma_data.get('word_forms', []),
        'pos_tags': set(),
        'avg_confidence': 0.0,
        'validation_status': 'none',
        'is_ambiguous': False
    }

    # Get form distribution
    form_dist = lemma_data.get('form_distribution', {})

    # Collect confidence scores
    confidences = []
    for form, data in form_dist.items():
        conf = data.get('confidence_avg', 0.0)
        if conf > 0:
            confidences.append(conf)

    if confidences:
        stats['avg_confidence'] = sum(confidences) / len(confidences)

    # Get POS tags and validation from words section
    validation_statuses = []
    for word_form in lemma_data.get('word_forms', []):
        if word_form not in words_data:
            continue

        word_data = words_data[word_form]

        if lemma not in word_data.get('lemmas', []):
            continue

        # POS tags
        lemma_pos = word_data.get('pos_tags', {}).get(lemma, {})
        for pos in lemma_pos:
            stats['pos_tags'].add(pos)

        # Methods and validation
        lemma_methods = word_data.get('methods', {}).get(lemma, {})
        for method in lemma_methods:
            if '_validation_' in method:
                parts = method.split('_validation_')
                if len(parts) == 2:
                    val_part = parts[1]
                    if '_valid' in val_part:
                        validation_statuses.append('valid')
                    elif '_invalid' in val_part:
                        validation_statuses.append('invalid')

    # Validation status
    if validation_statuses:
        if all(s == 'valid' for s in validation_statuses):
            stats['validation_status'] = 'all_valid'
        elif all(s == 'invalid' for s in validation_statuses):
            stats['validation_status'] = 'all_invalid'
        else:
            stats['validation_status'] = 'mixed'

    # Ambiguity
    for word_form in lemma_data.get('word_forms', []):
        if word_form in ambiguous_data:
            stats['is_ambiguous'] = True
            break

    return stats


def analyze_pair(lemma1, lemma2, lemma_index, words_data, ambiguous_data):
    """Analyze a pair of similar lemmas"""

    lemma1_data = lemma_index.get(lemma1, {})
    lemma2_data = lemma_index.get(lemma2, {})

    # Get statistics for each lemma
    stats1 = get_lemma_stats(lemma1, lemma1_data, words_data, ambiguous_data)
    stats2 = get_lemma_stats(lemma2, lemma2_data, words_data, ambiguous_data)

    # Combined frequency
    combined_frequency = stats1['total_occurrences'] + stats2['total_occurrences']

    # Shared word forms
    forms1 = set(stats1['word_forms'])
    forms2 = set(stats2['word_forms'])
    shared_forms = forms1.intersection(forms2)

    # POS match
    pos_tags_match = bool(stats1['pos_tags'].intersection(stats2['pos_tags']))

    # Frequency ratio (higher/lower)
    if stats1['total_occurrences'] > 0 and stats2['total_occurrences'] > 0:
        frequency_ratio = max(stats1['total_occurrences'], stats2['total_occurrences']) / \
                         min(stats1['total_occurrences'], stats2['total_occurrences'])
    else:
        frequency_ratio = 0.0

    # Confidence difference
    confidence_diff = abs(stats1['avg_confidence'] - stats2['avg_confidence'])

    # Edit type and position
    edit_type, edit_position = detect_edit_type_and_position(lemma1, lemma2)

    # Both validated
    both_validated = (stats1['validation_status'] != 'none' and
                     stats2['validation_status'] != 'none')

    # Either ambiguous
    either_ambiguous = stats1['is_ambiguous'] or stats2['is_ambiguous']

    return {
        'lemma1': lemma1,
        'lemma2': lemma2,
        'combined_frequency': combined_frequency,
        'lemma1_wordforms': ', '.join(sorted(stats1['word_forms'][:20])),  # Limit for readability
        'lemma2_wordforms': ', '.join(sorted(stats2['word_forms'][:20])),
        'pos_tags_match': pos_tags_match,
        'shared_wordforms': len(shared_forms),
        'lemma1_pos': ', '.join(sorted(stats1['pos_tags'])),
        'lemma2_pos': ', '.join(sorted(stats2['pos_tags'])),
        'lemma1_occurrences': stats1['total_occurrences'],
        'lemma2_occurrences': stats2['total_occurrences'],
        'frequency_ratio': round(frequency_ratio, 2),
        'lemma1_avg_confidence': round(stats1['avg_confidence'], 3),
        'lemma2_avg_confidence': round(stats2['avg_confidence'], 3),
        'confidence_difference': round(confidence_diff, 3),
        'lemma1_validation': stats1['validation_status'],
        'lemma2_validation': stats2['validation_status'],
        'both_validated': both_validated,
        'either_ambiguous': either_ambiguous,
        'edit_type': edit_type,
        'edit_position': edit_position
    }


def load_corpus(corpus_path='corpus_validation_improved.json.gz'):
    """Load the corpus JSON file"""
    print(f"Loading corpus from {corpus_path}...")
    with gzip.open(corpus_path, 'rt', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"✓ Loaded corpus with {corpus['metadata']['unique_lemmas']:,} lemmas")
    return corpus


def generate_csv(corpus, output_path='lemma_similarity_pairs.csv'):
    """Generate the lemma similarity pairs CSV"""

    print(f"\nGenerating lemma similarity pairs CSV...")

    lemma_index = corpus.get('lemma_index', {})
    words_data = corpus.get('words', {})
    ambiguous_data = corpus.get('ambiguous_words', {})

    # Find similar pairs
    lemma_list = list(lemma_index.keys())
    pairs = find_similar_pairs_efficient(lemma_list)

    # Define CSV columns
    columns = [
        'lemma1',
        'lemma2',
        'combined_frequency',
        'lemma1_wordforms',
        'lemma2_wordforms',
        'pos_tags_match',
        'shared_wordforms',
        'lemma1_pos',
        'lemma2_pos',
        'lemma1_occurrences',
        'lemma2_occurrences',
        'frequency_ratio',
        'lemma1_avg_confidence',
        'lemma2_avg_confidence',
        'confidence_difference',
        'lemma1_validation',
        'lemma2_validation',
        'both_validated',
        'either_ambiguous',
        'edit_type',
        'edit_position'
    ]

    # Analyze all pairs
    print(f"\nAnalyzing {len(pairs):,} pairs...")
    rows = []
    for idx, (lemma1, lemma2) in enumerate(pairs, 1):
        if idx % 1000 == 0:
            print(f"  Analyzed {idx:,} / {len(pairs):,} pairs ({idx/len(pairs)*100:.1f}%)")

        row = analyze_pair(lemma1, lemma2, lemma_index, words_data, ambiguous_data)
        rows.append(row)

    # Sort by combined frequency (descending) - tackle high-impact pairs first
    rows.sort(key=lambda x: x['combined_frequency'], reverse=True)

    # Write CSV
    print(f"\nWriting CSV to {output_path}...")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ CSV written with {len(rows):,} similar pairs")

    # Print statistics
    print(f"\nStatistics:")
    print(f"  Total similar pairs: {len(rows):,}")
    print(f"  POS tags match: {sum(1 for r in rows if r['pos_tags_match']):,}")
    print(f"  With shared word forms: {sum(1 for r in rows if r['shared_wordforms'] > 0):,}")
    print(f"  Both validated: {sum(1 for r in rows if r['both_validated']):,}")
    print(f"  Either ambiguous: {sum(1 for r in rows if r['either_ambiguous']):,}")
    print(f"\nEdit type distribution:")
    edit_types = Counter(r['edit_type'] for r in rows)
    for edit_type, count in edit_types.most_common():
        print(f"  {edit_type}: {count:,}")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate lemma similarity pairs CSV for merge review')
    parser.add_argument('--corpus', default='corpus_validation_improved.json.gz',
                       help='Path to corpus JSON file (default: corpus_validation_improved.json.gz)')
    parser.add_argument('--output', default='lemma_similarity_pairs.csv',
                       help='Output CSV file path (default: lemma_similarity_pairs.csv)')

    args = parser.parse_args()

    # Load corpus
    corpus = load_corpus(args.corpus)

    # Generate CSV
    generate_csv(corpus, args.output)

    print(f"\n✓ Done! CSV file: {args.output}")
    print(f"\nUsage examples:")
    print(f"  # Open in spreadsheet software and sort by 'combined_frequency' descending")
    print(f"  # Filter by 'pos_tags_match=TRUE' to see candidates with matching POS")
    print(f"  # Filter by 'shared_wordforms>0' to see lemmas sharing word forms")
    print(f"  # Review 'frequency_ratio' - high ratios suggest one is likely a typo")


if __name__ == '__main__':
    main()
