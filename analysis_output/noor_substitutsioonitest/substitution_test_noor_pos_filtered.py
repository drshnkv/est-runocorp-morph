#!/usr/bin/env python3
"""
IMPROVED Substitution Test with POS filtering and aggregation.

Improvements over basic version:
1. Filter candidates to match target POS (only adjectives/nouns for 'noor')
2. Aggregate all shared templates per candidate lemma
3. Calculate multiple synonym scores
4. Include POS distribution info
"""

import json
import gzip
import csv
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime


# Target lemmas
TARGET_LEMMAS = {'noor', 'nooruke', 'nooreke'}

# POS codes that 'noor' typically has (A=adjective, S=noun)
TARGET_POS = {'A', 'S'}


def load_poems_index_v2(filepath: Path) -> dict:
    """Load the v2 poems index with verse structure."""
    print(f"Loading {filepath}...")
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    print(f"  Loaded {len(data['poems']):,} poems")
    return data


def analyze_lemma_pos_distribution(poems_v2: dict) -> Dict[str, Counter]:
    """
    Build POS distribution for each lemma.
    Returns: {lemma: Counter({pos: count})}
    """
    print("\nAnalyzing POS distribution for all lemmas...")

    lemma_pos = defaultdict(Counter)
    poems = poems_v2['poems']

    for i, (poem_id, poem) in enumerate(poems.items()):
        if i % 30000 == 0:
            print(f"  Processing poem {i:,}/{len(poems):,}...")

        if poem.get('is_empty', False):
            continue

        for word in poem.get('words', []):
            lemma = word.get('lemma', '')
            pos = word.get('pos', '')
            if lemma and pos:
                lemma_pos[lemma][pos] += 1

    print(f"  Analyzed POS for {len(lemma_pos):,} lemmas")
    return lemma_pos


def get_primary_pos(pos_counter: Counter) -> str:
    """Get the most common POS for a lemma."""
    if not pos_counter:
        return ''
    return pos_counter.most_common(1)[0][0]


def build_templates_with_pos(poems_v2: dict, lemma_pos: Dict[str, Counter]) -> Tuple[Dict, Dict, Dict]:
    """
    Build template database with POS information.

    Returns:
        lemma_templates: {lemma: Counter of templates}
        template_lemmas: {template: set of lemmas}
        lemma_template_pos: {lemma: {template: Counter of POS used}}
    """
    print("\nBuilding POS-aware template database...")

    lemma_templates = defaultdict(Counter)
    template_lemmas = defaultdict(set)
    lemma_template_pos = defaultdict(lambda: defaultdict(Counter))

    poems = poems_v2['poems']

    for i, (poem_id, poem) in enumerate(poems.items()):
        if i % 30000 == 0:
            print(f"  Processing poem {i:,}/{len(poems):,}...")

        if poem.get('is_empty', False):
            continue

        words = poem.get('words', [])

        # Group by verse
        verses = defaultdict(list)
        for w in words:
            v_idx = w.get('verse_index', -1)
            if v_idx >= 0:
                verses[v_idx].append(w)

        for v_idx, v_words in verses.items():
            if len(v_words) < 2:
                continue

            originals = [w.get('original', '') for w in v_words]
            lemmas = [w.get('lemma', '') for w in v_words]
            pos_tags = [w.get('pos', '') for w in v_words]

            for pos_idx, lemma in enumerate(lemmas):
                if not lemma:
                    continue

                pos = pos_tags[pos_idx]

                # Create template
                template_words = originals.copy()
                template_words[pos_idx] = '___'
                template = ' '.join(template_words)

                lemma_templates[lemma][template] += 1
                template_lemmas[template].add(lemma)
                lemma_template_pos[lemma][template][pos] += 1

    print(f"  Built templates for {len(lemma_templates):,} lemmas")
    return lemma_templates, template_lemmas, lemma_template_pos


