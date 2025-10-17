#!/usr/bin/env python3
"""
Advanced analysis examples for Estonian Runosong Morphological Corpus

This script demonstrates more sophisticated linguistic analysis:
- POS tag distribution and patterns
- Morphological form analysis
- Quality assessment
- Method performance comparison
- Dialectal variation detection
"""

import json
import gzip
import sqlite3
from collections import Counter, defaultdict

def analyze_pos_patterns(corpus):
    """Analyze part-of-speech tag patterns in the corpus"""
    print("\n" + "="*60)
    print("POS TAG ANALYSIS")
    print("="*60)

    pos_counter = Counter()
    pos_by_method = defaultdict(Counter)

    for word, data in corpus['words'].items():
        for pos, count in data['pos_tags'].items():
            pos_counter[pos] += count

            # Track which methods produce which POS tags
            for method in data['methods']:
                pos_by_method[method][pos] += count

    total = sum(pos_counter.values())

    print("\nPOS tag distribution:")
    for pos, count in pos_counter.most_common(15):
        percentage = (count / total) * 100
        print(f"  {pos:10s}: {count:>8,} ({percentage:>5.2f}%)")

    print("\nPOS diversity by processing method:")
    for method in ['estnltk+dict', 'estnltk', 'dict', 'manual_override']:
        if method in pos_by_method:
            unique_pos = len(pos_by_method[method])
            total_method = sum(pos_by_method[method].values())
            print(f"  {method:20s}: {unique_pos:2d} different POS tags ({total_method:>8,} words)")

def analyze_morphological_forms(corpus):
    """Analyze morphological form patterns"""
    print("\n" + "="*60)
    print("MORPHOLOGICAL FORM ANALYSIS")
    print("="*60)

    form_counter = Counter()
    forms_per_word = []

    for word, data in corpus['words'].items():
        num_forms = len(data.get('forms', {}))
        forms_per_word.append(num_forms)

        for form, count in data.get('forms', {}).items():
            form_counter[form] += count

    print("\nMost common morphological forms:")
    for form, count in form_counter.most_common(20):
        print(f"  {form:15s}: {count:>8,}")

    avg_forms = sum(forms_per_word) / len(forms_per_word) if forms_per_word else 0
    print(f"\nAverage forms per word: {avg_forms:.2f}")
    print(f"Words with multiple forms: {sum(1 for f in forms_per_word if f > 1):,}")

def analyze_quality_vs_frequency(corpus):
    """Analyze relationship between quality tiers and word frequency"""
    print("\n" + "="*60)
    print("QUALITY VS FREQUENCY ANALYSIS")
    print("="*60)

    quality_stats = defaultdict(lambda: {'count': 0, 'total_freq': 0, 'high_freq': 0})

    for word, data in corpus['words'].items():
        quality = data['quality']
        freq = data['total_count']

        quality_stats[quality]['count'] += 1
        quality_stats[quality]['total_freq'] += freq
        if freq > 100:
            quality_stats[quality]['high_freq'] += 1

    print("\nQuality tier statistics:")
    for quality in ['high_confidence', 'medium_confidence', 'low_confidence', 'needs_review']:
        if quality in quality_stats:
            stats = quality_stats[quality]
            avg_freq = stats['total_freq'] / stats['count'] if stats['count'] > 0 else 0
            print(f"\n  {quality}:")
            print(f"    Unique words: {stats['count']:,}")
            print(f"    Total instances: {stats['total_freq']:,}")
            print(f"    Average frequency: {avg_freq:.1f}")
            print(f"    High-frequency words (>100): {stats['high_freq']:,}")

