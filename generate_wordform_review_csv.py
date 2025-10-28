#!/usr/bin/env python3
"""
Generate Word-Form Review CSV for LLM Validation

Creates a CSV with 20,000 most frequent word forms including:
- Lemma assignments (primary + alternatives)
- Quality indicators (POS, morphology, confidence)
- Validation status
- Sample poem contexts (2-3 per word form)

Purpose: Enable word-form-centric LLM validation where Claude reviews
(word_form, lemma) assignments in actual usage contexts.
"""

import json
import gzip
import csv
from collections import Counter
from pathlib import Path
import random


def load_corpus(corpus_path='corpus_validation_improved.json.gz'):
    """Load the corpus JSON file"""
    print(f"Loading corpus from {corpus_path}...")
    with gzip.open(corpus_path, 'rt', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"✓ Loaded corpus with {len(corpus['words']):,} word forms")
    return corpus


def load_poems_index(poems_path='poems_index.json.gz'):
    """Load the poems index for contexts"""
    print(f"\nLoading poems index from {poems_path}...")
    with gzip.open(poems_path, 'rt', encoding='utf-8') as f:
        poems = json.load(f)
    print(f"✓ Loaded {len(poems['poems']):,} poems")
    return poems


def build_context_mapping(poems):
    """Build word_form → contexts mapping from poems index"""
    print("\nBuilding word form → context mapping...")

    context_map = {}

    for poem_id, poem_data in poems['poems'].items():
        words_data = poem_data.get('words', [])

        for idx, word_entry in enumerate(words_data):
            word_form = word_entry.get('original')
            if not word_form:
                continue

            # Get surrounding context (simplified - just the word itself for now)
            # In a more sophisticated version, we'd extract sentence/line context
            if word_form not in context_map:
                context_map[word_form] = []

            # Store poem_id and word data with context
            context_map[word_form].append({
                'poem_id': poem_id,
                'word': word_form,
                'lemma': word_entry.get('lemma'),
                'pos': word_entry.get('pos'),
                'form': word_entry.get('form'),
                'confidence': word_entry.get('confidence'),
                'word_index': idx,  # Store index for later context extraction
            })

    print(f"✓ Built context mapping for {len(context_map):,} unique word forms")
    return context_map


def extract_sentence_context(poems, poem_id, word_index, window=5):
    """Extract sentence context around a word"""
    try:
        poem_data = poems['poems'][poem_id]
        text_data = poem_data.get('text', [])

        if word_index >= len(text_data):
            return None

        # Get words in a window around target word
        start = max(0, word_index - window)
        end = min(len(text_data), word_index + window + 1)

        context_words = []
        for i in range(start, end):
            word = text_data[i].get('word', '')
            if i == word_index:
                # Mark the target word
                context_words.append(f"**{word}**")
            else:
                context_words.append(word)

        return ' '.join(context_words)
    except:
        return None


def get_sample_contexts(word_form, poems, context_map, num_samples=3):
    """Get sample contexts for a word form from poems"""
    contexts_data = context_map.get(word_form, [])

    if not contexts_data:
        return "", ""

    # Sample up to num_samples contexts
    sample_size = min(num_samples, len(contexts_data))
    sampled = random.sample(contexts_data, sample_size) if len(contexts_data) > num_samples else contexts_data

    # Extract contexts with surrounding words
    contexts = []
    poem_ids = []

    for ctx in sampled:
        poem_id = ctx['poem_id']
        word_index = ctx['word_index']
        poem_ids.append(poem_id)

        # Get surrounding words for context (5 words before and after)
        poem_data = poems['poems'][poem_id]
        words = poem_data.get('words', [])

        start_idx = max(0, word_index - 5)
        end_idx = min(len(words), word_index + 6)

        # Build context string
        context_words = []
        for i in range(start_idx, end_idx):
            word = words[i].get('original', '')
            if i == word_index:
                # Mark the target word
                context_words.append(f"**{word}**")
            else:
                context_words.append(word)

        context_str = ' '.join(context_words)
        lemma_str = ctx['lemma']
        contexts.append(f"{context_str} [→{lemma_str}]")

    contexts_str = " | ".join(contexts[:3])  # Use | separator for readability
    poem_ids_str = ", ".join(poem_ids[:3])

    return contexts_str, poem_ids_str


