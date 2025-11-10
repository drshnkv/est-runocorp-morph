# Estonian Runosong Morphological Corpus

> **⚠️ Experimental Mixed-Method Annotation Corpus**
>
> This corpus represents automated morphological annotation using **EstNLTK + lexical resources** combined with **manual expert corrections** (37%) and **LLM-assisted annotations from Järva subcorpus** (2.9%), with validation-based improvements for archaic dialectal Estonian texts.
>
> **Accuracy evaluation:** See "Evaluation Methodology and Results" section below for performance metrics. The confidence scores (average 0.92) reflect method reliability estimates, not actual annotation accuracy. This corpus serves as a methodological baseline for comparing with LLM-based approaches.

A morphologically annotated corpus of 108,969 Estonian runosongs (traditional folk poetry), containing 7.3 million word instances processed using a mixed-method approach combining automated methods, manual expert annotations, and LLM assistance.

## Overview

This corpus provides automated morphological annotation of Estonian dialectal runosong texts, combining EstNLTK 1.7.4 morphological processing with lexical resources (175,493 unique word forms). The annotation includes part-of-speech tags, morphological forms, lemmatization, and confidence scoring across multiple processing methods.


## Corpus Statistics

### Current Version (corpus_unknown_reduced)

- **Total word instances processed**: 7,344,568
- **Unique word forms**: 451,371
- **Unique lemmas generated**: 116,572
- **Average occurrences per word**: 16.3
- **Texts processed**: 108,969 runosong poems
- **Unknown words**: 6,190 (0.08%) - **85.3% reduction** from v5
- **Average confidence score**: 0.92 (method reliability, not accuracy)

### Previous Version (v5) Statistics

- **Unknown words**: 42,070 (0.57%)
- **Unique lemmas**: 125,162

### Method Distribution

| Method | Word Count | Percentage | Avg Confidence |
|--------|-----------|------------|----------------|
| manual_override | 2,713,782 | 36.95% | 1.000 |
| estnltk+dict | 2,267,138 | 30.87% | 1.000 |
| estnltk | 696,829 | 9.49% | 0.950 |
| dict | 566,448 | 7.71% | 0.647 |
| levenshtein | 248,009 | 3.38% | 0.310 |
| suffix_strip | 203,696 | 2.77% | 0.800 |
| estnltk+dict_jarva_claude_3.5 | 155,068 | 2.11% | 1.000 |
| estnltk_validation_levenshtein_valid | 111,666 | 1.52% | 0.867 |
| estnltk_jarva_claude_3.5 | 65,682 | 0.89% | 1.000 |
| dict_jarva_claude_3.5 | 45,397 | 0.62% | 1.000 |
| neurotolge_vro | 35,874 | 0.49% | 0.000 |
| compound | 31,617 | 0.43% | 0.300 |
| unknown | 6,190 | 0.08% | 0.000 |
| estnltk_validation_compound_invalid | 23,545 | 0.32% | 0.000 |
| estnltk_validation_suffix_strip_valid | 19,617 | 0.27% | 0.610 |
| (others) | ~17,000 | ~0.23% | varies |

**Note:** Methods with `_validation_` suffix indicate validation-based improvements applied in v5. `_valid` suffix means validation confirmed the lemma, `_invalid` means validation identified issues.

### Quality Distribution

| Quality Tier | Unique Words | Percentage |
|-------------|-------------|------------|
| high_confidence | 240,848 | 56.3% |
| medium_confidence | 55,663 | 13.0% |
| low_confidence | 16,067 | 3.8% |
| needs_review | 114,894 | 26.9% |

## Files Included

### Current Version (v6 - November 2025) ✨ NEW

- **`corpus_unknown_reduced.json.gz`** (34 MB) - Corpus with Neurotõlge VRO improvements
- **`corpus_unknown_reduced.db`** (77 MB) - SQLite database for efficient querying
- **`poems_index.json.gz`** (82 MB) - Complete poem index with preserved word order and annotations
- **`CORPUS_UNKNOWN_REDUCED_README.md`** - Detailed documentation for v6 corpus
- **`DOCUMENTATION_ET.md`** - Estonian language documentation of annotation process
- **`examples/`** - Code examples for using the corpus

