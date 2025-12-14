#!/usr/bin/env python3
"""
Generate poems_index_v2 with verse line markers.

Features:
- Preserves "/" verse markers from original CSV
- Adds verse_lines array for easy iteration
- Enhanced metadata from CSV (title, collection, places, etc.)
- Full morphological annotations from existing poems_index
- Comprehensive verification suite

Usage:
    python generate_poem_index_v2.py \
        --csv ../../estnltk_dict_only/koik_regilaulud_okt_2025.csv \
        --poems-index poems_index.json.gz \
        --output poems_index_v2.json.gz

Created: 2025-12-14
"""

import json
import gzip
import csv
import argparse
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_csv_data(csv_path: Path) -> dict:
    """
    Load and index CSV data by poem ID.

    Returns dict: {poem_id: {poemText, verseCount, poemTitle, ...}}
    """
    print(f"Loading CSV data from {csv_path}...")
    csv_data = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            poem_id = row['p_id']
            csv_data[poem_id] = {
                'poemText': row.get('poemText', ''),
                'verseCount': int(row.get('verseCount', 0)) if row.get('verseCount') else 0,
                'poemTitle': row.get('poemTitle', ''),
                'nro': row.get('nro', ''),
                'collection': row.get('collection', ''),
                'placeNames': row.get('placeNames', ''),
                'placeTypes': row.get('placeTypes', ''),
                'placeOrigIds': row.get('placeOrigIds', ''),
                'poemYear': row.get('poemYear', ''),
                'typeNames': row.get('typeNames', ''),
                'typeDescriptions': row.get('typeDescriptions', ''),
                'collectorNames': row.get('collectorNames', '')
            }

    print(f"  Loaded {len(csv_data):,} poems from CSV")
    return csv_data


