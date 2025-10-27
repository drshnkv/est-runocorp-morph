#!/usr/bin/env python3
"""
Generate Lemma Overview CSV from Estonian Runosong Corpus v2

Creates a human-readable CSV with comprehensive information about each lemma
for quality review and linguistic analysis.

Uses the actual corpus structure where lemma_index contains aggregated data.
"""

import json
import gzip
import csv
from collections import Counter
from pathlib import Path

def load_corpus(corpus_path='corpus_validation_improved.json.gz'):
    """Load the corpus JSON file"""
    print(f"Loading corpus from {corpus_path}...")
    with gzip.open(corpus_path, 'rt', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"✓ Loaded corpus with {corpus['metadata']['unique_lemmas']:,} lemmas")
    return corpus

def analyze_lemma(lemma, lemma_data, words_data, ambiguous_data):
    """Analyze a single lemma using lemma_index data structure"""

    result = {
        'lemma': lemma,
        'total_occurrences': lemma_data.get('total_occurrences', 0),
        'num_word_forms': len(lemma_data.get('word_forms', [])),
        'word_forms_sample': '',
        'most_frequent_form': '',
        'most_frequent_form_count': 0,
        'most_frequent_form_pct': 0.0,
        'pos_tags': '',
        'morph_forms': '',
        'avg_confidence': 0.0,
        'primary_method': '',
        'methods_used': '',
        'has_validation': False,
        'validation_status': 'none',
        'validation_method': '',
        'is_ambiguous': False,
        'needs_review': False,
        'num_competing_lemmas': 0,
        'form_diversity_score': 0.0,
        'min_confidence': 1.0,
        'max_confidence': 0.0
    }

    # Get form distribution from lemma_index
    form_dist = lemma_data.get('form_distribution', {})

    if not form_dist:
        return result

    # Sort forms by count
    form_counts = [(form, data['count']) for form, data in form_dist.items()]
    form_counts.sort(key=lambda x: x[1], reverse=True)

    # Most frequent form
    if form_counts:
        result['most_frequent_form'] = form_counts[0][0]
        result['most_frequent_form_count'] = form_counts[0][1]
        if result['total_occurrences'] > 0:
            result['most_frequent_form_pct'] = (form_counts[0][1] / result['total_occurrences']) * 100

    # Word forms sample (top 10)
    top_forms = [f"{form}({count})" for form, count in form_counts[:10]]
    result['word_forms_sample'] = '; '.join(top_forms)

    # Collect morphological forms and confidence from form_distribution
    morph_forms = set()
    confidences = []

    for form, data in form_dist.items():
        # Morphological forms
        for mform in data.get('forms', []):
            morph_forms.add(mform)

        # Confidence
        conf = data.get('confidence_avg', 0.0)
        if conf > 0:
            confidences.append(conf)

    result['morph_forms'] = ', '.join(sorted(list(morph_forms)[:10]))

    # Confidence statistics
    if confidences:
        result['avg_confidence'] = sum(confidences) / len(confidences)
        result['min_confidence'] = min(confidences)
        result['max_confidence'] = max(confidences)

    # Form diversity score
    if result['total_occurrences'] > 0:
        result['form_diversity_score'] = result['num_word_forms'] / result['total_occurrences']

    # Now get detailed info from words section
    pos_tags = set()
    methods = []
    validation_statuses = []

    for word_form in lemma_data.get('word_forms', []):
        if word_form not in words_data:
            continue

        word_data = words_data[word_form]

        # Check if this lemma exists for this word
        if lemma not in word_data.get('lemmas', []):
            continue

        # POS tags
        lemma_pos = word_data.get('pos_tags', {}).get(lemma, {})
        for pos in lemma_pos:
            pos_tags.add(pos)

        # Methods
        lemma_methods = word_data.get('methods', {}).get(lemma, {})
        for method in lemma_methods:
            methods.append(method)
            if '_validation_' in method:
                result['has_validation'] = True
                parts = method.split('_validation_')
                if len(parts) == 2:
                    val_part = parts[1]
                    if '_valid' in val_part:
                        validation_statuses.append('valid')
                        result['validation_method'] = val_part.split('_valid')[0]
                    elif '_invalid' in val_part:
                        validation_statuses.append('invalid')
                        result['validation_method'] = val_part.split('_invalid')[0]

    result['pos_tags'] = ', '.join(sorted(pos_tags))

    # Methods
    if methods:
        method_counts = Counter(methods)
        result['primary_method'] = method_counts.most_common(1)[0][0]
        result['methods_used'] = ', '.join(sorted(set(methods)))

    # Validation status
    if validation_statuses:
        if all(s == 'valid' for s in validation_statuses):
            result['validation_status'] = 'all_valid'
        elif all(s == 'invalid' for s in validation_statuses):
            result['validation_status'] = 'all_invalid'
        else:
            result['validation_status'] = 'mixed'

    # Ambiguity (check in words section for each word_form)
    for word_form in lemma_data.get('word_forms', []):
        if word_form in ambiguous_data:
            result['is_ambiguous'] = True
            ambig_info = ambiguous_data[word_form]
            result['num_competing_lemmas'] = max(result['num_competing_lemmas'],
                                                   len(ambig_info.get('lemmas', {})))
            result['needs_review'] = result['needs_review'] or ambig_info.get('needs_review', False)
            break

    return result

