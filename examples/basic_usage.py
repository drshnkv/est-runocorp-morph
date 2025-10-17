#!/usr/bin/env python3
"""
Basic usage examples for Estonian Runosong Morphological Corpus

This script demonstrates fundamental operations with the corpus:
- Loading the JSON corpus
- Looking up word forms
- Finding lemma variants
- Analyzing ambiguous words
- Extracting statistics
"""

import json
import gzip
from collections import Counter

def load_corpus(path='../corpus_runosongs_v2_corrected_FIXED.json.gz'):
    """Load the compressed JSON corpus"""
    print(f"Loading corpus from {path}...")
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"✅ Loaded corpus with {len(corpus['words']):,} unique word forms")
    return corpus

def lookup_word(corpus, word):
    """Look up detailed information about a specific word"""
    if word not in corpus['words']:
        print(f"❌ Word '{word}' not found in corpus")
        return None

    data = corpus['words'][word]
    print(f"\n📝 Word: {word}")
    print(f"  Lemmas: {data['lemmas']}")
    print(f"  POS tags: {data['pos_tags']}")
    print(f"  Morphological forms: {data['forms']}")
    print(f"  Processing methods: {data['methods']}")
    print(f"  Total occurrences: {data['total_count']}")
    print(f"  Average confidence: {data['avg_confidence']:.3f}")
    print(f"  Quality tier: {data['quality']}")
    print(f"  Source poems: {len(data.get('source_poems', []))} poems")
    return data

def find_lemma_variants(corpus, lemma):
    """Find all word forms for a given lemma"""
    if lemma not in corpus['lemma_index']:
        print(f"❌ Lemma '{lemma}' not found in corpus")
        return []

    variants = corpus['lemma_index'][lemma]
    print(f"\n🔍 Variants of lemma '{lemma}':")
    for variant in variants:
        if variant in corpus['words']:
            count = corpus['words'][variant]['total_count']
            print(f"  {variant}: {count} occurrences")
    return variants

def analyze_ambiguous(corpus, word):
    """Check if a word has ambiguous lemmatization"""
    ambiguous = corpus.get('ambiguous_words', {})
    if word not in ambiguous:
        print(f"✅ Word '{word}' is not ambiguous")
        return None

    data = ambiguous[word]
    print(f"\n⚠️  Word '{word}' is ambiguous:")
    print(f"  Competing lemmas: {data['competing_lemmas']}")
    print(f"  Needs review: {data['needs_review']}")
    return data

def get_corpus_statistics(corpus):
    """Extract overall corpus statistics"""
    words = corpus['words']

    # Count total word instances
    total_instances = sum(w['total_count'] for w in words.values())

    # Count POS tags
    all_pos = Counter()
    for word_data in words.values():
        for pos, count in word_data['pos_tags'].items():
            all_pos[pos] += count

    # Count quality tiers
    quality_dist = Counter(w['quality'] for w in words.values())

    print("\n📊 Corpus Statistics:")
    print(f"  Total word instances: {total_instances:,}")
    print(f"  Unique word forms: {len(words):,}")
    print(f"  Unique lemmas: {len(corpus['lemma_index']):,}")

    print("\n  POS distribution:")
    for pos, count in all_pos.most_common(10):
        percentage = (count / total_instances) * 100
        print(f"    {pos}: {count:,} ({percentage:.1f}%)")

    print("\n  Quality distribution:")
    for quality, count in quality_dist.most_common():
        percentage = (count / len(words)) * 100
        print(f"    {quality}: {count:,} ({percentage:.1f}%)")

def main():
    """Run example analyses"""
    # Load corpus
    corpus = load_corpus()

    # Example 1: Look up a specific word
    lookup_word(corpus, 'piiri')

    # Example 2: Find all variants of a lemma
    find_lemma_variants(corpus, 'piir')

    # Example 3: Check ambiguous words
    analyze_ambiguous(corpus, 'kand')

    # Example 4: Get overall statistics
    get_corpus_statistics(corpus)

    # Example 5: Find high-confidence words with specific POS
    print("\n🔎 Sample nouns with high confidence:")
    count = 0
    for word, data in corpus['words'].items():
        if data['quality'] == 'high_confidence' and 'S' in data['pos_tags']:
            print(f"  {word} → {list(data['lemmas'].keys())[0]}")
            count += 1
            if count >= 10:
                break

if __name__ == '__main__':
    main()