**What's new in v6:**
- **Unknown word reduction**: 85.3% decrease (42,070 → 6,190 instances)
- **Neurotõlge VRO corrections**: 35,874 dialectal improvements (0.49% of corpus)
- **Multi-word lemmas**: 2,145 contextual multi-word expressions (6.0% of corrections)
- **Lemma consolidation**: 116,572 unique lemmas (reduced from 125,162)
- **Coverage**: 99.92% of corpus now has valid lemmas
- **Quality preservation**: All 2,994,162 high-quality lemmas from v5 preserved (manual + Járva + validation)

### Previous Versions

#### v5 (October 2025)

- **`corpus_validation_improved.json.gz`** (35 MB) - Corpus with validation-based improvements
- **`corpus_validation_improved.db`** (77 MB) - SQLite database

**What was new in v5:**
- **Validation improvements**: 214,968 corrections (2.93% of corpus) based on EstNLTK validation
- **Complete vocabulary**: Unknown words included (42,070 words, 0.57%)
- **Invalid lemma cleanup**: 167,994 → 125,162 unique lemmas (-25.5%)
- **Method provenance**: Enhanced tracking with `_validation_[method]_[status]` format
- **Quality preservation**: 2,994,162 high-quality lemmas preserved (manual + Järva)
- **Validation performance**: 67.9% success rate (146,038 valid / 214,968 total corrections)

#### v4 (October 2025)

- **`corpus_ambiguity_validated.json.gz`** (34 MB) - Corpus with EstNLTK-validated lemmas
- **`corpus_ambiguity_validated.db`** (73 MB) - SQLite database

**What was new in v4:**
- **Ambiguity validation**: 12,835 invalid lemmas corrected (70,953 instances)
- **EstNLTK strict validation**: All competing lemmas validated against Estonian dictionary
- **42.5% ambiguity reduction**: From 24,777 to 14,238 truly ambiguous words
- **Method tracking**: New `_estnltk_validated` suffix for corrected words

#### v3 (October 2025)

- **`corpus_fixed_ambiguity_strict.json.gz`** (34 MB) - Corpus with Järva improvements and fixed ambiguity detection
- **`corpus_fixed_ambiguity_strict.db`** (75 MB) - SQLite database

**What was new in v3:**
- **Järva improvements**: 280,380 lemma corrections (91.20% accuracy vs gold standard)
- **Fixed morphology**: Correct verb forms (sid, n, b, s, ma, tud instead of generic "x")
- **Fixed ambiguity detection**: 76.8% reduction in false ambiguity (24,777 truly ambiguous vs 106,821 before)
- **Cleaner structure**: `lemma_competition` only shows actually-chosen lemmas (not rejected-only)

### Earlier Versions

- **v2**: `corpus_runosongs_v2_corrected_FIXED.json.gz` (42 MB) - Before ambiguity fixes

## Data Structure

### JSON Format (Primary)

The JSON corpus contains complete morphological annotation with 8 main sections:

