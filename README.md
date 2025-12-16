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

### Current Version (v9 - POS Corrections) ✨ NEW

- **POS corrections applied**: 382,574 tokens (14.1% of manual_override)
- **Substitution rules**: 102 verified POS corrections
- **Poems affected**: 71,788 (65.9% of corpus)
- **Quality improvement**: Function words now correctly tagged

**What's new in v9:**
- **382,574 POS corrections**: Closed-class words now properly tagged
- **ikka S→D** (39,197): "always" now correctly an adverb
- **mina S→P** (30,896): "I" now correctly a pronoun
- **peale S→K** (26,560): "onto" now correctly an adposition
- **olema Y→V** (16,401): Dialectal verb forms now tagged as verbs
- **kas D→J** (15,967): "whether" now correctly a conjunction
- **And 97 more corrections...**

**Files:**
- `poems_index_v3/` (folder) - Enhanced poem index with POS corrections (split into parts)
- `corpus_full_source_poems_v2.json.gz` (59 MB) - Aggregated corpus with corrected POS counts

### Previous Version (v8 - corpus_full_source_poems)

- **Total word instances processed**: 7,344,568
- **Unique word forms**: 451,371
- **Unique lemmas generated**: 102,361
- **Word-poem pairs tracked**: 5,252,911 (unlimited - was 100/word max)
- **Unique poems in corpus**: 108,125
- **Average occurrences per word**: 16.3
- **Texts processed**: 108,969 runosong poems
- **Unknown words**: 6,190 (0.08%)
- **Average confidence score**: 0.92 (method reliability, not accuracy)

**What's new in v8:**
- **Full source poem tracking**: Removes 100-poem-per-word limit from v7
- **Per-poem occurrence counts**: `source_poems` now stores `{poem_id: count}` instead of list
- **Lemma index source_poems**: Each lemma now tracks which poems it appears in with counts
- **Statistical analysis ready**: Enables geographic distribution, per-poem frequency analysis, TTR calculations
- **All v7 features preserved**: DeepSeek merges, Neurotõlge VRO corrections maintained

### Previous Version (v7 - corpus_deepseek_merged)

- **Total word instances**: 7,344,568
- **Unique lemmas**: 102,361 (-12.2% from v6)
- **DeepSeek lemma merges**: 223,374 corrections applied
- **Lemma consolidation**: Dialectal/orthographic variants merged into canonical forms
- **source_poems limitation**: Limited to 100 poems per word (fixed in v8)

### Earlier Version (v6 - corpus_unknown_reduced)

- **Unique lemmas**: 116,572
- **Unknown words**: 6,190 (0.08%) - 85.3% reduction from v5
- **Neurotõlge VRO corrections**: 35,874

### Method Distribution (v7/v8)

| Method | Word Count | Percentage | Avg Confidence |
|--------|-----------|------------|----------------|
| manual_override | 2,686,600 | 36.58% | 1.000 |
| estnltk+dict | 2,217,690 | 30.19% | 1.000 |
| estnltk | 641,809 | 8.74% | 0.950 |
| dict | 547,719 | 7.46% | 0.643 |
| levenshtein | 232,575 | 3.17% | 0.308 |
| suffix_strip | 194,334 | 2.65% | 0.800 |
| estnltk+dict_jarva_claude_3.5 | 147,874 | 2.01% | 1.000 |
| estnltk_validation_levenshtein_valid | 107,134 | 1.46% | 0.950 |
| estnltk_jarva_claude_3.5 | 61,828 | 0.84% | 0.950 |
| estnltk_estnltk_validated | 57,892 | 0.79% | 0.950 |
| estnltk_deepseek_merged | 55,020 | 0.75% | 0.950 |
| estnltk+dict_deepseek_merged | 49,448 | 0.67% | 1.000 |
| dict_jarva_claude_3.5 | 42,745 | 0.58% | 0.662 |
| neurotolge_vro | 33,950 | 0.46% | 0.000 |
| manual_override_deepseek_merged | 27,182 | 0.37% | 1.000 |
| compound | 26,471 | 0.36% | 0.300 |
| (others) | ~214,000 | ~2.9% | varies |

**Note:** Methods with `_deepseek_merged` suffix indicate lemmas consolidated via DeepSeek R1 validation (223,374 total corrections). Methods with `_validation_` suffix indicate validation-based improvements from v5.

### Quality Distribution