def find_pos_filtered_synonyms(
    target_lemmas: Set[str],
    target_pos: Set[str],
    lemma_templates: Dict[str, Counter],
    template_lemmas: Dict[str, Set[str]],
    lemma_pos: Dict[str, Counter],
    lemma_template_pos: Dict,
    min_shared: int = 2
) -> List[dict]:
    """
    Find substitutable lemmas filtered by POS match.
    Aggregates all templates per candidate.
    """
    print(f"\nFinding POS-filtered substitutable lemmas...")
    print(f"  Target lemmas: {target_lemmas}")
    print(f"  Target POS filter: {target_pos}")

    # Show target POS distribution
    print(f"\n  Target lemma POS distributions:")
    for target in sorted(target_lemmas):
        if target in lemma_pos:
            print(f"    '{target}': {dict(lemma_pos[target].most_common(5))}")

    # Combine templates from all target lemmas
    target_templates = Counter()
    for target in target_lemmas:
        if target in lemma_templates:
            target_templates.update(lemma_templates[target])

    print(f"\n  Combined target templates: {len(target_templates):,}")

    # Find all candidate lemmas that share templates
    candidate_lemmas = set()
    for template in target_templates:
        candidate_lemmas.update(template_lemmas[template])
    candidate_lemmas -= target_lemmas

    print(f"  Total candidate lemmas: {len(candidate_lemmas):,}")

    # Filter by POS and aggregate
    results = []
    pos_filtered_count = 0

    for candidate in candidate_lemmas:
        # Get candidate's primary POS
        candidate_primary_pos = get_primary_pos(lemma_pos.get(candidate, Counter()))

        # Check if POS matches target
        if candidate_primary_pos not in target_pos:
            pos_filtered_count += 1
            continue

        candidate_temps = lemma_templates[candidate]

        # Find shared templates
        shared_templates = []
        total_target_in_shared = 0
        total_candidate_in_shared = 0

        for template, target_count in target_templates.items():
            if template in candidate_temps:
                candidate_count = candidate_temps[template]
                shared_templates.append({
                    'template': template,
                    'target_count': target_count,
                    'candidate_count': candidate_count
                })
                total_target_in_shared += target_count
                total_candidate_in_shared += candidate_count

        if len(shared_templates) >= min_shared:
            # Calculate aggregated scores

            # Jaccard similarity (set-based)
            jaccard = len(shared_templates) / (
                len(target_templates) + len(candidate_temps) - len(shared_templates)
            )

            # Dice coefficient (more weight to shared)
            dice = 2 * len(shared_templates) / (len(target_templates) + len(candidate_temps))

            # Weighted overlap (by occurrences)
            total_target_occ = sum(target_templates.values())
            total_candidate_occ = sum(candidate_temps.values())
            weighted_overlap = (total_target_in_shared + total_candidate_in_shared) / (
                total_target_occ + total_candidate_occ
            )

            # PMI-like score (pointwise mutual information approximation)
            # How much more likely to co-occur than by chance
            p_shared = len(shared_templates) / len(template_lemmas)
            p_target = len(target_templates) / len(template_lemmas)
            p_candidate = len(candidate_temps) / len(template_lemmas)
            pmi = p_shared / (p_target * p_candidate) if p_target * p_candidate > 0 else 0

            results.append({
                'lemma': candidate,
                'primary_pos': candidate_primary_pos,
                'pos_distribution': dict(lemma_pos[candidate].most_common(3)),
                'shared_template_count': len(shared_templates),
                'target_total_templates': len(target_templates),
                'candidate_total_templates': len(candidate_temps),
                'total_target_occurrences_in_shared': total_target_in_shared,
                'total_candidate_occurrences_in_shared': total_candidate_in_shared,
                'jaccard_score': jaccard,
                'dice_score': dice,
                'weighted_overlap': weighted_overlap,
                'pmi_approximation': pmi,
                'shared_templates': shared_templates
            })

    print(f"  Filtered out by POS mismatch: {pos_filtered_count:,}")
    print(f"  Remaining candidates (POS matched): {len(results):,}")

    # Sort by number of shared templates (primary) and dice score (secondary)
    results.sort(key=lambda x: (-x['shared_template_count'], -x['dice_score']))

    return results


