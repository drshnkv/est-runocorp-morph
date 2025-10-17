# Estonian Runosong Morphological Corpus

> **⚠️ Experimental Non-LLM Baseline Corpus – Version 1**
>
> This corpus represents automated morphological annotation using **EstNLTK + dictionary methods** for archaic dialectal Estonian texts where no gold standard exists.
>
> **Estimated accuracy: 60-70%** based on previous evaluation experiments. The confidence scores (average 0.92) reflect method reliability estimates, not actual annotation accuracy. This corpus serves as a methodological baseline for comparing with LLM-based approaches, which show better results but are still work in progress.

A morphologically annotated corpus of 108,969 Estonian runosongs (traditional folk poetry), containing 7.3 million word instances processed with non-LLM methods.

## Overview

This corpus provides automated morphological annotation of Estonian dialectal runosong texts, combining EstNLTK 1.7.4 morphological processing with extensive dictionary resources (175,493 unique word forms). The annotation includes part-of-speech tags, morphological forms, lemmatization, and confidence scoring across multiple processing methods.

**Part of**: EKKD Project 2025-2027 (Estonian Cultural Endowment)
**Version**: v3 (2025)
**License**: CC BY 4.0

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

- **`corpus_runosongs_v2_corrected_FIXED.json.gz`** (42 MB) - Complete corpus data with all annotations
- **`corpus_runosongs_v2_FIXED.db`** (79 MB) - SQLite database for efficient querying
- **`DOCUMENTATION_ET.md`** - Estonian language documentation of annotation process
- **`examples/`** - Code examples for using the corpus

## Data Structure

### JSON Format (Primary)

The JSON corpus contains complete morphological annotation with the following structure:

```json
{
  "words": {
    "piiri": {
      "lemmas": {"piir": 42},
      "pos_tags": {"S": 42},
      "forms": {"sg_g": 37, "sg_p": 5},
      "methods": {"estnltk+dict": 42},
      "total_count": 42,
      "avg_confidence": 1.0,
      "source_poems": ["ERA.1.1.1", "..."],
      "quality": "high_confidence"
    }
  },
  "lemma_index": {
    "piir": ["piir", "piiri", "piire", "piirid"]
  },
  "ambiguous_words": {
    "kand": {
      "competing_lemmas": {"kand": 45, "kanna": 12},
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
- `avg_confidence` (REAL)
- `primary_method` (TEXT)

**`lemma_variants` table:**
- `lemma` (TEXT)
- `word_form` (TEXT)
- `count` (INTEGER)
- `avg_confidence` (REAL)

**`method_stats` table:**
- `method` (TEXT PRIMARY KEY)
- `word_count` (INTEGER)
- `percentage` (REAL)
- `avg_confidence` (REAL)

**`ambiguous_words` table:**
- `word` (TEXT PRIMARY KEY)
- `num_competing_lemmas` (INTEGER)
- `needs_review` (INTEGER)

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
SELECT method, word_count, percentage, avg_confidence
FROM method_stats
ORDER BY word_count DESC;
```

See the `examples/` directory for more code samples.

## Annotation Methodology

### Three-Tier Correction System

The corpus underwent automated correction using a hybrid scoring system:

- **Tier 1** (high confidence): 588,046 corrections validated by Vabamorf morphological analyzer
- **Tier 2** (medium confidence): 2,608 corrections from dictionary without Vabamorf validation
- **Tier 3** (low confidence): 38,533 corrections from low-similarity matches

Total: 629,187 automated corrections

### Hybrid Ranking System

For selecting among multiple lemma candidates:
- **60%** edit distance (Levenshtein distance from original form)
- **40%** frequency score (based on University of Tartu literary corpus)

The frequency component helps select more likely correct lemmas, as words appearing more frequently in literary texts are generally more common in runosongs as well. Tested on 448,217 low-confidence words, resulting in 119,184 (26.6%) alternative lemmas selected.

### Processing Pipeline

1. **EstNLTK+dict** (33%): Morphological analysis confirmed by dictionary entries
2. **Manual override** (37%): Expert-annotated lemmas from FILTER project corpus
3. **EstNLTK** (14%): Pure morphological analysis
4. **Dict** (8%): Direct dictionary match without morphological confirmation
5. **Levenshtein** (4%): Fuzzy matching for dialectal variants
6. **Other methods** (4%): Suffix stripping, h-variation, compound analysis, etc.

## Key Features

- **POS tagging**: Morphological classification for processed words
- **Morphological forms**: Case/number/tense markers (sg_g, pl_p, etc.)
- **Quality categorization**: Four-tier assessment based on method and validation
- **Method tracking**: Transparent annotation provenance for each word
- **Source traceability**: Links to original poem identifiers
- **Confidence scoring**: 0-1 scale reflecting method reliability (not accuracy)
- **Ambiguity marking**: 106,821 words flagged as potentially ambiguous
- **Frequency data**: Corpus-based frequency information

## Lemma Validation Status

Of 192,756 unique lemmas generated:
- **60,993 (31.6%)** can be validated with standard Estonian morphology (using EstNLTK/Vabamorf)
- **131,763 (68.4%)** are archaic/dialectal forms or unvalidated word forms

Note: Validation here means the lemma is recognized by standard Estonian morphological tools, not that the lemmatization is necessarily correct for the specific context.

## Citation

If you use this corpus in your research, please cite:

```
Estonian Runosong Morphological Corpus v3 (2025)
EKKD Project 2025-2027
https://github.com/drshnkv/est-runocorp-morph
License: CC BY 4.0
```

## Technical Details

- **Processing environment**: Google Colab with parallel batch processing
- **Batch structure**: 1090 batches (~100 poems each)
- **Morphological analyzer**: EstNLTK 1.7.4 with Vabamorf
- **Validation mode**: Strict (guess=False, propername=False, compound=False)
- **Dictionary sources**: Combined index of 175,493 unique entries
- **Processing time**: ~6 minutes for complete corpus (7.3M words)

## Related Resources

- [EstNLTK Documentation](https://estnltk.github.io/)
- [Vabamorf](https://github.com/Filosoft/vabamorf)
- [EKSS Dictionary](https://www.eki.ee/dict/ekss/)
- [Estonian Dialectology](https://www.eki.ee/murded/)

## Contact

For questions or issues with this corpus, please open an issue on GitHub.

## Acknowledgments

This corpus was created as part of the EKKD Project 2025-2027, funded by the Estonian Cultural Endowment. Special thanks to the FILTER research group for manual annotation data.

## License

This corpus is released under **CC BY 4.0** (Creative Commons Attribution 4.0 International).

You are free to:
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit and indicate if changes were made