def analyze_word_form(word_form, word_data, poems, context_map):
    """Analyze a word form and compile all information"""

    result = {
        'word_form': word_form,
        'total_occurrences': 0,
        'num_poems': len(word_data.get('source_poems', [])),
        'primary_lemma': '',
        'all_lemmas': '',
        'num_lemmas': 0,
        'pos_tags': '',
        'morph_forms': '',
        'avg_confidence': 0.0,
        'min_confidence': 1.0,
        'max_confidence': 0.0,
        'primary_method': '',
        'validation_status': 'none',
        'is_ambiguous': False,
        'needs_review': False,
        'sample_contexts': '',
        'context_poem_ids': '',
        'word_length': len(word_form),
        'lemma_length': 0
    }

    # Get lemma counts (dict: lemma → count)
    lemma_counts = word_data.get('lemma_counts', {})
    if not lemma_counts:
        return result

    # Total occurrences
    result['total_occurrences'] = word_data.get('total_count', sum(lemma_counts.values()))

    # Primary lemma = most frequent
    primary = max(lemma_counts.items(), key=lambda x: x[1])[0]
    result['primary_lemma'] = primary
    result['lemma_length'] = len(primary)
    result['all_lemmas'] = ', '.join(sorted(lemma_counts.keys()))
    result['num_lemmas'] = len(lemma_counts)
    result['is_ambiguous'] = len(lemma_counts) > 1

    # Get data for primary lemma from top-level dicts
    # POS tags
    pos_tags_dict = word_data.get('pos_tags', {}).get(primary, {})
    result['pos_tags'] = ', '.join(sorted(pos_tags_dict.keys()))

    # Morphological forms
    forms_dict = word_data.get('forms', {}).get(primary, {})
    result['morph_forms'] = ', '.join(sorted(list(forms_dict.keys())[:10]))  # Limit to 10

    # Confidence
    conf_dict = word_data.get('confidences', {}).get(primary, {})
    if conf_dict:
        result['avg_confidence'] = conf_dict.get('avg', 0.0)
        result['min_confidence'] = conf_dict.get('min', 0.0)
        result['max_confidence'] = conf_dict.get('max', 0.0)

    # Methods
    methods_dict = word_data.get('methods', {}).get(primary, {})
    if methods_dict:
        # methods_dict is {method: count}, get most common
        method_counts = Counter(methods_dict.keys())
        result['primary_method'] = method_counts.most_common(1)[0][0]

        # Validation status (check if any method has validation)
        for method in methods_dict.keys():
            if '_validation_' in method:
                parts = method.split('_validation_')
                if len(parts) == 2:
                    val_part = parts[1]
                    if '_valid' in val_part:
                        result['validation_status'] = 'valid'
                        break
                    elif '_invalid' in val_part:
                        result['validation_status'] = 'invalid'

    # Get sample contexts
    contexts_str, poem_ids_str = get_sample_contexts(word_form, poems, context_map, num_samples=3)
    result['sample_contexts'] = contexts_str
    result['context_poem_ids'] = poem_ids_str

    # Needs review flag (ambiguous + high frequency)
    result['needs_review'] = result['is_ambiguous'] and result['total_occurrences'] > 100

    return result