| Quality Tier | Unique Words | Percentage |
|-------------|-------------|------------|
| high_confidence | 240,264 | 53.2% |
| medium_confidence | 55,608 | 12.3% |
| low_confidence | 16,166 | 3.6% |
| needs_review | 139,333 | 30.9% |

## Files Included

### Current Version (v9 - December 2025) ✨ NEW

- **`poems_index_v3/`** (folder, 135 MB total) - POS-corrected poem index (split into 3 parts)
- **`corpus_full_source_poems_v2.json.gz`** (59 MB) - Corpus with corrected POS distributions

**What's new in v9:**
- **POS tag corrections**: 102 systematic corrections applied to 382,574 tokens
- **Function word classification**: Pronouns, adverbs, adpositions, conjunctions now correct
- **Distribution shift**: S (nouns) -325,286 → P/D/K/V/J gains
- **Documentation**: See `POS_SUBSTITUTION_ANALYSIS_REPORT.md` for full analysis

**Top corrections by token count:**

| Substitution | Tokens | Explanation |
|--------------|--------|-------------|
| ikka S→D | 39,197 | "always" is adverb |
| mina S→P | 30,896 | "I" is pronoun |
| peale S→K | 26,560 | "onto" is adposition |
| olema Y→V | 16,401 | dialectal verb |
| kas D→J | 15,967 | "whether" is conjunction |

**Assembly (poems_index_v3):**
```bash
cd poems_index_v3
./assemble.sh  # Creates ../poems_index_v3.json.gz
```

### Previous Version (v8 - December 2025)

- **`corpus_full_source_poems.json.gz`** (62 MB) - Corpus with full source poem tracking

**What was new in v8:**
- **Unlimited source_poems**: No more 100-poem limit per word (v7 had this limit)
- **Per-poem counts**: `source_poems` now stores `{poem_id: occurrence_count}` instead of list
- **Lemma source_poems**: `lemma_index` now includes `source_poems` field with per-poem counts
- **Statistical enablement**: Word "ei" now has 31,988 poems tracked (was limited to 100)
- **Lemma "olema"**: Now tracks 59,681 poems with occurrence counts
- **All v7 features preserved**: DeepSeek merges, Neurotõlge VRO corrections, 102,361 lemmas

### Previous Version (v7 - December 2025)

- **`corpus_deepseek_merged.json.gz`** (35 MB) - Corpus with DeepSeek lemma merges

**What was new in v7:**
- **Lemma consolidation**: 102,361 unique lemmas (reduced from 116,572, -12.2%)
- **DeepSeek R1 validation**: 223,374 lemma merge corrections applied
- **Merged variants**: Dialectal/orthographic variants unified (e.g., neid→neiu, peig→peiu)
- **source_poems limitation**: Limited to 100 poems per word (fixed in v8)

### Earlier Version (v6 - November 2025)

- **`corpus_unknown_reduced.json.gz`** (34 MB) - Corpus with Neurotõlge VRO improvements
- **`corpus_unknown_reduced.db`** (77 MB) - SQLite database for efficient querying
- **`poems_index.json.gz`** (82 MB) - Complete poem index with preserved word order and annotations
- **`poems_index_v2/`** (folder) - Enhanced v2 index split into parts (see "poems_index_v2" section below)
- **`CORPUS_UNKNOWN_REDUCED_README.md`** - Detailed documentation for v6 corpus
- **`DOCUMENTATION_ET.md`** - Estonian language documentation of annotation process
- **`examples/`** - Code examples for using the corpus

**What was new in v6:**
- **Unknown word reduction**: 85.3% decrease (42,070 → 6,190 instances)
- **Neurotõlge VRO corrections**: 35,874 dialectal improvements (0.49% of corpus)
- **Lemma consolidation**: 116,572 unique lemmas (reduced from 125,162)
- **Coverage**: 99.92% of corpus now has valid lemmas

### Earlier Versions

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
    "unique_lemmas": 102361,
    "created": "2025-12-14 HH:MM:SS",
    "version": "v6_full_source_poems",
    "features": [
      "aggregated_storage",
      "reverse_lemma_index",
      "full_source_poem_tracking",
      "source_poems_with_counts",
      "lemma_index_source_poems",
      "..."
    ]
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
      "source_poems": {
        "89248": 15,
        "89250": 3,
        "89255": 7,
        "...": "..."
      }
    }
  },