def save_aggregated_results(
    results: List[dict],
    target_lemmas: Set[str],
    target_pos: Set[str],
    output_path: Path,
    top_n: int = 100
):
    """Save aggregated, POS-filtered results to CSV."""

    rows = []
    for rank, item in enumerate(results[:top_n], 1):
        # Get top 3 template examples
        top_templates = sorted(
            item['shared_templates'],
            key=lambda x: -(x['target_count'] + x['candidate_count'])
        )[:3]

        template_examples = ' | '.join([
            f"\"{t['template']}\" ({t['target_count']}+{t['candidate_count']})"
            for t in top_templates
        ])

        rows.append({
            'rank': rank,
            'lemma': item['lemma'],
            'primary_pos': item['primary_pos'],
            'pos_distribution': str(item['pos_distribution']),
            'shared_templates': item['shared_template_count'],
            'target_occurrences_in_shared': item['total_target_occurrences_in_shared'],
            'candidate_occurrences_in_shared': item['total_candidate_occurrences_in_shared'],
            'jaccard_score': round(item['jaccard_score'], 6),
            'dice_score': round(item['dice_score'], 6),
            'weighted_overlap': round(item['weighted_overlap'], 6),
            'candidate_total_templates': item['candidate_total_templates'],
            'top_template_examples': template_examples,
        })

    columns = [
        'rank', 'lemma', 'primary_pos', 'pos_distribution',
        'shared_templates', 'target_occurrences_in_shared', 'candidate_occurrences_in_shared',
        'jaccard_score', 'dice_score', 'weighted_overlap',
        'candidate_total_templates', 'top_template_examples'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✓ Saved {len(rows)} POS-filtered results to: {output_path}")


def print_analysis_summary(results: List[dict], target_pos: Set[str]):
    """Print detailed analysis summary."""

    print("\n" + "="*80)
    print("POS-FILTERED SUBSTITUTION ANALYSIS SUMMARY")
    print(f"(Only candidates with POS in {target_pos})")
    print("="*80)

    if not results:
        print("No results found!")
        return

    # Group by POS
    by_pos = defaultdict(list)
    for item in results[:50]:
        by_pos[item['primary_pos']].append(item)

    for pos in sorted(by_pos.keys()):
        items = by_pos[pos]
        print(f"\n--- POS: {pos} ({len(items)} lemmas) ---")

        for item in items[:15]:
            lemma = item['lemma']
            shared = item['shared_template_count']
            dice = item['dice_score']
            target_occ = item['total_target_occurrences_in_shared']
            cand_occ = item['total_candidate_occurrences_in_shared']

            print(f"  {lemma}:")
            print(f"    shared templates: {shared}, dice: {dice:.4f}")
            print(f"    target occurrences: {target_occ:,}, candidate: {cand_occ:,}")

            # Top template
            if item['shared_templates']:
                top = max(item['shared_templates'],
                         key=lambda x: x['target_count'] + x['candidate_count'])
                print(f"    top template: \"{top['template']}\" ({top['target_count']}+{top['candidate_count']})")


def save_full_template_details(
    results: List[dict],
    output_path: Path,
    top_n_lemmas: int = 30
):
    """Save detailed template breakdown for top lemmas."""

    rows = []
    for item in results[:top_n_lemmas]:
        lemma = item['lemma']
        pos = item['primary_pos']

        for t in item['shared_templates']:
            rows.append({
                'candidate_lemma': lemma,
                'candidate_pos': pos,
                'template': t['template'],
                'target_occurrences': t['target_count'],
                'candidate_occurrences': t['candidate_count'],
                'combined_occurrences': t['target_count'] + t['candidate_count'],
                'ratio_target_to_candidate': round(t['target_count'] / max(t['candidate_count'], 1), 2)
            })

    # Sort by combined occurrences
    rows.sort(key=lambda x: -x['combined_occurrences'])

    columns = [
        'candidate_lemma', 'candidate_pos', 'template',
        'target_occurrences', 'candidate_occurrences',
        'combined_occurrences', 'ratio_target_to_candidate'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Saved {len(rows)} detailed templates to: {output_path}")


def main():
    base_dir = Path("/Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/est-runocorp-morph-standalone")

    # Load data
    poems_v2 = load_poems_index_v2(base_dir / "poems_index_v2.json.gz")

    # Analyze POS distribution
    lemma_pos = analyze_lemma_pos_distribution(poems_v2)

    # Build templates with POS info
    lemma_templates, template_lemmas, lemma_template_pos = build_templates_with_pos(
        poems_v2, lemma_pos
    )

    # Find POS-filtered synonyms
    results = find_pos_filtered_synonyms(
        TARGET_LEMMAS,
        TARGET_POS,
        lemma_templates,
        template_lemmas,
        lemma_pos,
        lemma_template_pos,
        min_shared=2
    )

    # Print summary
    print_analysis_summary(results, TARGET_POS)

    # Save results
    output_dir = base_dir / "analysis_output"
    output_dir.mkdir(exist_ok=True)

    # Main aggregated results
    save_aggregated_results(
        results, TARGET_LEMMAS, TARGET_POS,
        output_dir / "substitution_test_noor_POS_FILTERED.csv",
        top_n=100
    )

    # Detailed templates for top lemmas
    save_full_template_details(
        results,
        output_dir / "substitution_test_noor_POS_FILTERED_detailed.csv",
        top_n_lemmas=30
    )

    # Save method explanation
    explanation = f"""# POS-Filtered Substitution Test Results
# Target: {', '.join(sorted(TARGET_LEMMAS))}
# POS Filter: {TARGET_POS}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Column Explanations

### Main Results CSV (substitution_test_noor_POS_FILTERED.csv)

| Column | Description |
|--------|-------------|
| rank | Ranking by shared_templates count |
| lemma | Candidate lemma that can substitute for target |
| primary_pos | Most common POS tag for this lemma |
| pos_distribution | Distribution of POS tags (e.g., {{'A': 500, 'S': 100}}) |
| shared_templates | Number of verse templates shared with target |
| target_occurrences_in_shared | Total times target appears in shared templates |
| candidate_occurrences_in_shared | Total times candidate appears in shared templates |
| jaccard_score | Jaccard similarity: shared / (target_templates + candidate_templates - shared) |
| dice_score | Dice coefficient: 2*shared / (target_templates + candidate_templates) |
| weighted_overlap | Occurrence-weighted overlap score |
| candidate_total_templates | Total unique templates for candidate |
| top_template_examples | Top 3 shared templates with counts |

### Detailed Templates CSV (substitution_test_noor_POS_FILTERED_detailed.csv)

| Column | Description |
|--------|-------------|
| candidate_lemma | The substitute lemma |
| candidate_pos | POS tag of candidate |
| template | The verse template with ___ placeholder |
| target_occurrences | Times target (noor/nooreke/nooruke) fills this template |
| candidate_occurrences | Times candidate fills this template |
| combined_occurrences | Sum of both (for ranking productivity) |
| ratio_target_to_candidate | target_occurrences / candidate_occurrences |

## Interpretation Guide

- **High shared_templates + High dice_score** = Strong synonym/antonym candidate
- **ratio_target_to_candidate ≈ 1** = Equally common in shared contexts
- **ratio >> 1** = Target dominates this template (candidate is rarer variant)
- **ratio << 1** = Candidate dominates (target is rarer in this context)

## POS Filtering Rationale

'noor' functions primarily as:
- **A (adjective)**: "noor mees" (young man)
- **S (noun)**: "noorest nooreni" (from young to young)

By filtering to only A/S candidates, we exclude:
- Verbs (V) that happen to share templates syntactically
- Pronouns (P) and other function words
- Adverbs (D) that occupy similar positions but different semantic roles
"""

    with open(output_dir / "substitution_test_noor_POS_FILTERED_explanation.md", 'w') as f:
        f.write(explanation)

    print(f"\n✓ Saved method explanation")
    print("\n" + "="*80)
    print("✓ POS-filtered analysis complete!")
    print("="*80)


if __name__ == '__main__':
    main()