def generate_csv(corpus, poems, context_map, top_n=20000, output_path='wordform_review_20k.csv'):
    """Generate the word-form review CSV"""

    print(f"\nGenerating word-form review CSV (top {top_n:,} word forms)...")

    words_data = corpus.get('words', {})

    # Get all word forms with their total occurrences
    word_form_freq = []
    for word_form, word_data in words_data.items():
        total = word_data.get('total_count', 0)
        word_form_freq.append((word_form, total))

    # Sort by frequency descending
    word_form_freq.sort(key=lambda x: x[1], reverse=True)

    # Take top N
    top_word_forms = word_form_freq[:top_n]
    print(f"  Selected top {len(top_word_forms):,} word forms")

    # Define CSV columns
    columns = [
        'word_form',
        'total_occurrences',
        'num_poems',
        'primary_lemma',
        'all_lemmas',
        'num_lemmas',
        'pos_tags',
        'morph_forms',
        'avg_confidence',
        'min_confidence',
        'max_confidence',
        'primary_method',
        'validation_status',
        'is_ambiguous',
        'needs_review',
        'sample_contexts',
        'context_poem_ids',
        'word_length',
        'lemma_length'
    ]

    # Process all word forms
    rows = []
    for idx, (word_form, freq) in enumerate(top_word_forms, 1):
        if idx % 1000 == 0:
            print(f"  Processed {idx:,} / {len(top_word_forms):,} ({idx/len(top_word_forms)*100:.1f}%)")

        word_data = words_data[word_form]
        row = analyze_word_form(word_form, word_data, poems, context_map)
        rows.append(row)

    # Write CSV
    print(f"\nWriting CSV to {output_path}...")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ CSV written with {len(rows):,} word forms")

    # Print statistics
    print(f"\nStatistics:")
    print(f"  Total word forms: {len(rows):,}")
    print(f"  Ambiguous word forms: {sum(1 for r in rows if r['is_ambiguous']):,}")
    print(f"  Need review: {sum(1 for r in rows if r['needs_review']):,}")
    print(f"  Validated (valid): {sum(1 for r in rows if r['validation_status'] == 'valid'):,}")
    print(f"  Validated (invalid): {sum(1 for r in rows if r['validation_status'] == 'invalid'):,}")

    # Frequency coverage
    total_occurrences = sum(r['total_occurrences'] for r in rows)
    corpus_total = sum(wd.get('total_count', 0) for wd in words_data.values())
    coverage = (total_occurrences / corpus_total * 100) if corpus_total > 0 else 0
    print(f"  Corpus coverage: {coverage:.1f}% ({total_occurrences:,} / {corpus_total:,} word instances)")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate word-form review CSV for LLM validation')
    parser.add_argument('--corpus', default='corpus_validation_improved.json.gz',
                       help='Path to corpus JSON file (default: corpus_validation_improved.json.gz)')
    parser.add_argument('--poems', default='poems_index.json.gz',
                       help='Path to poems index file (default: poems_index.json.gz)')
    parser.add_argument('--output', default='wordform_review_20k.csv',
                       help='Output CSV file path (default: wordform_review_20k.csv)')
    parser.add_argument('--top-n', type=int, default=20000,
                       help='Number of top word forms to include (default: 20000)')

    args = parser.parse_args()

    # Load corpus
    corpus = load_corpus(args.corpus)

    # Load poems index
    poems = load_poems_index(args.poems)

    # Build context mapping
    context_map = build_context_mapping(poems)

    # Generate CSV
    generate_csv(corpus, poems, context_map, top_n=args.top_n, output_path=args.output)

    print(f"\n✓ Done! CSV file: {args.output}")
    print(f"\nUsage for LLM validation:")
    print(f"  1. Open CSV in spreadsheet software")
    print(f"  2. Filter/sort by needs_review=TRUE or is_ambiguous=TRUE")
    print(f"  3. Send batches of 50-100 rows to Claude for (word_form, lemma) validation")
    print(f"  4. Claude sees: word form + current lemma + contexts + quality indicators")
    print(f"  5. Claude validates: 'Is this lemma correct for this word form?'")


if __name__ == '__main__':
    main()