```json
{
  "metadata": {
    "total_words": 7344568,
    "unique_forms": 451371,
    "unique_lemmas": 116572,
    "created": "2025-11-10 12:09:25",
    "modified": "2025-11-10 13:13:48",
    "version": "v6_unknown_reduced",
    "neurotolge_vro_applied": true,
    "neurotolge_corrections": 35874,
    "unknown_reduction": {"before": 42070, "after": 6190, "reduction_pct": 85.3},
    "features": ["aggregated_storage", "reverse_lemma_index", "source_poem_tracking", "..."]
  },

  "words": {
    "piiri": {
      "lemmas": ["piir"],
      "lemma_counts": {"piir": 787},
      "methods": {"piir": {"estnltk+dict": 787}},
      "confidences": {"piir": {"avg": 1.0, "min": 1.0, "max": 1.0, "count": 787}},
      "pos_tags": {"piir": {"S": 787}},
      "forms": {"piir": {"sg_g": 720, "sg_p": 67}},
      "total_count": 787,
      "first_seen": "batch_00001",
      "last_seen": "batch_01090",
      "source_poems": ["89248", "89249", "..."]
    }
  },

  "lemma_index": {
    "piir": {
      "word_forms": ["piir", "piiri", "piire", "piirid"],
      "total_occurrences": 2847,
      "form_distribution": {
        "piiri": {"count": 787, "forms": ["sg_g", "sg_p"], "confidence_avg": 1.0}
      }
    }
  },

  "ambiguous_words": {
    "kand": {
      "total_occurrences": 57,
      "lemma_competition": {
        "kand": {"chosen": 45, "rejected": 0, "confidence_avg": 0.85},
        "kanna": {"chosen": 12, "rejected": 45, "confidence_avg": 0.75}
      },
      "alternatives_seen": ["kand", "kanna"],
      "needs_review": true
    }
  },

  "method_analytics": {
    "estnltk+dict": {
      "total_uses": 2267138,
      "avg_confidence": 1.0,
      "by_pos": {
        "S": {"count": 1245678, "avg_confidence": 1.0},
        "V": {"count": 567890, "avg_confidence": 1.0}
      }
    }
  },

  "morphological_patterns": {
    "S_sg_n": {"count": 567890, "avg_confidence": 0.95},
    "V_ma": {"count": 234567, "avg_confidence": 0.92}
  },

  "quality_tiers": {
    "high_confidence": {"unique_words": 240485, "percentage": 53.2},
    "medium_confidence": {"unique_words": 55611, "percentage": 12.3},
    "low_confidence": {"unique_words": 16153, "percentage": 3.6},
    "needs_review": {"unique_words": 139912, "percentage": 30.9}
  },

  "corpus_timeline": [
    {
      "batch_num": 1,
      "cumulative_words": 7345,
      "cumulative_unique_forms": 2134,
      "cumulative_lemmas": 1567
    }
  ]
}
```

**Section descriptions:**

1. **`metadata`** - Corpus-level statistics and build information
2. **`words`** - Main word form index (452,161 unique forms) with aggregated statistics
3. **`lemma_index`** - Reverse index from lemmas to word forms (125,600 lemmas, **alphabetically sorted**)
4. **`ambiguous_words`** - Words with multiple competing lemma interpretations (14,105 words)
5. **`method_analytics`** - Performance statistics for each lemmatization method (76 methods)
6. **`morphological_patterns`** - Distribution of POS + morphological form combinations (81 patterns)
7. **`quality_tiers`** - Quality categorization statistics (4 tiers)
8. **`corpus_timeline`** - Progressive statistics as batches were processed (1,090 entries)

### SQLite Schema

The SQLite database provides fast indexed lookups with 4 tables:

**`words` table:**
- `word` (TEXT PRIMARY KEY)
- `total_count` (INTEGER)
- `first_seen` (TEXT) - First batch where word appeared
- `last_seen` (TEXT) - Last batch where word appeared
- `lemmas` (TEXT) - Comma-separated list of lemmas
- `avg_confidence` (REAL)

**`lemma_variants` table:**
- `lemma` (TEXT)
- `word_form` (TEXT)
- `count` (INTEGER)
- `avg_confidence` (REAL)
- PRIMARY KEY (`lemma`, `word_form`)

**`method_stats` table:**
- `method` (TEXT PRIMARY KEY)
- `total_uses` (INTEGER)
- `avg_confidence` (REAL)

**`ambiguous_words` table:**
- `word` (TEXT PRIMARY KEY)
- `total_occurrences` (INTEGER)
- `num_competing_lemmas` (INTEGER)
- `needs_review` (BOOLEAN)

## Usage Examples

### Python Example

```python
#!/usr/bin/env python3
"""Example usage of the Estonian Runosong Corpus"""
import json
import gzip

# Load the corpus
with gzip.open('corpus_unknown_reduced.json.gz', 'rt', encoding='utf-8') as f:
    corpus = json.load(f)

# Look up a specific word
word = 'piiri'
if word in corpus['words']:
    data = corpus['words'][word]
    print(f"Word: {word}")
    print(f"  Lemmas: {data['lemmas']}")
    print(f"  POS tags: {data['pos_tags']}")
    print(f"  Forms: {data['forms']}")
    print(f"  Total count: {data['total_count']}")
    print(f"  Confidence: {data['avg_confidence']}")
    print(f"  Quality: {data['quality']}")

# Find all word forms for a lemma
lemma = 'piir'
if lemma in corpus['lemma_index']:
    variants = corpus['lemma_index'][lemma]
    print(f"\nVariants of '{lemma}': {variants}")

# Check ambiguous words
if word in corpus.get('ambiguous_words', {}):
    ambig = corpus['ambiguous_words'][word]
    print(f"\n'{word}' has competing lemmas: {ambig['competing_lemmas']}")
```

