# poems_index_v3 - POS-Corrected Poem Index

This directory contains the split parts of `poems_index_v3.json.gz`, the POS-corrected version of the Estonian runosong corpus poem index.

## Quick Start

```bash
# Run assembly script
./assemble.sh

# Or with Python
python assemble.py

# Decompress the assembled file
gunzip -k ../poems_index_v3.json.gz
```

## What's New in v3

**382,574 POS corrections applied** to manual_override entries, improving the accuracy of closed-class word tagging.

| Statistic | Value |
|-----------|-------|
| Substitution rules applied | 102 |
| Total poems | 108,969 |
| Poems with corrections | 71,788 (65.9%) |
| Manual override words | 2,713,782 |
| Words corrected | 382,574 (14.1%) |

### Top 10 Corrections

| Substitution | Tokens | Explanation |
|--------------|--------|-------------|
| ikka S->D | 39,197 | "always" is adverb, not noun |
| mina S->P | 30,896 | "I" is pronoun, not noun |
| peale S->K | 26,560 | "onto" is adposition, not noun |
| olema Y->V | 16,401 | "to be" is verb, not abbreviation |
| kas D->J | 15,967 | "whether" is conjunction, not adverb |
| olema S->V | 15,524 | "to be" is verb, not noun |
| seal S->D | 10,665 | "there" is adverb, not noun |
| vastu V->K | 9,464 | "towards" is adposition, not verb |
| see S->P | 9,133 | "this" is pronoun, not noun |
| siis S->D | 8,662 | "then" is adverb, not noun |

## File Structure

| File | Size | Description |
|------|------|-------------|
| `poems_index_v3.json.gz.aa` | 50 MB | Part 1 of 3 |
| `poems_index_v3.json.gz.ab` | 50 MB | Part 2 of 3 |
| `poems_index_v3.json.gz.ac` | 35 MB | Part 3 of 3 |
| `assemble.sh` | - | Bash assembly script |
| `assemble.py` | - | Python assembly script |
| `checksum.md5` | - | MD5 checksum for verification |

## Checksum

```
0ef619a0d4c8af6396e55ad732253568  poems_index_v3.json.gz
```

## Changes from v2

- Applied 102 verified POS substitutions to manual_override entries
- Function words now correctly classified (pronouns, adverbs, adpositions)
- See `../POS_SUBSTITUTION_ANALYSIS_REPORT.md` for full methodology

## Related Files

- `../corpus_full_source_poems_v2.json.gz` - Aggregated corpus with corrected POS counts
- `../final_substitutions.csv` - The 102 substitution rules applied
- `../POS_SUBSTITUTION_ANALYSIS_REPORT.md` - Full analysis report