def generate_csv(corpus, output_path='lemma_overview_v2.csv'):
    """Generate the lemma overview CSV"""

    print(f"\nGenerating lemma overview CSV...")

    lemma_index = corpus.get('lemma_index', {})
    words_data = corpus.get('words', {})
    ambiguous_data = corpus.get('ambiguous_words', {})

    # Define CSV columns
    columns = [
        'lemma',
        'total_occurrences',
        'num_word_forms',
        'word_forms_sample',
        'most_frequent_form',
        'most_frequent_form_count',
        'most_frequent_form_pct',
        'pos_tags',
        'morph_forms',
        'avg_confidence',
        'primary_method',
        'methods_used',
        'has_validation',
        'validation_status',
        'validation_method',
        'is_ambiguous',
        'needs_review',
        'num_competing_lemmas',
        'form_diversity_score',
        'min_confidence',
        'max_confidence'
    ]

    # Process all lemmas
    rows = []
    total_lemmas = len(lemma_index)

    for idx, (lemma, lemma_data) in enumerate(lemma_index.items(), 1):
        if idx % 5000 == 0:
            print(f"  Processed {idx:,} / {total_lemmas:,} lemmas ({idx/total_lemmas*100:.1f}%)")

        row = analyze_lemma(lemma, lemma_data, words_data, ambiguous_data)
        rows.append(row)

    # Sort by total occurrences (descending)
    rows.sort(key=lambda x: x['total_occurrences'], reverse=True)

    # Write CSV
    print(f"\nWriting CSV to {output_path}...")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ CSV written with {len(rows):,} lemmas")

    # Print statistics
    print(f"\nStatistics:")
    print(f"  Total lemmas: {len(rows):,}")
    print(f"  With data: {sum(1 for r in rows if r['total_occurrences'] > 0):,}")
    print(f"  With validation: {sum(1 for r in rows if r['has_validation']):,}")
    print(f"  Ambiguous: {sum(1 for r in rows if r['is_ambiguous']):,}")
    print(f"  Need review: {sum(1 for r in rows if r['needs_review']):,}")
    print(f"  All valid validation: {sum(1 for r in rows if r['validation_status'] == 'all_valid'):,}")
    print(f"  All invalid validation: {sum(1 for r in rows if r['validation_status'] == 'all_invalid'):,}")
    print(f"  Mixed validation: {sum(1 for r in rows if r['validation_status'] == 'mixed'):,}")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate lemma overview CSV from corpus')
    parser.add_argument('--corpus', default='corpus_validation_improved.json.gz',
                        help='Path to corpus JSON file (default: corpus_validation_improved.json.gz)')
    parser.add_argument('--output', default='lemma_overview_v2.csv',
                        help='Output CSV file path (default: lemma_overview_v2.csv)')

    args = parser.parse_args()

    # Load corpus
    corpus = load_corpus(args.corpus)

    # Generate CSV
    generate_csv(corpus, args.output)

    print(f"\n✓ Done! CSV file: {args.output}")
    print(f"\nUsage examples:")
    print(f"  # Open in spreadsheet software")
    print(f"  # Sort by 'total_occurrences' to review high-frequency lemmas")
    print(f"  # Filter by 'has_validation=TRUE' to see validation changes")
    print(f"  # Filter by 'validation_status=all_invalid' to find potential issues")

if __name__ == '__main__':
    main()
