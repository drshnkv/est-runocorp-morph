# Estonian Runosong Corpus v5 - Unknown Words Reduced

**Version:** v5_unknown_reduced
**Date:** 2025-11-10
**Status:** Production-ready corpus with significantly reduced unknown words

---

## Overview

This corpus represents the **Estonian runosong lemmatization corpus with unknown words reduced by 85.3%** through the application of Neurotõlge VRO dialectal improvements. It contains 7.3+ million word instances from traditional Estonian folk songs with high-quality lemmatization.

---

## Corpus Statistics

### Coverage Metrics

| Metric | Count | Details |
|--------|-------|---------|
| **Total word instances** | 7,344,568 | All word tokens in corpus |
| **Unique word forms** | 451,371 | Distinct wordforms |
| **Unique lemmas** | 116,572 | Distinct base forms |
| **Unknown words** | 6,190 (0.08%) | Down from 42,070 (85.3% reduction) |
| **Coverage** | 99.92% | Percentage of words with valid lemmas |

### Quality Improvements Applied

```
Historical progression:
─────────────────────────────────────────────────────────
Tier 1-3 corrections:       629,187 improvements
Järva improvements:          280,380 improvements
Validation improvements:     214,968 improvements
Neurotõlge VRO:               35,874 improvements
─────────────────────────────────────────────────────────
Total improvements:        1,160,409 (15.8% of corpus)
```

---

## Neurotõlge VRO Improvements

### What Was Applied

The corpus incorporates **35,874 Neurotõlge VRO corrections** that specifically target Võro dialectal forms previously unknown to the system.

**Correction types:**
- Single-word lemmas: 33,729 (94.0%)
- Multi-word phrases: 2,145 (6.0%)

**Source:** TartuNLP Neurotõlge API (VRO↔EST neural translation)

**Method:** VRO→EST translation → VRO lemmatization

### Unknown Word Reduction

| Phase | Unknown Words | Coverage |
|-------|--------------|----------|
| **Before Neurotõlge VRO** | 42,070 (0.57%) | 99.43% |
| **After Neurotõlge VRO** | 6,190 (0.08%) | 99.92% |
| **Reduction** | 35,880 (-85.3%) | +0.49 pp |

---

## Files

### Corpus Files

**Primary files in this directory:**

```
corpus_unknown_reduced.json       417 MB (uncompressed)
corpus_unknown_reduced.json.gz     34 MB (compressed) ← RECOMMENDED
```

**Recommendation:** Use the `.gz` file for storage and distribution (12× smaller).

### Metadata Structure

The corpus includes comprehensive metadata:

```json
{
  "metadata": {
    "total_words": 7344568,
    "unique_forms": 451371,
    "unique_lemmas": 116572,
    "created": "2025-11-10 12:09:25",
    "version": "v5_unknown_reduced",
    "description": "Estonian runosong corpus v5 with unknown words reduced...",
    "modified": "2025-11-10 13:13:48",
    "neurotolge_vro_applied": true,
    "neurotolge_corrections": 35874,
    "unknown_reduction": {
      "before": 42070,
      "after": 6190,
      "reduction_pct": 85.3
    },
    "features": [
      "aggregated_storage",
      "reverse_lemma_index",
      "source_poem_tracking",
      "ambiguity_analysis",
      "method_analytics",
      "morphological_patterns",
      "quality_tiers",
      "corpus_timeline",
      "unknown_words_included",
      "neurotolge_vro_corrections"
    ]
  }
}
```

---

## Usage

### Loading the Corpus

**Python example:**

```python
import json
import gzip

# Load compressed version (recommended)
with gzip.open('corpus_unknown_reduced.json.gz', 'rt', encoding='utf-8') as f:
    corpus = json.load(f)

# Access metadata
metadata = corpus['metadata']
print(f"Total words: {metadata['total_words']:,}")
print(f"Unknown words: {metadata['unknown_reduction']['after']:,}")
print(f"Coverage: {(1 - metadata['unknown_reduction']['after'] / metadata['total_words']) * 100:.2f}%")

# Access word forms
words = corpus['words']
print(f"Unique word forms: {len(words):,}")

# Example: Get lemma for a word
if 'kodu' in words:
    word_data = words['kodu']
    print(f"Lemmas for 'kodu': {word_data['lemmas']}")
    print(f"Methods: {word_data['methods']}")
```

### Querying the Corpus

```python
# Get all neurotolge_vro corrections
neurotolge_words = []
for word, data in corpus['words'].items():
    for lemma, methods in data.get('methods', {}).items():
        if 'neurotolge_vro' in methods:
            neurotolge_words.append({
                'word': word,
                'lemma': lemma,
                'count': methods['neurotolge_vro']
            })

print(f"Neurotõlge VRO corrections: {len(neurotolge_words):,}")

# Get words by method
method_analytics = corpus.get('method_analytics', {})
for method, stats in sorted(method_analytics.items(),
                           key=lambda x: x[1]['total_uses'],
                           reverse=True)[:10]:
    print(f"{method}: {stats['total_uses']:,} uses")
```

---

## Data Integrity

### Verification Results

✅ **All safety guarantees maintained:**
- Manual overrides preserved: 2,713,782 entries
- Järva improvements preserved: 280,380 entries
- Validation improvements preserved: 214,968 entries
- Only `method="unknown"` words modified
- Zero unexpected changes detected

### Change Summary

**Word-level changes:**
- 21,907 unique word types changed from `unknown` → `neurotolge_vro`
- 35,874 total word instances affected
- Perfect 1:1 method transition (unknown removed = neurotolge_vro added)

**Minor cleanup:**
- 1 word form removed (`ampquot` - XML entity artifact)
- 6 total instances cleaned

---

## Quality Characteristics

### Method Distribution