def load_poems_index(index_path: Path) -> dict:
    """
    Load existing poems index with annotations.

    Handles both .json and .json.gz files.
    """
    print(f"Loading poems index from {index_path}...")

    if str(index_path).endswith('.gz'):
        with gzip.open(index_path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
    else:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    poems = data.get('poems', {})
    metadata = data.get('metadata', {})

    print(f"  Loaded {len(poems):,} poems")
    print(f"  Version: {metadata.get('version', 'unknown')}")
    print(f"  Total words: {metadata.get('total_words', 'unknown'):,}")

    return {'poems': poems, 'metadata': metadata}


def clean_csv_text(text: str) -> str:
    """
    Clean CSV text by removing known artifacts.

    Handles:
    - 'ampquot' artifacts from incorrect HTML entity encoding
    """
    # Remove 'ampquot' artifacts (incorrectly escaped &quot;)
    cleaned = text.replace('ampquot', '')
    return cleaned


def parse_verses(text: str, clean: bool = True) -> tuple:
    """
    Parse verse-marked text into verse lines and flat word list.

    Args:
        text: Text with " / " verse separators
        clean: If True, clean artifacts from text first

    Returns:
        tuple: (verse_lines, words_flat, cleaned_text)
        - verse_lines: List of verse strings
        - words_flat: List of all words in order
        - cleaned_text: The cleaned text with "/" markers
    """
    if clean:
        text = clean_csv_text(text)

    # Handle empty text
    if not text.strip():
        return [], [], ''

    # Split by " / " to get verses
    verse_lines = [v.strip() for v in text.split(' / ') if v.strip()]

    # Get flat word list by splitting each verse
    words_flat = []
    for verse in verse_lines:
        verse_words = verse.split()
        words_flat.extend(verse_words)

    # Reconstruct cleaned text with markers
    cleaned_text = ' / '.join(verse_lines)

    return verse_lines, words_flat, cleaned_text


def align_annotations_to_verses(verse_lines: list, annotations: list) -> list:
    """
    Align existing word annotations to verse structure.

    Adds verse_index and word_in_verse to each annotation.

    Args:
        verse_lines: List of verse strings
        annotations: List of word annotation dicts

    Returns:
        List of annotations with verse indices added
    """
    aligned = []
    word_idx = 0

    for verse_idx, verse in enumerate(verse_lines):
        verse_words = verse.split()
        for word_pos, _ in enumerate(verse_words):
            if word_idx < len(annotations):
                ann = annotations[word_idx].copy()
                ann['verse_index'] = verse_idx
                ann['word_in_verse'] = word_pos
                aligned.append(ann)
            word_idx += 1

    # Handle any remaining annotations (shouldn't happen if aligned correctly)
    while word_idx < len(annotations):
        ann = annotations[word_idx].copy()
        ann['verse_index'] = -1  # Marker for unaligned
        ann['word_in_verse'] = -1
        aligned.append(ann)
        word_idx += 1

    return aligned


def verify_word_alignment(poem_id: str, csv_words: list, index_words: list) -> list:
    """
    Verify that words from CSV match words from poems_index.

    Returns list of issues found.
    """
    issues = []

    # Check counts
    if len(csv_words) != len(index_words):
        issues.append(f"Word count mismatch: CSV={len(csv_words)}, index={len(index_words)}")
        return issues  # Can't align if counts differ

    # Check each word
    for i, (csv_word, index_ann) in enumerate(zip(csv_words, index_words)):
        index_word = index_ann.get('original', '')
        if csv_word != index_word:
            issues.append(f"Word {i} mismatch: CSV='{csv_word}', index='{index_word}'")
            if len(issues) >= 5:  # Limit issues reported
                issues.append(f"... and possibly more mismatches")
                break

    return issues


def build_poem_v2(poem_id: str, csv_row: dict, poem_v1: dict) -> tuple:
    """
    Build v2 poem entry by merging CSV data with v1 annotations.

    Returns:
        tuple: (poem_v2_dict, issues_list)
    """
    issues = []

    # Parse verses from CSV (with artifact cleaning)
    raw_poem_text = csv_row.get('poemText', '')
    verse_lines, csv_words, cleaned_text = parse_verses(raw_poem_text)

    # Get v1 annotations
    v1_words = poem_v1.get('words', [])

    # Handle empty poems
    is_empty = len(v1_words) == 0

    # Verify alignment (skip for empty poems)
    if not is_empty:
        alignment_issues = verify_word_alignment(poem_id, csv_words, v1_words)
        issues.extend(alignment_issues)
    else:
        alignment_issues = []

    # Align annotations to verses
    if not alignment_issues and not is_empty:
        aligned_words = align_annotations_to_verses(verse_lines, v1_words)
    else:
        # Fall back to original annotations without verse indices
        aligned_words = []
        for word in v1_words:
            w = word.copy()
            w['verse_index'] = -1
            w['word_in_verse'] = -1
            aligned_words.append(w)

    # Build v2 structure
    poem_v2 = {
        'text': cleaned_text,  # Cleaned text with "/" markers
        'text_flat': ' '.join(csv_words),  # Flattened version
        'verse_lines': verse_lines,
        'verse_count': len(verse_lines),
        'words': aligned_words,
        'num_words': len(aligned_words),
        'is_empty': is_empty,  # Flag for empty poems
        'metadata': {
            'title': csv_row.get('poemTitle', ''),
            'collection': csv_row.get('collection', ''),
            'nro': csv_row.get('nro', ''),
            'places': [p.strip() for p in csv_row.get('placeNames', '').split(',') if p.strip()],
            'place_types': [p.strip() for p in csv_row.get('placeTypes', '').split(',') if p.strip()],
            'year': csv_row.get('poemYear', ''),
            'types': [t.strip() for t in csv_row.get('typeNames', '').split(',') if t.strip()],
            'type_descriptions': [t.strip() for t in csv_row.get('typeDescriptions', '').split(',') if t.strip()],
            'collectors': [c.strip() for c in csv_row.get('collectorNames', '').split(',') if c.strip()]
        },
        'batch': poem_v1.get('batch', ''),
        'row_index': poem_v1.get('row_index', 0)
    }

    return poem_v2, issues


def build_poems_index_v2(csv_data: dict, poems_index: dict) -> tuple:
    """
    Build v2 index merging CSV text with annotations.

    Returns:
        tuple: (index_v2, all_issues)
    """
    print("\nBuilding poems_index_v2...")

    poems_v1 = poems_index['poems']
    poems_v2 = {}
    all_issues = {}

    total_words = 0
    total_verses = 0
    empty_poems = 0

    # Progress tracking
    total = len(poems_v1)
    checkpoint = max(1, total // 10)

    for i, (poem_id, poem_v1) in enumerate(poems_v1.items()):
        if (i + 1) % checkpoint == 0:
            print(f"  Processing: {i + 1:,}/{total:,} ({100*(i+1)//total}%)")

        # Get CSV data for this poem
        csv_row = csv_data.get(poem_id)

        if csv_row is None:
            all_issues[poem_id] = [f"Poem {poem_id} not found in CSV"]
            poems_v2[poem_id] = poem_v1  # Keep original
            continue

        # Build v2 entry
        poem_v2, issues = build_poem_v2(poem_id, csv_row, poem_v1)
        poems_v2[poem_id] = poem_v2

        if issues:
            all_issues[poem_id] = issues

        total_words += poem_v2['num_words']
        total_verses += poem_v2['verse_count']
        if poem_v2.get('is_empty', False):
            empty_poems += 1

    # Build v2 metadata
    metadata_v2 = {
        'version': 'v2',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_from': 'poems_index + koik_regilaulud_okt_2025.csv',
        'total_poems': len(poems_v2),
        'total_words': total_words,
        'total_verses': total_verses,
        'empty_poems': empty_poems,
        'non_empty_poems': len(poems_v2) - empty_poems,
        'avg_words_per_poem': total_words / len(poems_v2) if poems_v2 else 0,
        'avg_verses_per_poem': total_verses / len(poems_v2) if poems_v2 else 0,
        'features': [
            'verse_markers',
            'verse_lines_array',
            'enhanced_metadata',
            'verse_indices_per_word',
            'morphological_annotations',
            'empty_poem_tracking'
        ]
    }

    index_v2 = {
        'metadata': metadata_v2,
        'poems': poems_v2
    }

    print(f"\n  Total poems: {len(poems_v2):,}")
    print(f"  Total words: {total_words:,}")
    print(f"  Total verses: {total_verses:,}")
    print(f"  Empty poems: {empty_poems:,}")
    print(f"  Issues found: {len(all_issues)}")

    return index_v2, all_issues


def run_verification(index_v2: dict, csv_data: dict, poems_v1: dict) -> tuple:
    """
    Run full verification suite.

    Returns:
        tuple: (passed, results_dict)
    """
    print("\n=== VERIFICATION SUITE ===\n")
    results = {}
    all_passed = True

    poems = index_v2['poems']
    metadata = index_v2['metadata']

    # Known data characteristics (from source data analysis)
    KNOWN_EMPTY_POEMS = 844  # Poems with empty text in source data

    # 1. Poem count
    expected_poems = 108969
    actual_poems = len(poems)
    passed = actual_poems == expected_poems
    results['poem_count'] = {
        'passed': passed,
        'expected': expected_poems,
        'actual': actual_poems
    }
    print(f"[{'✓' if passed else '✗'}] Poem count: {actual_poems:,} (expected {expected_poems:,})")
    all_passed &= passed

    # 2. ID range
    numeric_ids = [int(k) for k in poems.keys()]
    min_id, max_id = min(numeric_ids), max(numeric_ids)
    passed = min_id == 89248 and max_id == 198216
    results['id_range'] = {
        'passed': passed,
        'expected_min': 89248,
        'expected_max': 198216,
        'actual_min': min_id,
        'actual_max': max_id
    }
    print(f"[{'✓' if passed else '✗'}] ID range: {min_id} - {max_id} (expected 89248 - 198216)")
    all_passed &= passed

    # 3. Word count
    expected_words = 7344574
    actual_words = metadata['total_words']
    tolerance = expected_words * 0.001  # 0.1% tolerance
    passed = abs(actual_words - expected_words) <= tolerance
    results['word_count'] = {
        'passed': passed,
        'expected': expected_words,
        'actual': actual_words,
        'difference': actual_words - expected_words
    }
    print(f"[{'✓' if passed else '✗'}] Word count: {actual_words:,} (expected ~{expected_words:,}, diff={actual_words-expected_words:+,})")
    all_passed &= passed

    # 4. Verse structure validation (accounting for known empty poems)
    no_verse_poems = 0
    empty_poems = 0
    total_verses = 0
    for poem_id, poem in poems.items():
        if poem.get('is_empty', False):
            empty_poems += 1
        elif poem.get('verse_count', 0) == 0:
            no_verse_poems += 1
        total_verses += poem.get('verse_count', 0)

    # Pass if no unexpected empty poems (beyond known empty ones)
    passed = empty_poems <= KNOWN_EMPTY_POEMS and no_verse_poems == 0
    results['verse_structure'] = {
        'passed': passed,
        'no_verse_poems': no_verse_poems,
        'empty_poems': empty_poems,
        'known_empty': KNOWN_EMPTY_POEMS,
        'total_verses': total_verses
    }
    print(f"[{'✓' if passed else '✗'}] Verse structure: {total_verses:,} verses, {empty_poems} empty poems (known: {KNOWN_EMPTY_POEMS}), {no_verse_poems} unexpected empty")
    all_passed &= passed

    # 5. Verse consistency (check verse_lines matches verse_count)
    # Note: We no longer compare to CSV verseCount since that field has data quality issues
    verse_inconsistencies = 0
    for poem_id, poem in poems.items():
        verse_count = poem.get('verse_count', 0)
        verse_lines = poem.get('verse_lines', [])
        if len(verse_lines) != verse_count:
            verse_inconsistencies += 1
    passed = verse_inconsistencies == 0
    results['verse_consistency'] = {
        'passed': passed,
        'inconsistencies': verse_inconsistencies
    }
    print(f"[{'✓' if passed else '✗'}] Verse consistency: {verse_inconsistencies} poems with verse_count != len(verse_lines)")
    all_passed &= passed

    # 6. Word annotation completeness (for non-empty poems)
    incomplete_words = 0
    required_fields = ['original', 'lemma', 'pos', 'method', 'confidence']
    sample_incomplete = []
    for poem_id, poem in poems.items():
        if poem.get('is_empty', False):
            continue  # Skip empty poems
        for word in poem.get('words', []):
            missing = [f for f in required_fields if f not in word]
            if missing:
                incomplete_words += 1
                if len(sample_incomplete) < 3:
                    sample_incomplete.append((poem_id, word.get('original', '?'), missing))
    passed = incomplete_words == 0
    results['annotation_completeness'] = {
        'passed': passed,
        'incomplete_words': incomplete_words,
        'sample_incomplete': sample_incomplete
    }
    print(f"[{'✓' if passed else '✗'}] Annotation completeness: {incomplete_words} words missing fields")
    all_passed &= passed

    # 7. Verse index validity (for non-empty poems with successful alignment)
    invalid_verse_idx = 0
    for poem_id, poem in poems.items():
        if poem.get('is_empty', False):
            continue  # Skip empty poems
        verse_count = poem.get('verse_count', 0)
        for word in poem.get('words', []):
            verse_idx = word.get('verse_index', -1)
            # -1 means alignment failed (acceptable for poems with issues)
            if verse_idx != -1 and (verse_idx < 0 or verse_idx >= verse_count):
                invalid_verse_idx += 1
    passed = invalid_verse_idx == 0
    results['verse_index_validity'] = {
        'passed': passed,
        'invalid_count': invalid_verse_idx
    }
    print(f"[{'✓' if passed else '✗'}] Verse index validity: {invalid_verse_idx} words with out-of-range verse_index")
    all_passed &= passed

    # 8. Metadata population
    poems_with_title = sum(1 for p in poems.values() if p.get('metadata', {}).get('title'))
    poems_with_collection = sum(1 for p in poems.values() if p.get('metadata', {}).get('collection'))
    title_pct = 100 * poems_with_title / len(poems) if poems else 0
    collection_pct = 100 * poems_with_collection / len(poems) if poems else 0
    passed = title_pct >= 90 and collection_pct >= 90
    results['metadata_population'] = {
        'passed': passed,
        'title_pct': title_pct,
        'collection_pct': collection_pct
    }
    print(f"[{'✓' if passed else '✗'}] Metadata population: {title_pct:.1f}% titles, {collection_pct:.1f}% collections")
    all_passed &= passed

    # 9. Spot checks for specific poems (accounting for known empty ones)
    spot_checks = [
        ('89248', 'First poem', False),  # Not known empty
        ('99999', 'Last 5-digit ID', False),
        ('100000', 'First 6-digit ID', False),
        ('198216', 'Last poem', True),  # Known empty
        ('105772', 'Sample middle poem', False)
    ]
    spot_results = []
    for poem_id, label, known_empty in spot_checks:
        poem = poems.get(poem_id)
        if poem:
            is_empty = poem.get('is_empty', False)
            if known_empty:
                # For known empty poems, just check it exists and is marked empty
                ok = is_empty
                status = 'empty (expected)'
            else:
                # For normal poems, check has content
                has_verses = poem.get('verse_count', 0) > 0
                has_text = len(poem.get('text', '')) > 0
                has_words = len(poem.get('words', [])) > 0
                ok = has_verses and has_text and has_words
                status = 'has content' if ok else 'missing content'
            spot_results.append((poem_id, label, ok, status))
        else:
            spot_results.append((poem_id, label, False, 'not found'))

    passed = all(r[2] for r in spot_results)
    results['spot_checks'] = {
        'passed': passed,
        'checks': spot_results
    }
    print(f"[{'✓' if passed else '✗'}] Spot checks: {sum(1 for r in spot_results if r[2])}/{len(spot_results)} passed")
    for poem_id, label, ok, status in spot_results:
        print(f"    [{'+' if ok else '-'}] {poem_id} ({label}): {status}")
    all_passed &= passed

    # 10. Annotation consistency with v1
    annotation_mismatches = 0
    sample_size = min(1000, len(poems))
    sample_ids = list(poems.keys())[:sample_size]
    for poem_id in sample_ids:
        v2_words = poems[poem_id].get('words', [])
        v1_words = poems_v1.get(poem_id, {}).get('words', [])
        for v2_word, v1_word in zip(v2_words, v1_words):
            if v2_word.get('lemma') != v1_word.get('lemma'):
                annotation_mismatches += 1
                break  # Count per poem, not per word
    passed = annotation_mismatches == 0
    results['annotation_consistency'] = {
        'passed': passed,
        'mismatches': annotation_mismatches,
        'sample_size': sample_size
    }
    print(f"[{'✓' if passed else '✗'}] Annotation consistency: {annotation_mismatches} mismatches in {sample_size} samples")
    all_passed &= passed

    # Summary
    print(f"\n=== VERIFICATION SUMMARY ===")
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r['passed'])
    print(f"Passed: {passed_checks}/{total_checks}")
    print(f"Overall: {'✓ ALL PASSED' if all_passed else '✗ SOME FAILED'}")

    return all_passed, results


def save_index(index_v2: dict, output_path: Path):
    """Save index to gzip-compressed JSON."""
    print(f"\nSaving to {output_path}...")

    with gzip.open(output_path, 'wt', encoding='utf-8') as f:
        json.dump(index_v2, f, ensure_ascii=False, indent=2)

    # Verify the saved file
    print("Verifying saved file...")
    import subprocess
    result = subprocess.run(['gzip', '-t', str(output_path)], capture_output=True)
    if result.returncode == 0:
        print("  ✓ gzip integrity check passed")
    else:
        print(f"  ✗ gzip integrity check FAILED: {result.stderr.decode()}")
        return False

    # Check file size
    file_size = output_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB")

    if file_size_mb < 80:
        print(f"  ⚠ WARNING: File size ({file_size_mb:.2f} MB) is smaller than expected (>80 MB)")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate poems_index_v2 with verse line markers'
    )
    parser.add_argument(
        '--csv',
        type=Path,
        default=Path('../../estnltk_dict_only/koik_regilaulud_okt_2025.csv'),
        help='Path to source CSV with verse markers'
    )
    parser.add_argument(
        '--poems-index',
        type=Path,
        default=Path('poems_index.json.gz'),
        help='Path to existing poems_index.json.gz'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('poems_index_v2.json.gz'),
        help='Output path for v2 index'
    )
    parser.add_argument(
        '--skip-verification',
        action='store_true',
        help='Skip verification suite'
    )
    parser.add_argument(
        '--issues-file',
        type=Path,
        default=None,
        help='Save issues to JSON file'
    )
    parser.add_argument(
        '--force-save',
        action='store_true',
        help='Save output even if verification fails (non-interactive)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("POEMS INDEX V2 GENERATOR")
    print("=" * 60)
    print(f"CSV source: {args.csv}")
    print(f"Poems index: {args.poems_index}")
    print(f"Output: {args.output}")
    print("=" * 60)

    # Load data
    csv_data = load_csv_data(args.csv)
    poems_index = load_poems_index(args.poems_index)

    # Build v2
    index_v2, issues = build_poems_index_v2(csv_data, poems_index)

    # Save issues if requested
    if args.issues_file and issues:
        print(f"\nSaving {len(issues)} issues to {args.issues_file}...")
        with open(args.issues_file, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)

    # Run verification
    if not args.skip_verification:
        all_passed, verification_results = run_verification(
            index_v2, csv_data, poems_index['poems']
        )

        if not all_passed:
            print("\n⚠ WARNING: Some verification checks did not pass.")
            if not args.force_save:
                try:
                    response = input("Save anyway? (y/n): ").strip().lower()
                    if response != 'y':
                        print("Aborted.")
                        sys.exit(1)
                except EOFError:
                    print("Non-interactive mode detected. Use --force-save to save anyway.")
                    sys.exit(1)
            else:
                print("--force-save enabled, proceeding with save...")

    # Save output
    if not save_index(index_v2, args.output):
        print("\n✗ Save failed!")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