> **v8 Note:** `source_poems` is now a dict mapping `poem_id → occurrence_count` (was a list limited to 100 entries in v7 and earlier). The sum of all values equals `total_count`.

  "lemma_index": {
    "piir": {
      "word_forms": ["piir", "piiri", "piire", "piirid"],
      "total_occurrences": 2847,
      "source_poems": {
        "89248": 5,
        "89260": 3,
        "90105": 2,
        "...": "..."
      },
      "form_distribution": {
        "piiri": {"count": 787, "forms": ["sg_g", "sg_p"], "confidence_avg": 1.0}
      }
    }
  },

> **v8 Note:** `lemma_index` now includes `source_poems` field (new in v8) tracking which poems each lemma appears in with occurrence counts. The sum of `source_poems` values equals `total_occurrences`.

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
2. **`words`** - Main word form index (451,371 unique forms) with aggregated statistics and full source_poems tracking
3. **`lemma_index`** - Reverse index from lemmas to word forms (102,361 lemmas, **alphabetically sorted**) with source_poems tracking (v8)
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

# Load the corpus (use corpus_full_source_poems.json.gz for v8)
with gzip.open('corpus_full_source_poems.json.gz', 'rt', encoding='utf-8') as f:
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

### v8 Statistical Analysis Examples

The v8 corpus enables comprehensive statistical analysis with full source poem tracking:

**Get word distribution across poems:**
```python
# Word frequency per poem (v8 feature)
word = 'ei'
data = corpus['words'][word]
source_poems = data['source_poems']  # dict: {poem_id: count}

print(f"Word '{word}' appears in {len(source_poems):,} poems")
print(f"Total occurrences: {sum(source_poems.values()):,}")
print(f"Average per poem: {sum(source_poems.values()) / len(source_poems):.1f}")

# Top poems for this word
top_poems = sorted(source_poems.items(), key=lambda x: -x[1])[:5]
for poem_id, count in top_poems:
    print(f"  Poem {poem_id}: {count} occurrences")
```

**Analyze lemma distribution (v8 feature):**
```python
# Lemma now has source_poems (new in v8)
lemma = 'olema'
data = corpus['lemma_index'][lemma]
source_poems = data['source_poems']  # dict: {poem_id: count}

print(f"Lemma '{lemma}' appears in {len(source_poems):,} poems")
print(f"Word forms: {len(data['word_forms']):,}")
print(f"Total occurrences: {data['total_occurrences']:,}")

# Geographic/dialectal distribution possible via poem metadata
```

**Calculate type-token ratio for a poem:**
```python
def calculate_ttr(corpus, poem_id):
    """Calculate type-token ratio for a specific poem (v8 feature)."""
    types = 0
    tokens = 0

    for word, data in corpus['words'].items():
        count = data['source_poems'].get(str(poem_id), 0)
        if count > 0:
            types += 1
            tokens += count

    return types / tokens if tokens > 0 else 0

# Example: TTR for poem 89248
ttr = calculate_ttr(corpus, 89248)
print(f"Poem 89248 TTR: {ttr:.3f}")
```

