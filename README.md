# Estonian Runosong Morphological Corpus

> **⚠️ Experimental Non-LLM Baseline Corpus – Version 1**
>
> This corpus represents preliminary automated morphological annotation using **EstNLTK + lexical resources** for archaic dialectal Estonian texts.
>
> **Estimated accuracy: ca 70%** based on preliminary non-conclusive evaluation.  The confidence scores (average 0.92) reflect method reliability estimates, not actual annotation accuracy. This corpus serves as a methodological baseline for comparing with LLM-based approaches, which show better results but are still work in progress.

A morphologically annotated corpus of 108,969 Estonian runosongs (traditional folk poetry), containing 7.3 million word instances processed with non-LLM methods.

## Overview

This corpus provides automated morphological annotation of Estonian dialectal runosong texts, combining EstNLTK 1.7.4 morphological processing with lexical resources (175,493 unique word forms). The annotation includes part-of-speech tags, morphological forms, lemmatization, and confidence scoring across multiple processing methods.


## Corpus Statistics

- **Total word instances processed**: 7,302,185
- **Unique word forms**: 427,472
- **Unique lemmas generated**: 167,994
- **Average occurrences per word**: 17.1
- **Texts processed**: 108,969 runosong poems
- **Unknown words**: 42,389 (0.58%)
- **Average confidence score**: 0.92 (method reliability, not accuracy)

### Method Distribution

| Method | Word Count | Percentage | Avg Confidence |
|--------|-----------|------------|----------------|
| manual_override | 2,713,782 | 37.2% | 1.000 |
| estnltk+dict | 2,423,711 | 33.2% | 1.000 |
| estnltk | 1,010,589 | 13.8% | 0.950 |
| dict | 617,085 | 8.5% | 0.647 |
| levenshtein | 261,191 | 3.6% | 0.310 |
| suffix_strip | 213,645 | 2.9% | 0.800 |
| compound | 53,136 | 0.7% | 0.300 |
| h_variation | 7,665 | 0.1% | 0.700 |
| hybrid_corrected | 1,381 | 0.0% | 0.779 |

### Quality Distribution

| Quality Tier | Unique Words | Percentage |
|-------------|-------------|------------|
| high_confidence | 240,848 | 56.3% |
| medium_confidence | 55,663 | 13.0% |
| low_confidence | 16,067 | 3.8% |
| needs_review | 114,894 | 26.9% |

## Files Included

### Current Version (v4 - October 2025) ✨ NEW

- **`corpus_ambiguity_validated.json.gz`** (34 MB) - Corpus with EstNLTK-validated lemmas
- **`corpus_ambiguity_validated.db`** (73 MB) - SQLite database for efficient querying
- **`poems_index.json.gz`** (81 MB) - Complete poem index with preserved word order and annotations ⭐ NEW
- **`DOCUMENTATION_ET.md`** - Estonian language documentation of annotation process
- **`examples/`** - Code examples for using the corpus

**What's new in v4:**
- **Ambiguity validation**: 12,835 invalid lemmas corrected (70,953 instances)
- **EstNLTK strict validation**: All competing lemmas validated against Estonian dictionary
- **42.5% ambiguity reduction**: From 24,777 to 14,238 truly ambiguous words
- **Method tracking**: New `_estnltk_validated` suffix for corrected words
- **Preservation**: True ambiguity (9,466 words) and dialectal forms (3,484 words) maintained

### Previous Version (v3 - October 2025)

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

The JSON corpus contains complete morphological annotation with the following structure:

```json
{
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
      "source_poems": ["ERA.1.1.1", "..."]
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
      "needs_review": true
    }
  }
}
```

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
with gzip.open('corpus_runosongs_v2_corrected_FIXED.json.gz', 'rt', encoding='utf-8') as f:
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

## Annotation Methodology

### Processing Pipeline

1. **EstNLTK+dict** (33%): Morphological analysis confirmed by dictionary entries
2. **Manual override** (37%): Expert-annotated lemmas from FILTER project corpus
3. **EstNLTK** (14%): Pure morphological analysis
4. **Dict** (8%): Direct dictionary match without morphological confirmation
5. **Levenshtein** (4%): Fuzzy matching for dialectal variants
6. **Other methods** (4%): Suffix stripping, h-variation, compound analysis, etc.


###  Automated follow-up correction cycles based on the ranking system and other filtration criteria

Ranking system:

For selecting among multiple lemma candidates:
- **60%** edit distance (Levenshtein distance from original form)
- **40%** frequency score (based on University of Tartu literary corpus)

The frequency component helps select more likely correct lemmas, as words appearing more frequently in literary texts are generally more common in runosongs as well. Tested on 448,217 low-confidence words, resulting in 119,184 (26.6%) alternative lemmas selected.


## Key Features

- **POS tagging**: Morphological classification for processed words
- **Morphological forms**: Case/number/tense markers (sg_g, pl_p, etc.)
- **Quality categorization**: Four-tier assessment based on method and validation
- **Method tracking**: Transparent annotation provenance for each word
- **Source traceability**: Links to original poem identifiers
- **Confidence scoring**: 0-1 scale reflecting method reliability (not accuracy)
- **Ambiguity marking**: 14,238 words with genuine lemma competition (v4: EstNLTK-validated, was 24,777 in v3, 106,821 in v2)
- **Frequency data**: Corpus-based frequency information

## Lemma Validation Status

Of 160,024 unique lemmas generated:
- **61,024 (38.1%)** can be validated with standard Estonian morphology (using EstNLTK/Vabamorf)
- **99,000 (61.9%)** are archaic/dialectal forms or unvalidated word forms

**Validation history:**
- Oct 14 (pre-corrections): 23.7% valid (51,341 / 216,357 lemmas)
- Oct 16 (after Tier 1+2+3): 31.6% valid (60,993 / 192,756 lemmas)
- Oct 19 (after improvements based on 361 Järvamaa runosongs annotated with Claude Sonnet 3.5): 31.7% valid (61,024 / 192,434 lemmas)
- Oct 20 (after ambiguity validation): 38.1% valid (61,024 / 160,024 lemmas)
  - **Removed 32,410 invalid lemmas** from ambiguous words
  - Validation improvement: **+6.4 percentage points**

Note: Validation means the lemma is recognized by standard Estonian morphological tools, not that the lemmatization is necessarily correct for the specific context. Järva improvements (280,380 corrections) were based on high-quality LLM annotations achieving 91.20% accuracy vs gold standard.

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


## Citation and Licence

If you intend to use this corpus in your research, please contact first:

```
kaarel.veskis@kirmus.ee
https://github.com/drshnkv/est-runocorp-morph
```

## Technical Details

- **Processing environment**: Google Colab with parallel batch processing
- **Batch structure**: 1090 batches (~100 poems each)
- **Morphological analyzer**: EstNLTK 1.7.4 with Vabamorf
- **Dictionary sources**: Combined index of 175,493 unique entries