### SQL Example

```sql
-- Find all word forms for a specific lemma
SELECT word_form, count, avg_confidence
FROM lemma_variants
WHERE lemma = 'piir'
ORDER BY count DESC;

-- Find high-frequency words needing review
SELECT w.word, w.total_count, w.avg_confidence, a.num_competing_lemmas
FROM words w
JOIN ambiguous_words a ON w.word = a.word
WHERE a.needs_review = 1 AND w.total_count > 100
ORDER BY a.num_competing_lemmas DESC, w.total_count DESC
LIMIT 50;

-- Get method performance statistics
SELECT method, total_uses, avg_confidence
FROM method_stats
ORDER BY total_uses DESC;
```

See the `examples/` directory for more code samples.

## Viewing Complete Annotated Texts

The corpus includes a poem-level index (`poems_index.json.gz`) that allows viewing complete texts with their morphological annotations preserved in order.

### Quick Start

```bash
cd examples

# View a specific poem
python view_poem.py 89248

# View with detailed annotations
python view_poem.py 89248 --detailed

# View random poems
python view_poem.py --random 5

# Filter and view high-quality poems
python view_poem.py --random 3 --min-confidence 0.95
```

### Example Output

```
================================================================================
POEM ID: 89248
================================================================================
Source batch: batch_00001
Row index: 0
Number of words: 80
Average confidence: 0.960
POS distribution: {'S': 29, 'D': 12, 'P': 10, 'V': 23, 'K': 2, 'A': 4}

--------------------------------------------------------------------------------
ORIGINAL TEXT:
--------------------------------------------------------------------------------
piiri pääri pääsuke kus su kullas pesake kuivand kuuse otsas...

--------------------------------------------------------------------------------
ANNOTATED TEXT (word/lemma(POS)):
--------------------------------------------------------------------------------
piiri/piir(S) pääri/praegu(S) pääsuke/pääsukene(S) kus/kus(D) su/sa(P)
kullas/kuld(S) pesake/pesa(S) kuivand/kuivama(V) kuuse/kuusk(S)...
================================================================================
```

### Advanced Usage

**Filter by criteria:**
```bash
# Poems with specific POS tag
python view_poem.py --random 5 --pos-contains V

# Short poems only
python view_poem.py --random 10 --max-words 50

# High-confidence long poems
python view_poem.py --random 3 --min-confidence 0.9 --min-words 100
```

**Export poems:**
```bash
# Export single poem to JSON
python view_poem.py 89248 --export poem_89248.json

# Export multiple poems
python view_poem.py 89248 89249 89250 --export poems_batch_1.json
```

**Corpus statistics:**
```bash
python view_poem.py --list-stats
```

### Poem Index Structure

The `poems_index.json.gz` file (81 MB compressed) contains all 108,969 poems with complete annotation data:

```json
{
  "metadata": {
    "version": "v1",
    "total_poems": 108969,
    "total_words": 7344574,
    "avg_words_per_poem": 67.4
  },
  "poems": {
    "89248": {
      "text": "piiri pääri pääsuke...",
      "words": [
        {
          "original": "piiri",
          "lemma": "piir",
          "pos": "S",
          "form": "sg_g",
          "method": "estnltk+dict",
          "confidence": 1.0
        },
        ...
      ],
      "batch": "batch_00001",
      "row_index": 0,
      "num_words": 80
    }
  }
}
```

### Regenerating Poem Index

If you have the original batch files, you can regenerate the poem index:

```bash
cd examples
python generate_poem_index.py --batch-dir /path/to/batches --output ../poems_index.json.gz
```

## Lemma Overview CSV

A comprehensive CSV overview of all lemmas is provided for human quality review and linguistic analysis. The CSV contains 21 columns with detailed information about each lemma.

### Quick Start

```bash
# Generate the CSV (already provided in corpus)
python3 generate_lemma_overview_v2.py

# Output: lemma_overview_v2.csv (116,572 lemmas in v6)
```

### CSV Columns

The CSV includes 21 columns organized into categories:

**Core Identification:**
- `lemma` - The lemma form
- `total_occurrences` - Total instances across corpus
- `num_word_forms` - Number of distinct word forms