**Find poems with co-occurring words:**
```python
def find_co_occurring_poems(corpus, word1, word2):
    """Find poems where both words appear (v8 feature)."""
    poems1 = set(corpus['words'].get(word1, {}).get('source_poems', {}).keys())
    poems2 = set(corpus['words'].get(word2, {}).get('source_poems', {}).keys())
    return poems1 & poems2

# Find poems with both "ema" and "isa"
common_poems = find_co_occurring_poems(corpus, 'ema', 'isa')
print(f"Poems with both 'ema' and 'isa': {len(common_poems)}")
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

## poems_index_v2 (Enhanced with Verse Structure)

Version 2 of the poems index adds verse line structure and enhanced metadata.

### Assembly Required

The v2 index (135 MB) is split into 3 parts due to GitHub's 100 MB file size limit:

```bash
cd poems_index_v2
./assemble.sh  # or: python assemble.py
```

After assembly, `poems_index_v2.json.gz` will be created in the parent directory.

### New Features in v2

| Feature | Description |
|---------|-------------|
| `verse_lines` | Array of verse strings (split by `/` markers) |
| `verse_index` | Per-word position indicating which verse the word belongs to |
| `word_in_verse` | Word position within its verse |
| `text` | Original text with `/` verse markers preserved |
| `is_empty` | Flag for 844 empty poems |
| `metadata` | Enhanced: places, collectors, types, year, collection |

### v2 Statistics

| Metric | Value |
|--------|-------|
| Total poems | 108,969 |
| Total words | 7,344,574 |
| Total verses | 2,005,147 |
| Empty poems | 844 |
| File size | 135 MB |

### v2 Poem Structure

```json
{
  "89248": {
    "text": "piiri pääri pääsuke / kus su kullas pesake / ...",
    "text_flat": "piiri pääri pääsuke kus su kullas pesake ...",
    "verse_lines": ["piiri pääri pääsuke", "kus su kullas pesake", ...],
    "verse_count": 22,
    "words": [
      {
        "original": "piiri",
        "lemma": "piir",
        "pos": "S",
        "form": "sg_g",
        "verse_index": 0,
        "word_in_verse": 0,
        "method": "estnltk+dict",
        "confidence": 1.0
      }
    ],
    "is_empty": false,
    "metadata": {
      "title": "AES, MT 3, 1 (1)",
      "collection": "erab",
      "places": ["Viru-Jaagupi", "Viru-Nigula"],
      "year": "...",
      "types": ["..."],
      "collectors": ["..."]
    }
  }
}
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
- **Source traceability**: Full poem tracking with occurrence counts (v8: unlimited poems per word, with per-poem frequency)
- **Confidence scoring**: 0-1 scale reflecting method reliability (not accuracy)
- **Ambiguity marking**: 14,238 words with genuine lemma competition (v4: EstNLTK-validated, was 24,777 in v3, 106,821 in v2)
- **Frequency data**: Corpus-based frequency information

## Lemma Validation Status

**V8 Full Source Poems** (102,361 unique lemmas):
- **Full source poem tracking**: 5,252,911 word-poem pairs (unlimited per word)
- **Per-poem occurrence counts**: `source_poems` stores `{poem_id: count}` not just presence
- **Lemma index source_poems**: NEW field tracking poem distribution for each lemma
- **Example - word "ei"**: 31,988 poems tracked (was limited to 100)
- **Example - lemma "olema"**: 59,681 poems tracked with counts
- **Statistical analysis enabled**: Geographic distribution, TTR, frequency analysis
- **All v7 features preserved**: DeepSeek merges, Neurotõlge VRO, 102,361 lemmas

**V7 DeepSeek Merged** (102,361 unique lemmas):
- **12.2% lemma reduction** via DeepSeek R1 merge validation (116,572 → 102,361)
- **223,374 merge corrections** across 1,090 batch files
- **Dialectal variant unification** (e.g., neid→neiu: 14,593, peig→peiu: 6,045)
- **All v6 features preserved** (Neurotõlge VRO, unknown word coverage)

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

### Gold Standard and Evaluation

The corpus was evaluated against a TEST set of 2,352 words from 74 poems. This TEST set was extracted from a larger gold standard (6,405 words, 94 poems) by excluding word-lemma pairs already used for corpus `manual_override` entries:

| Set | Words | Poems | Purpose |
|-----|------:|------:|---------|
| TRAIN | 4,053 | 94 | Words used for manual_override (circular validation) |
| TEST | 2,352 | 74 | Words NOT used for manual_override (independent evaluation) |

### Three-Tier Evaluation Results

| Tier | Description | Words | V5 Baseline | V7 Result | Change |
|------|-------------|------:|------------:|----------:|-------:|
| **Tier 1** | Pure automatic methods | 1,988 | 66.35% | **67.00%** | +0.65% |
| **Tier 2** | Context-dependent | 364 | 37.64% | **36.81%** | -0.83% |
| **Tier 3** | Overall TEST | 2,352 | 61.90% | **62.33%** | +0.43% |

Tier 2 contains words where the same word form requires different lemmas in different contexts (polysemy). The corpus stores multiple lemmas per word form, but evaluation uses the highest-count lemma.

### Automatic Method Performance (V7)

| Method | Accuracy | Coverage |
|--------|----------|----------|
| estnltk+dict | 84.1% | 42.3% |
| dict | 66.7% | 11.6% |
| estnltk | 53.7% | 12.0% |
| levenshtein | 40.4% | 5.8% |
| suffix_strip | 41.9% | 4.0% |

The V7 corpus with 223,374 DeepSeek lemma merge corrections shows +0.43% overall improvement while reducing unique lemmas by 12.2% (116,572 → 102,361).

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