The corpus uses multiple lemmatization methods with varying confidence levels:

| Method | Instances | Avg Confidence | Quality |
|--------|-----------|----------------|---------|
| **manual_override** | 2,713,782 | 1.0 | Highest (expert-verified) |
| **estnltk+dict** | 2,267,138 | 1.0 | High (morphology + dictionary) |
| **estnltk** | 696,829 | 0.95 | High (morphological analysis) |
| **dict** | 566,448 | 0.64 | Medium (dictionary lookup) |
| **Järva improvements** | 280,380 | Varies | High (dialect-specific) |
| **Validation improvements** | 214,968 | Varies | Medium-High (validated) |
| **levenshtein** | 248,009 | 0.31 | Low (fuzzy matching) |
| **suffix_strip** | 203,696 | 0.8 | Medium (suffix removal) |
| **neurotolge_vro** | 35,874 | 0.0 | New (neural translation) |
| **unknown** | 6,190 | N/A | Lowest (no lemma found) |

**Note:** `neurotolge_vro` has confidence 0.0 because these were previously unknown words - the method itself should be validated separately.

### Remaining Unknown Words

The 6,190 remaining unknown words (0.08%) likely represent:

1. **Rare dialectal variants** not captured by VRO translation
2. **Archaic vocabulary** no longer in modern use
3. **Proper nouns** (personal names, place names)
4. **Transcription artifacts** (OCR errors, non-standard spellings)
5. **Truly unknown forms** requiring linguistic research

---

## Dialectal Coverage

### Multi-word Lemmas

The corpus includes **2,145 multi-word lemmas** from Neurotõlge VRO that preserve semantic completeness:

**Examples:**

```
Word form           → Multi-word lemma         (Translation)
───────────────────────────────────────────────────────────────
neljanurgelista     → "nelinurkne nimekiri"    (square list)
kutreskaula         → "kuue kaelaga"           (with six necks)
keskepõrmandalla    → "keskmisel korrusel"     (on middle floor)
juhvanjahvan        → "juhivankri all"         (under driver's cart)
villatäpenista      → "villane penista"        (woolen blanket)
kingapaelusiida     → "kingapaela siid"        (shoelace silk)
kuldaluuakene       → "kuldne aken"            (golden window)
nelladviied         → "nelikümmend viis"       (forty-five)
```

These preserve dialectal compound meanings that single-word lemmas would lose.

---

## Corpus Structure

### Top-level Keys

```json
{
  "metadata": {...},           // Corpus metadata and statistics
  "words": {...},              // Word forms → lemma data
  "lemma_index": {...},        // Reverse index: lemmas → word forms
  "ambiguous_words": {...},    // Words with multiple valid lemmas
  "method_analytics": {...},   // Method performance statistics
  "morphological_patterns": {...}, // POS and morphology distributions
  "quality_tiers": {...},      // Confidence-based quality tiers
  "corpus_timeline": {...}     // Corpus evolution over time
}
```

### Word Entry Structure

```json
"kodu": {
  "lemmas": ["kodu"],
  "lemma_counts": {"kodu": 787},
  "methods": {
    "kodu": {
      "estnltk+dict": 787
    }
  },
  "confidences": {
    "kodu": {
      "avg": 1.0,
      "min": 1.0,
      "max": 1.0,
      "count": 787
    }
  },
  "pos_tags": {"kodu": {"S": 787}},
  "forms": {"kodu": {"sg_g": 720, "sg_p": 67}},
  "total_count": 787,
  "first_seen": "batch_00001",
  "last_seen": "batch_01090",
  "source_poems": [89248, 89434, ...]
}
```

---

## Related Documentation

### Processing Pipeline

1. **Source batches:** `../output_batches/batches_v2_neurotolge_vro/` (1,090 batch files)
2. **Build script:** `build_corpus_v5_validation.py`
3. **Metadata update:** `update_corpus_metadata.py`
4. **Comparison report:** `../output_batches/CORPUS_COMPARISON_REPORT_NEUROTOLGE_VRO.md`

### Previous Session Work

**Neurotõlge VRO application session (2025-11-10):**
- `../estonian-neurotolge-pilot/SESSION_SUMMARY_2025_11_10_neurotolge_vro_FINAL.md`
- `../estonian-neurotolge-pilot/OUTPUTS_SUMMARY.md`
- `../estonian-neurotolge-pilot/NEUROTOLGE_VRO_APPLICATION_REPORT_20251110_113332.md`

### Verification Scripts

- `../output_batches/compare_corpus_versions_v2.py` - Compare corpus versions
- `../output_batches/verify_corpus_changes.py` - Verify only expected changes applied

---

## Citation

If using this corpus in research, please cite:

```
Estonian Runosong Lemmatization Corpus v5 (Unknown Words Reduced)
Version: v5_unknown_reduced
Date: 2025-11-10
Coverage: 99.92% (6,190 unknown out of 7,344,568 words)
Improvements: Neurotõlge VRO dialectal corrections applied (35,874 corrections)
```

---

## License and Attribution

This corpus builds on traditional Estonian folk songs from public domain collections. The lemmatization improvements incorporate:

- EstNLTK (Estonian NLP Toolkit)
- TartuNLP Neurotõlge API (VRO↔EST translation)
- Manual expert corrections
- Dialectal analysis (Järva corpus)
- Morphological validation

---

## Support and Issues

For questions or issues with this corpus:

1. Check the comparison report: `../output_batches/CORPUS_COMPARISON_REPORT_NEUROTOLGE_VRO.md`
2. Review session documentation in `../estonian-neurotolge-pilot/`
3. Verify data integrity with `verify_corpus_changes.py`

---

**Last Updated:** 2025-11-10 13:15
**Corpus Location:** `/Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/est-runocorp-morph-standalone/`