**Word Form Details:**
- `word_forms_sample` - Top 10 forms with counts (e.g., "piiri(787); piire(520)")
- `most_frequent_form` - Most common word form
- `most_frequent_form_count` - Count of most frequent form
- `most_frequent_form_pct` - Percentage of total occurrences

**Linguistic Information:**
- `pos_tags` - Part-of-speech tags (comma-separated)
- `morph_forms` - Morphological forms (e.g., "sg_g, sg_p, pl_p")
- `avg_confidence` - Average confidence score across all instances

**Method & Quality Tracking:**
- `primary_method` - Most frequently used lemmatization method
- `methods_used` - All methods applied (comma-separated)
- `has_validation` - Boolean, whether validation was applied
- `validation_status` - "all_valid", "all_invalid", "mixed", or "none"
- `validation_method` - Which validation method was used

**Ambiguity & Quality Flags:**
- `is_ambiguous` - Boolean, whether word has competing lemmas
- `needs_review` - Boolean, whether expert review is recommended
- `num_competing_lemmas` - Number of alternative lemma interpretations

**Distribution Statistics:**
- `form_diversity_score` - Ratio of forms to occurrences (type/token)
- `min_confidence` - Lowest confidence across instances
- `max_confidence` - Highest confidence across instances

### Usage Examples

**Open in spreadsheet software:**
```bash
# LibreOffice Calc, Excel, Google Sheets, etc.
open lemma_overview_v2.csv
```

**Sort and filter strategies:**
- **High-frequency review**: Sort by `total_occurrences` descending
- **Validation changes**: Filter `has_validation = TRUE`
- **Potential issues**: Filter `validation_status = all_invalid` and `total_occurrences > 100`
- **Ambiguous cases**: Filter `is_ambiguous = TRUE` and `needs_review = TRUE`
- **Quality assessment**: Sort by `avg_confidence` ascending to find low-confidence lemmas

### Statistics

From v6 corpus:
- **Total lemmas**: 116,572 (-8,590 from v5 due to consolidation)
- **Unknown words**: 6,190 (0.08%) - 85.3% reduction from v5
- **Neurotõlge VRO corrections**: 35,874 (0.49% of corpus)

## Annotation Methodology

### Processing Pipeline

1. **EstNLTK+dict** (33%): Morphological analysis confirmed by dictionary entries
2. **Manual override** (37%): Expert-annotated lemmas from FILTER project corpus
3. **EstNLTK** (14%): Pure morphological analysis
4. **Dict** (8%): Direct dictionary match without morphological confirmation
5. **Levenshtein** (4%): Fuzzy matching for dialectal variants
6. **Other methods** (4%): Suffix stripping, h-variation, compound analysis, etc.


### Example Automated Correction Cycle

Multiple automated correction cycles were applied to improve lemma quality, including high-confidence tier corrections, Järva subcorpus improvements (280,380 corrections), validation-based improvements (214,968 corrections), and Neurotõlge VRO dialectal corrections (35,874 corrections).

**Example ranking system for lemma candidate selection:**

For selecting among multiple lemma candidates:
- **60%** edit distance (Levenshtein distance from original form)
- **40%** frequency score (based on University of Tartu literary corpus)

The frequency component helps select more likely correct lemmas, as words appearing more frequently in literary texts are generally more common in runosongs as well. This approach was tested on 448,217 low-confidence words, resulting in 119,184 (26.6%) alternative lemmas selected.


## Key Features

- **POS tagging**: Morphological classification for processed words
- **Morphological forms**: Case/number/tense markers (sg_g, pl_p, etc.)
- **Method tracking**: Transparent annotation provenance for each word
- **Source traceability**: Links to original poem identifiers
- **Confidence scoring**: 0-1 scale reflecting method reliability (not accuracy)
- **Ambiguity marking**: 14,238 words with genuine lemma competition (v4: EstNLTK-validated, was 24,777 in v3, 106,821 in v2)
- **Frequency data**: Corpus-based frequency information

## Lemma Validation Status

**V6 Unknown Words Reduced** (116,572 unique lemmas):
- **85.3% unknown word reduction** via Neurotõlge VRO (42,070 → 6,190)
- **35,874 VRO dialectal corrections** (0.49% of corpus)
- **8,590 lemmas consolidated** (125,600 → 116,572) for better deduplication
- **99.92% corpus coverage** (only 0.08% unknown words remaining)
- **All v5 high-quality lemmas preserved** (2,994,162 entries: manual + Järva + validation)