def compare_method_performance(corpus):
    """Compare performance of different processing methods"""
    print("\n" + "="*60)
    print("METHOD PERFORMANCE COMPARISON")
    print("="*60)

    method_stats = defaultdict(lambda: {
        'words': 0,
        'instances': 0,
        'avg_confidence': [],
        'quality_dist': Counter()
    })

    for word, data in corpus['words'].items():
        for method, count in data['methods'].items():
            method_stats[method]['words'] += 1
            method_stats[method]['instances'] += count
            method_stats[method]['avg_confidence'].append(data['avg_confidence'])
            method_stats[method]['quality_dist'][data['quality']] += 1

    print("\nMethod performance summary:")
    for method in sorted(method_stats.keys(), key=lambda m: method_stats[m]['instances'], reverse=True):
        stats = method_stats[method]
        avg_conf = sum(stats['avg_confidence']) / len(stats['avg_confidence']) if stats['avg_confidence'] else 0

        print(f"\n  {method}:")
        print(f"    Unique words: {stats['words']:,}")
        print(f"    Total instances: {stats['instances']:,}")
        print(f"    Average confidence: {avg_conf:.3f}")
        print(f"    Quality distribution:")
        for quality, count in stats['quality_dist'].most_common():
            pct = (count / stats['words']) * 100
            print(f"      {quality:20s}: {count:>6,} ({pct:>5.1f}%)")

def find_dialectal_variants(corpus, lemma):
    """Find potential dialectal variants for a given lemma"""
    print("\n" + "="*60)
    print(f"DIALECTAL VARIANTS ANALYSIS: {lemma}")
    print("="*60)

    if lemma not in corpus['lemma_index']:
        print(f"Lemma '{lemma}' not found")
        return

    variants = corpus['lemma_index'][lemma]

    print(f"\nFound {len(variants)} variants:")
    variant_data = []
    for variant in variants:
        if variant in corpus['words']:
            data = corpus['words'][variant]
            variant_data.append({
                'form': variant,
                'count': data['total_count'],
                'confidence': data['avg_confidence'],
                'methods': list(data['methods'].keys()),
                'forms': list(data.get('forms', {}).keys())
            })

    # Sort by frequency
    variant_data.sort(key=lambda x: x['count'], reverse=True)

    for v in variant_data[:20]:  # Show top 20
        print(f"\n  {v['form']:15s} (freq: {v['count']:>5,}, conf: {v['confidence']:.3f})")
        print(f"    Methods: {', '.join(v['methods'])}")
        print(f"    Forms: {', '.join(v['forms'][:5])}")

def analyze_ambiguity_patterns(corpus):
    """Analyze patterns in ambiguous words"""
    print("\n" + "="*60)
    print("AMBIGUITY PATTERN ANALYSIS")
    print("="*60)

    ambiguous = corpus.get('ambiguous_words', {})

    competing_counts = Counter()
    high_freq_ambiguous = []

    for word, data in ambiguous.items():
        num_competing = len(data['competing_lemmas'])
        competing_counts[num_competing] += 1

        if word in corpus['words']:
            freq = corpus['words'][word]['total_count']
            if freq > 50:
                high_freq_ambiguous.append((word, freq, data['competing_lemmas']))

    print("\nDistribution of competing lemmas:")
    for num, count in sorted(competing_counts.items()):
        print(f"  {num} competing lemmas: {count:,} words")

    print(f"\nHigh-frequency ambiguous words (>50 occurrences): {len(high_freq_ambiguous)}")

    high_freq_ambiguous.sort(key=lambda x: x[1], reverse=True)
    print("\nTop 10 high-frequency ambiguous words:")
    for word, freq, lemmas in high_freq_ambiguous[:10]:
        print(f"  {word:15s} (freq: {freq:>5,})")
        for lemma, count in sorted(lemmas.items(), key=lambda x: x[1], reverse=True):
            print(f"    → {lemma}: {count} instances")

def main():
    """Run advanced analyses"""
    print("Loading corpus...")
    with gzip.open('../corpus_runosongs_v2_corrected_FIXED.json.gz', 'rt', encoding='utf-8') as f:
        corpus = json.load(f)
    print(f"✅ Loaded corpus with {len(corpus['words']):,} unique words")

    # Run analyses
    analyze_pos_patterns(corpus)
    analyze_morphological_forms(corpus)
    analyze_quality_vs_frequency(corpus)
    compare_method_performance(corpus)
    find_dialectal_variants(corpus, 'piir')
    analyze_ambiguity_patterns(corpus)

    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)

if __name__ == '__main__':
    main()
