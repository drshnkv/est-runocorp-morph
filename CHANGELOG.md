# Changelog

All notable changes to the Estonian Runosong Morphological Corpus will be documented in this file.

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