**V5 Validation Results** (125,600 unique lemmas):
- **61,378 lemmas validated (48.9%)** using VabamorfAnalyzer
- **+10.8 percentage point improvement** over v4 (38.1% → 48.9%)
- **+354 more valid lemmas** than v4 despite smaller inventory
- **Previous v4**: 61,024 / 160,024 (38.1%) validated

**Validation history:**
- Oct 14 (pre-corrections): 23.7% valid (51,341 / 216,357 lemmas)
- Oct 16 (after Tier 1+2+3): 31.6% valid (60,993 / 192,756 lemmas)
- Oct 19 (after Järva improvements): 31.7% valid (61,024 / 192,434 lemmas)
- Oct 20 (after ambiguity validation): 38.1% valid (61,024 / 160,024 lemmas)
- Oct 27 (v5 - after validation improvements): 125,600 unique lemmas
  - **214,968 validation-based corrections applied** (2.93% of corpus)
  - **67.9% correction success rate** (146,038 valid / 214,968 total)
  - **Invalid lemma cleanup**: Removed 42,394 invalid lemmas (167,994 → 125,600)
  - **Unknown words included**: All 42,389 unknown words now in corpus
- **Nov 10 (v6 - Neurotõlge VRO improvements)**: 116,572 unique lemmas
  - **35,874 Neurotõlge VRO corrections** (0.49% of corpus)
  - **85.3% unknown word reduction** (42,070 → 6,190)
  - **2,145 multi-word lemmas** (6.0% of corrections)
  - **99.92% coverage** achieved

**Validation method performance (v5):**
- **Dict**: 91.4% valid (896 / 980 corrections)
- **Levenshtein**: 86.7% valid (121,232 / 139,875 corrections)
- **H-variation**: 81.6% valid (2,651 / 3,250 corrections)
- **Suffix-strip**: 61.0% valid (21,259 / 34,850 corrections)
- **Compound**: 0.0% valid (morphological decompositions, informative)

Note: Validation means the lemma is recognized by standard Estonian morphological tools. Järva improvements (280,380 corrections) achieved 91.20% accuracy vs gold standard. V5 validation improvements complementary to Järva, targeting different error patterns. V6 Neurotõlge VRO improvements specifically target Võro dialectal forms previously unknown to the system.

## Evaluation Methodology and Results

The corpus quality was evaluated using a gold standard of 6,405 manually annotated words from 94 Estonian runosong poems. A context-aware instance-level train/test split methodology was employed, with 4,053 TRAIN words (63.3%) used for manual override annotations and 2,352 TEST words (36.7%) reserved for independent evaluation.

> **Note:** This evaluation was performed on a previous version of the corpus (v5 - October 2025). The current v6 version (November 2025) includes additional Neurotõlge VRO improvements (35,874 corrections, 0.49% of corpus) that further reduce unknown words by 85.3% (42,070 → 6,190). Performance metrics below reflect the v5 baseline.

### Automatic Lemmatization Performance

Pure automatic methods (estnltk+dict, dict, estnltk, levenshtein, suffix_strip) were evaluated on 1,988 TEST words (84.5% of the TEST set), achieving **66.35% accuracy** with no manual annotation involvement or test set contamination.

The best-performing method, **estnltk+dict**, achieved **84.08% accuracy** on 50.9% of test words, demonstrating that hybrid approaches combining morphological analysis with dictionary lookup outperform single-method strategies for dialectal Estonian texts.

### Method Performance Summary

| Method | Accuracy | Coverage of Test |
|--------|----------|------------------|
| estnltk+dict | 84.08% | 50.9% |
| dict | 65.23% | 14.0% |
| estnltk | 51.17% | 15.0% |
| levenshtein | 39.44% | 7.1% |
| suffix_strip | 41.05% | 4.8% |

These results reflect the challenging nature of Estonian dialectal runosong texts, with their archaic forms and regional variation, while demonstrating that systematic hybrid approaches can achieve strong performance on standard word forms.

## Lexical Resources 

This corpus was created using a combined index of lexical resources (175,493 unique word forms). The primary sources include:

