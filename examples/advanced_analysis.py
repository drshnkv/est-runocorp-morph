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

    # Use method_analytics from corpus if available
    if 'method_analytics' in corpus:
        print("\nMethod distribution (from corpus analytics):")
        metadata = corpus.get('metadata', {})
        for method, data in sorted(corpus['method_analytics'].items(),
                                  key=lambda x: -x[1]['total_uses'])[:10]:
            pct = 100 * data['total_uses'] / metadata.get('total_words', 1)
            print(f"  {method:20s}: {data['total_uses']:>8,} ({pct:>5.1f}%) "
                  f"[conf: {data['avg_confidence']:.3f}]")

            # Show POS distribution for this method
            if 'by_pos' in data and data['by_pos']:
                top_pos = sorted(data['by_pos'].items(), key=lambda x: -x[1]['count'])[:5]
                pos_str = ', '.join(f"{pos}({stats['count']:,})" for pos, stats in top_pos)
                print(f"    Top POS: {pos_str}")
    else:
        # Fallback: aggregate from words
        pos_counter = Counter()
        pos_by_method = defaultdict(Counter)

        for word, data in corpus['words'].items():
            for lemma in data['lemmas']:
                # POS tags are nested by lemma
                pos_tags = data['pos_tags'].get(lemma, {})
                for pos, count in pos_tags.items():
                    pos_counter[pos] += count

                    # Methods are also nested by lemma
                    methods = data['methods'].get(lemma, {})
                    for method, method_count in methods.items():
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

    # Use morphological_patterns from corpus if available
    if 'morphological_patterns' in corpus:
        print("\nMost common morphological forms (from corpus analytics):")
        for form, data in list(corpus['morphological_patterns'].items())[:20]:
            print(f"  {form:15s}: {data['total_count']:>8,}")
            # Show top methods for this form
            if 'methods_used' in data:
                method_str = ', '.join(f"{m}({p:.0f}%)" for m, p in
                                      sorted(data['methods_used'].items(), key=lambda x: -x[1])[:3])
                print(f"    Methods: {method_str}")
    else:
        # Fallback: aggregate from words
        form_counter = Counter()
        forms_per_word = []

        for word, data in corpus['words'].items():
            for lemma in data['lemmas']:
                # Forms are nested by lemma
                forms = data.get('forms', {}).get(lemma, {})
                num_forms = len(forms)
                forms_per_word.append(num_forms)

                for form, count in forms.items():
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

    # Use quality_tiers from corpus if available
    if 'quality_tiers' in corpus:
        print("\nQuality tier statistics (from corpus analytics):")
        for tier, data in corpus['quality_tiers'].items():
            print(f"\n  {tier}:")
            print(f"    Unique words: {data['count']:,} ({data['percentage']:.1f}%)")

            # Show sample high-frequency words
            if 'examples' in data and data['examples']:
                print(f"    Top examples:")
                for example in data['examples'][:5]:
                    print(f"      {example['word']:15s}: {example['occurrences']:>6,} occ, "
                          f"conf={example['avg_confidence']:.3f}")
    else:
        # Fallback: calculate from words
        quality_stats = defaultdict(lambda: {'count': 0, 'total_freq': 0, 'high_freq': 0})

        for word, data in corpus['words'].items():
            # Calculate average confidence to determine quality
            total_conf = 0
            total_count = 0
            for lemma in data['lemmas']:
                conf_stats = data['confidences'].get(lemma, {})
                if 'avg' in conf_stats and 'count' in conf_stats:
                    total_conf += conf_stats['avg'] * conf_stats['count']
                    total_count += conf_stats['count']

            avg_conf = total_conf / total_count if total_count > 0 else 0.0
            freq = data['total_count']

            # Determine quality tier
            if avg_conf >= 0.9:
                quality = 'high_confidence'
            elif avg_conf >= 0.7:
                quality = 'medium_confidence'
            elif avg_conf >= 0.5:
                quality = 'low_confidence'
            else:
                quality = 'needs_review'

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

    # Use method_analytics directly if available
    if 'method_analytics' in corpus:
        print("\nMethod performance (from corpus analytics):")
        metadata = corpus.get('metadata', {})
        for method, data in sorted(corpus['method_analytics'].items(),
                                  key=lambda x: -x[1]['total_uses']):
            pct = 100 * data['total_uses'] / metadata.get('total_words', 1)
            print(f"\n  {method}:")
            print(f"    Total uses: {data['total_uses']:,} ({pct:.1f}%)")
            print(f"    Average confidence: {data['avg_confidence']:.3f}")

            # Confidence distribution
            if 'confidence_distribution' in data:
                conf_dist = data['confidence_distribution']
                print(f"    Confidence: high={conf_dist['high']:.1f}%, "
                      f"medium={conf_dist['medium']:.1f}%, "
                      f"low={conf_dist['low']:.1f}%")

            # Top POS
            if 'by_pos' in data and data['by_pos']:
                top_pos = sorted(data['by_pos'].items(), key=lambda x: -x[1]['count'])[:3]
                print(f"    Top POS: {', '.join(f'{pos}({stats['count']:,})' for pos, stats in top_pos)}")
    else:
        print("\nMethod analytics not available in corpus")

