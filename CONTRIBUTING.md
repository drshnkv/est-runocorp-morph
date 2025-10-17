# Contributing to Estonian Runosong Morphological Corpus

Thank you for your interest in improving the Estonian Runosong Morphological Corpus!

## How to Contribute

### Reporting Issues

If you find errors or inconsistencies in the corpus annotation:

1. **Check existing issues** - Someone may have already reported it
2. **Create a new issue** with:
   - Word form and lemma in question
   - Expected annotation vs actual annotation
   - Context (poem ID if available)
   - Linguistic justification for the correction

### Suggesting Improvements

We welcome suggestions for:

- **Annotation corrections** - Specific lemmatization errors
- **Quality improvements** - Better confidence scoring methods
- **Documentation enhancements** - Clearer explanations
- **Code examples** - New usage patterns or analyses
- **Methodological insights** - Alternative processing approaches

### Submitting Corrections

For small corrections (< 10 words):
1. Open an issue with the corrections
2. Provide linguistic justification

For larger corrections (> 10 words):
1. Create a CSV file with columns: `word, current_lemma, proposed_lemma, justification`
2. Open an issue and attach the CSV
3. Include sources (EKSS, dialect dictionaries, etc.)

## Annotation Standards

All corrections should follow these principles:

### Lemma Selection Standards

1. **Declinable words**: Singular nominative (sg Nom)
2. **Comparative forms**: Positive degree in singular nominative
3. **Verbs**: ma-infinitive (supine) per EKSS standard
4. **Invariable words**: Same written form
5. **Compound words**: Complete compound in sg Nom/ma-infinitive

### Dialectal Material Guidelines

- **Diminutives**: Use -ke form (not -kene)
- **Derivational morphology**: Keep suffixes/infixes for distinct lemmas
- **Fallback hierarchy**: EKSS → Finnish cognate → Finnic languages → dialectal form
- **Standard references**: Use EKSS, synaq.org, arhiiv.eki.ee/dict/vms/, arhiiv.eki.ee/dict/ems/

### Citation Requirements

For dialectal or archaic forms:
- Provide source (dictionary, reference grammar)
- Explain morphological reasoning
- Note regional variation if applicable

## Code Contributions

### Example Scripts

If you create useful analysis scripts:

1. Follow the style in `examples/` directory
2. Include clear docstrings
3. Add comments for non-obvious operations
4. Test with the actual corpus files
5. Update `examples/README.md`

### Code Style

**Python:**
- PEP 8 compliance
- Type hints encouraged
- Clear variable names
- Comprehensive docstrings

**SQL:**
- Clear commenting
- Readable formatting
- Explain complex queries
- Test before submitting

## Review Process

1. **Linguistic review** - Correctness of annotation
2. **Data integrity check** - No breaking changes
3. **Documentation update** - Keep docs in sync
4. **Community feedback** - Open discussion period

## Questions?

Open an issue with the "question" label. We aim to respond within 1 week.

## License

By contributing, you agree that your contributions will be licensed under CC BY 4.0, the same license as the corpus.

## Acknowledgments

All contributors will be acknowledged in future corpus versions and in the project documentation.

## Contact

For major contributions or collaboration inquiries, please contact the maintainers through GitHub issues.

---

**Note**: This is a scholarly linguistic resource. All contributions should prioritize **linguistic accuracy** and **scholarly rigor** over convenience or automation.
