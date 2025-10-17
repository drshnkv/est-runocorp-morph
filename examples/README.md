# Examples for Estonian Runosong Morphological Corpus

This directory contains code examples for working with the corpus in both Python and SQL.

## Python Examples

### basic_usage.py

Demonstrates fundamental operations:
- Loading the compressed JSON corpus
- Looking up individual words
- Finding all variants of a lemma
- Checking for ambiguous words
- Extracting corpus statistics

**Usage:**
```bash
cd examples
python basic_usage.py
```

### advanced_analysis.py

More sophisticated linguistic analysis:
- POS tag distribution and patterns
- Morphological form analysis
- Quality vs frequency correlation
- Method performance comparison
- Dialectal variant detection
- Ambiguity pattern analysis

**Usage:**
```bash
cd examples
python advanced_analysis.py
```

## SQL Examples

### query_examples.sql

Collection of SQL queries for the SQLite database:

**Query categories:**
1. **Basic queries** - Word lookups, lemma variants, method statistics
2. **Ambiguous words analysis** - Finding words needing expert review
3. **Quality analysis** - Low-confidence words, method-specific queries
4. **Lemma analysis** - Variant counts, frequency analysis
5. **Method comparison** - Confidence metrics across methods
6. **Frequency analysis** - Hapax legomena, distribution patterns
7. **Validation queries** - Data integrity checks
8. **Export queries** - Sample datasets for research

**Usage:**
```bash
# Interactive mode
sqlite3 ../corpus_runosongs_v2_FIXED.db

# Then run queries from the file
.read query_examples.sql

# Or run specific queries
sqlite3 ../corpus_runosongs_v2_FIXED.db < query_examples.sql
```

## Requirements

### Python
- Python 3.7+
- Standard library only (no additional packages required)

### SQL
- SQLite 3
- Available by default on most systems

## Quick Start

1. **Check corpus files are available:**
   ```bash
   ls -lh ../corpus_runosongs_v2_*
   ```

2. **Run basic Python example:**
   ```bash
   python basic_usage.py
   ```

3. **Try SQL queries:**
   ```bash
   sqlite3 ../corpus_runosongs_v2_FIXED.db "SELECT * FROM method_stats;"
   ```

## Example Output

### Python - Word Lookup
```
📝 Word: piiri
  Lemmas: {'piir': 42}
  POS tags: {'S': 42}
  Morphological forms: {'sg_g': 37, 'sg_p': 5}
  Processing methods: {'estnltk+dict': 42}
  Total occurrences: 42
  Average confidence: 1.000
  Quality tier: high_confidence
  Source poems: 38 poems
```

### SQL - Method Statistics
```
method           word_count  percentage  avg_confidence
-------------    ----------  ----------  --------------
manual_override  2713782     37.2        1.000
estnltk+dict     2423711     33.2        1.000
estnltk          1010589     13.8        0.950
dict             617085      8.5         0.647
```

## Tips

1. **For large-scale analysis**: Use the SQLite database for better performance
2. **For detailed word data**: Use the JSON corpus for complete information
3. **For quick exploration**: Start with basic_usage.py to understand the data structure
4. **For research**: Modify query_examples.sql to export custom datasets

## Further Reading

- See `../README.md` for corpus overview and statistics
- See `../DOCUMENTATION_ET.md` for Estonian-language documentation of annotation process
- See corpus build log at `../corpus_v3_build.log` for processing details