def find_dialectal_variants(corpus, lemma):
    """Find potential dialectal variants for a given lemma"""
    print("\n" + "="*60)
    print(f"DIALECTAL VARIANTS ANALYSIS: {lemma}")
    print("="*60)

    if lemma not in corpus['lemma_index']:
        print(f"Lemma '{lemma}' not found")
        return

    lemma_data = corpus['lemma_index'][lemma]
    word_forms = lemma_data['word_forms']

    print(f"\nTotal occurrences: {lemma_data['total_occurrences']:,}")
    print(f"Found {len(word_forms)} word form variants")

    # Get form distribution
    form_dist = lemma_data.get('form_distribution', {})

    # Sort by frequency
    sorted_forms = sorted(form_dist.items(), key=lambda x: -x[1]['count'])

    print(f"\nTop 20 variants by frequency:")
    for word_form, stats in sorted_forms[:20]:
        print(f"\n  {word_form:15s} (freq: {stats['count']:>5,}, conf: {stats['confidence_avg']:.3f})")
        print(f"    Morphological forms: {', '.join(stats['forms'][:5]) if stats['forms'] else 'N/A'}")

def analyze_ambiguity_patterns(corpus):
    """Analyze patterns in ambiguous words"""
    print("\n" + "="*60)
    print("AMBIGUITY PATTERN ANALYSIS")
    print("="*60)

    ambiguous = corpus.get('ambiguous_words', {})

    competing_counts = Counter()
    high_freq_ambiguous = []

    for word, data in ambiguous.items():
        num_competing = len(data['lemma_competition'])
        competing_counts[num_competing] += 1

        freq = data['total_occurrences']
        if freq > 50:
            high_freq_ambiguous.append((word, freq, data['lemma_competition']))

    print("\nDistribution of competing lemmas:")
    for num, count in sorted(competing_counts.items()):
        print(f"  {num} competing lemmas: {count:,} words")

    print(f"\nHigh-frequency ambiguous words (>50 occurrences): {len(high_freq_ambiguous)}")

    high_freq_ambiguous.sort(key=lambda x: x[1], reverse=True)
    print("\nTop 10 high-frequency ambiguous words:")
    for word, freq, lemma_comp in high_freq_ambiguous[:10]:
        print(f"  {word:15s} (freq: {freq:>5,})")
        for lemma, stats in sorted(lemma_comp.items(), key=lambda x: -x[1]['chosen']):
            if stats['chosen'] > 0:
                print(f"    → {lemma}: chosen {stats['chosen']}x, "
                      f"conf={stats['confidence_avg']:.3f}")

def main():
    """Run advanced analyses"""
    print("Loading corpus...")
    with gzip.open('../corpus_unknown_reduced.json.gz', 'rt', encoding='utf-8') as f:
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