**EMK** – Corpus of Estonian Dialects. University of Tartu, Institute of Estonian and General Linguistics. *Eesti murrete korpus*. https://datadoi.ee/handle/33/492 (Accessed 22 July 2025).

**EKI‑RC** – EKI Runosong Corpus. Institute of the Estonian Language. *EKI regilaulukorpus* (2019‑2024), derived from the 1969–1974 *Regilaulud. Antoloogia* volumes; (Internal project corpus; description in Ross 2015, *Keel ja Kirjandus*, 68 (6), 510‑539.) (Accessed 22 July 2025).

**EKSS** – Explanatory Dictionary of the Estonian Language. Institute of the Estonian Language. *Eesti keele seletav sõnaraamat* (Online edition). https://www.eki.ee/dict/ekss/ (Accessed 22 July 2025).

**EMS** – Estonian Dialect Dictionary. Institute of the Estonian Language. *Eesti murrete sõnaraamat* (Version 1.3). https://eki.ee/dict/ems/ (Accessed 22 July 2025).

**IMS** – Eastern Estonian Dialect Dictionary. Institute of the Estonian Language. *Ida‑Eesti murdesõnastik*. https://www.eki.ee/dict/ida/ (Accessed 22 July 2025).

**VMS** – Glossary of Lesser‑Known Dialect Words. Estonian Literary Museum. *Vähemtuntud murdesõnade seletusi*. https://www.folklore.ee/moistatused/?id=murdesonu (Accessed 22 July 2025).

**VES** – Võro–Estonian Dictionary. Võro Institute. *Võro-eesti synaraamat* (Online edition; comp. Jüvä Sullõv; print ed. 2002, ISBN 9985-9386-0-7). https://www.folklore.ee/Synaraamat/ (Accessed 22 July 2025).

**ERLA** – Glossary of Rare and Obscure Folk‑Song Words. Estonian Literary Museum. *Harva ja vähem‑kasutatavate sõnade sõnastik*, in *Regilaulud. Antoloogia* corpus. https://www.folklore.ee/laulud/erla/ (Accessed 22 July 2025).

**ERAB** – Oras, Janika; Saarlo, Liina; Sarv, Mari; Labi, Kanni; Uus, Merli; Šmitaite, Reda (comps.). Eesti Regilaulude Andmebaas / Database of Estonian Runosongs. Estonian Folklore Archives, Estonian Literary Museum. 2003 – present. URL: https://www.folklore.ee/regilaul/andmebaas

**UT-FIC** – The Frequency List of Estonian Literary Language. University of Tartu, Computational Linguistics. Fiction subcorpus lemma frequencies from the Balanced Corpus of Estonian (15 million words). https://www.cl.ut.ee/ressursid/sagedused1/failid/lemma_ilu_kahanevas.txt (Accessed November 2025).


## Tools Used

The corpus annotations were generated using **EstNLTK 1.7.4** (Laur et al., 2020) morphological analyzer, which incorporates **Vabamorf** (Kaalep & Vaino, 2001) as its underlying morphological analysis engine.

Kaalep, H. J., & Vaino, T. (2001). Complete morphological analysis in the linguist's toolbox. *Congressus Nonus Internationalis Fenno-Ugristarum*, *5*, 9-16.

Laur, S., Orasmaa, S., Särg, D., & Tammo, P. (2020). EstNLTK 1.6: Remastered Estonian NLP pipeline. *Proceedings of the Twelfth Language Resources and Evaluation Conference* (pp. 7152–7160). European Language Resources Association.

**Neurotõlge** – TartuNLP Neural Machine Translation system. University of Tartu, Natural Language Processing research group. Used for VRO↔EST (Võro-Estonian) translation in dialectal lemma improvements. https://translate.ut.ee/ (Main demo: https://neurotolge.ee/) (Accessed November 2025).


## Citation and Licence

If you intend to use this corpus, please contact first:

```
kaarel.veskis@kirmus.ee
https://github.com/drshnkv/est-runocorp-morph
```

## Technical Details

- **Processing environment**: Google Colab with parallel batch processing
- **Batch structure**: 1090 batches (~100 poems each)
- **Morphological analyzer**: EstNLTK 1.7.4 with Vabamorf
- **Dictionary sources**: Combined index of 175,493 unique entries



