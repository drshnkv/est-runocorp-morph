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
    print(f"  Total occurrences: {data['total_count']}")
    print(f"  Lemmas: {data['lemmas']}")

    # Show details for each lemma
    for lemma in data['lemmas']:
        print(f"\n  Lemma '{lemma}':")
        print(f"    Count: {data['lemma_counts'].get(lemma, 0)}")

        # Confidence stats
        conf_stats = data['confidences'].get(lemma, {})
        if conf_stats:
            print(f"    Confidence: avg={conf_stats.get('avg', 0):.3f}, "
                  f"min={conf_stats.get('min', 0):.3f}, "
                  f"max={conf_stats.get('max', 0):.3f}")

        # POS tags
        pos_tags = data['pos_tags'].get(lemma, {})
        if pos_tags:
            print(f"    POS tags: {pos_tags}")

        # Morphological forms
        forms = data['forms'].get(lemma, {})
        if forms:
            print(f"    Forms: {forms}")

        # Methods
        methods = data['methods'].get(lemma, {})
        if methods:
            print(f"    Methods: {methods}")

    print(f"\n  First seen: {data.get('first_seen', 'N/A')}")
    print(f"  Last seen: {data.get('last_seen', 'N/A')}")
    print(f"  Source poems: {len(data.get('source_poems', []))} poems")

    return data

def find_lemma_variants(corpus, lemma):
    """Find all word forms for a given lemma"""
    if lemma not in corpus['lemma_index']:
        print(f"❌ Lemma '{lemma}' not found in corpus")
        return []

    lemma_data = corpus['lemma_index'][lemma]
    print(f"\n🔍 Variants of lemma '{lemma}':")
    print(f"  Total occurrences: {lemma_data['total_occurrences']:,}")
    print(f"  Word forms: {len(lemma_data['word_forms'])}")

    # Show form distribution
    print(f"\n  Form distribution:")
    form_dist = lemma_data.get('form_distribution', {})
    for word_form, stats in sorted(form_dist.items(), key=lambda x: -x[1]['count'])[:10]:
        print(f"    {word_form}: {stats['count']} occurrences, "
              f"avg_conf={stats['confidence_avg']:.3f}, "
              f"forms={stats['forms']}")

    return lemma_data['word_forms']

def analyze_ambiguous(corpus, word):
    """Check if a word has ambiguous lemmatization"""
    ambiguous = corpus.get('ambiguous_words', {})
    if word not in ambiguous:
        print(f"✅ Word '{word}' is not ambiguous")
        return None

    data = ambiguous[word]
    print(f"\n⚠️  Word '{word}' is ambiguous:")
    print(f"  Total occurrences: {data['total_occurrences']}")
    print(f"  Needs review: {data['needs_review']}")

    print(f"\n  Lemma competition:")
    for lemma, stats in sorted(data['lemma_competition'].items(),
                               key=lambda x: -x[1]['chosen']):
        print(f"    {lemma}: chosen {stats['chosen']}x, "
              f"rejected {stats['rejected']}x, "
              f"avg_conf={stats['confidence_avg']:.3f}")

    if data.get('alternatives_seen'):
        print(f"\n  Alternative lemmas seen: {data['alternatives_seen']}")

    return data

def get_corpus_statistics(corpus):
    """Extract overall corpus statistics"""
    metadata = corpus.get('metadata', {})
    words = corpus['words']

    print("\n📊 Corpus Statistics:")
    print(f"  Total word instances: {metadata.get('total_words', 0):,}")
    print(f"  Unique word forms: {len(words):,}")
    print(f"  Unique lemmas: {len(corpus['lemma_index']):,}")

    # Method analytics
    if 'method_analytics' in corpus:
        print("\n  Method distribution:")
        for method, data in sorted(corpus['method_analytics'].items(),
                                  key=lambda x: -x[1]['total_uses'])[:10]:
            pct = 100 * data['total_uses'] / metadata.get('total_words', 1)
            print(f"    {method:20s}: {data['total_uses']:>8,} ({pct:>5.1f}%) "
                  f"[conf: {data['avg_confidence']:.3f}]")

    # Quality tiers
    if 'quality_tiers' in corpus:
        print("\n  Quality distribution:")
        for tier, data in corpus['quality_tiers'].items():
            print(f"    {tier:20s}: {data['count']:>8,} ({data['percentage']:>5.1f}%)")

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
    print("\n🔎 Sample nouns (POS=S) with high avg confidence:")
    count = 0
    for word, data in corpus['words'].items():
        # Calculate average confidence
        total_conf = 0
        total_count = 0
        has_noun = False

        for lemma in data['lemmas']:
            conf_stats = data['confidences'].get(lemma, {})
            if 'avg' in conf_stats and 'count' in conf_stats:
                total_conf += conf_stats['avg'] * conf_stats['count']
                total_count += conf_stats['count']

            # Check if any lemma has POS=S
            pos_tags = data['pos_tags'].get(lemma, {})
            if 'S' in pos_tags:
                has_noun = True

        avg_conf = total_conf / total_count if total_count > 0 else 0.0

        if has_noun and avg_conf >= 0.9:
            print(f"  {word} → {data['lemmas'][0]} (conf: {avg_conf:.3f})")
            count += 1
            if count >= 10:
                break

if __name__ == '__main__':
    main()
