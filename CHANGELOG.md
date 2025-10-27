# Changelog

All notable changes to the Estonian Runosong Morphological Corpus will be documented in this file.

## [1.1.0] - 2025-10-27

### Added
- V5 corpus with validation-based improvements and complete vocabulary
- Unknown words now included in corpus (42,389 words, 0.58%)
- Complete vocabulary coverage for comprehensive text analysis
- Enhanced method provenance tracking with `_validation_[method]_[status]` format

### Changed
- 214,968 validation-based lemma corrections applied (2.93% of corpus)
- Invalid lemma cleanup: 167,994 → 125,600 unique lemmas (-25.2%)
- Updated poems_index.json.gz with validation-improved annotations
- Total word instances: 7,302,185 → 7,344,574 (+42,389 unknowns)
- Unique word forms: 427,472 → 452,161 (+24,689)

### Validation Performance
- **Overall success rate**: 67.9% valid corrections (146,038 / 214,968)
- **Dict validation**: 91.4% valid (896 / 980)
- **Levenshtein validation**: 86.7% valid (121,232 / 139,875)
- **H-variation validation**: 81.6% valid (2,651 / 3,250)
- **Suffix-strip validation**: 61.0% valid (21,259 / 34,850)
- **Compound validation**: 0.0% valid (morphological decompositions, informative)

### Quality Preservation
- 2,713,782 manual corrections preserved
- 280,380 Järva Claude 3.5 corrections preserved
- 2,994,162 total high-quality lemmas maintained

### Note
Corpus accuracy evaluation awaits manual gold standard validation. Previous cross-reference with LLM annotations (361 Järva poems) showed 74.4% baseline accuracy, but this is not a definitive gold standard.

## [1.0.0] - 2025-10-19

### Added
- Initial release of Estonian Runosong Morphological Corpus
- 7.3 million word instances from 108,969 runosongs
- Automated morphological annotation using EstNLTK 1.7.4 + lexical resources
- SQLite database for efficient querying
- Comprehensive documentation in English and Estonian
- Code examples for Python and SQL usage

### Validated
- Quality testing against LLM-annotated Järva corpus (361 poems, 23,356 tokens)
- Achieved 74.4% exact match accuracy
- Confirms corpus quality at upper end of 60-70% estimated range

## Methodology

- **EstNLTK+dict**: Combined morphological analysis and dictionary validation (33%)
- **Manual overrides**: Expert-annotated lemmas from FILTER project (37%)
- **EstNLTK**: Pure morphological analysis (14%)
- **Other methods**: Dictionary matching, fuzzy matching, suffix stripping (16%)
