# CLAUDE.md

## ⚠️ CRITICAL: Git Commit Policy (Institutional Repository)

**NEVER include Claude as co-author in ANY commit messages.**

When creating git commits for this project:
- Do NOT add "Co-Authored-By: Claude" or any similar attribution
- Do NOT add "🤖 Generated with Claude Code" or similar
- Do NOT mention Claude, AI, or LLM in commit messages
- Use only the standard commit message format without any AI attribution

This is an institutional/academic repository where AI attribution is not acceptable.

**Example commit format to use:**
```
feat: Add new feature description

Detailed description of changes if needed.
```

**Do NOT use:**
```
feat: Add new feature

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Identity

This directory (`est-runocorp-morph-standalone/`) is the **local git clone** of:
- **GitHub:** https://github.com/drshnkv/est-runocorp-morph

All commits and pushes from this directory go to the GitHub repository.

# Estonian Runosong Morphological Corpus Project

This repository contains tools for creating, analyzing, and improving morphological annotations for Estonian runosong (traditional folk poetry) corpus.

## Project Structure

### est-runocorp-morph-standalone/
Main corpus generation and analysis directory with tools for:
- Generating similarity pairs between lemmas
- Creating overview CSVs for human review
- Viewing annotated poems
- LLM-based annotation pilot tests

### lemma_pair_review_pipeline/
AI-powered lemma pair review system using DeepSeek/Claude APIs:
- Batch processing of 86,741 lemma pairs
- Checkpoint-based resumable processing
- Context-enriched decision extraction
- Frequency-ranked word form analysis

## Key Commands

### Corpus Analysis & Generation

```bash
cd /Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/est-runocorp-morph-standalone

# Generate lemma similarity pairs for review
python3 generate_lemma_similarity_pairs.py

# Generate comprehensive lemma overview CSV (21 columns, 116K+ lemmas)
python3 generate_lemma_overview_v2.py

# View specific poem with annotations
cd examples
python3 view_poem.py 89248 --detailed

# View random high-quality poems
python3 view_poem.py --random 5 --min-confidence 0.95
```

### Lemma Pair Review Pipeline

```bash
cd /Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/lemma_pair_review_pipeline

# Setup DeepSeek API key
export DEEPSEEK_API_KEY="your-key-here"

# Run complete review pipeline
python3 review_lemma_pairs_deepseek.py --pairs-csv lemma_similarity_pairs.csv

# Resume from specific batch (after interruption)
python3 review_lemma_pairs_deepseek.py --resume
python3 review_lemma_pairs_deepseek.py --start-batch 310

# Extract decisions from checkpoints
python3 extract_decisions_with_contexts.py

# Custom extraction
python3 extract_decisions_with_contexts.py --output-prefix my_results
```

## Architecture & Data Flow

### Lemma Pair Review Pipeline Architecture

```
1. Pre-filtering (auto_merge_plus_sign.py)
   ├─ Auto-merge pairs differing only by + sign
   └─ Output: auto_merged_plus_sign.json + lemma_pairs_for_llm_review.csv

2. Prompt Generation (prompt_generator.py)
   ├─ Load poems_index.json.gz (108,969 poems)
   ├─ Extract top 20 frequent word forms + 5 context examples per lemma
   ├─ Generate batches with full linguistic context
   └─ Output: prompts/batch_XXXX_prompt.txt

3. API Processing (review_lemma_pairs_deepseek.py)
   ├─ DeepSeek API calls with retry mechanism (3 attempts, exponential backoff)
   ├─ Batch size: 25 pairs (fits 131K token limit)
   ├─ Checkpointing: checkpoints/priority1_batch_XXXX.json
   └─ Output: responses/batch_XXXX_response.json

4. Decision Extraction (extract_decisions_with_contexts.py)
   ├─ Read checkpoints for LLM decisions
   ├─ Parse prompts for frequency-ranked word forms
   ├─ Extract contextual usage examples
   └─ Output: extracted_merge_decisions.csv (33 fields)
            extracted_keep_separate_corrected.csv (30 fields)
```

### Two-Source Data Approach

**Checkpoint files** (decisions + metadata):
- Contain LLM linguistic judgments (decision, confidence, suggested lemmas)
- Truncated word forms (~20 alphabetical)
- Fast resumable processing

**Prompt files** (complete linguistic context):
- Complete word form lists with frequencies (e.g., 1,320 forms for "olema")
- Top 20 by frequency: "on (59,000), oli (41,152), om (16,401)..."
- 5 contextual text fragments per lemma showing actual usage

**Why both sources?**
- Checkpoints optimize for storage/resumability but truncate data
- Prompts preserve complete linguistic context as presented to LLM
- Extraction combines both for comprehensive CSV output

### DeepSeek Linguistic Judgments vs Frequency

The pipeline prioritizes **DeepSeek's suggested lemmas** over simple frequency-based selection:

```python
# CORRECT: Use DeepSeek's linguistic analysis
target_lemma = suggested_lemma_1  # e.g., "kubjas" (standard Estonian noun form)
source_lemma = "kubja"  # dialectal variant

# WRONG: Pure frequency-based (old approach)
target_lemma = more_frequent_lemma  # may select dialectal form
```

**Rationale**: Frequency alone insufficient for Estonian dialectal material - DeepSeek considers POS tags, semantic context, morphological patterns, and standard vs. dialectal forms.

## Data Structures

### Corpus JSON Format (corpus_deepseek_merged.json.gz)

8 main sections:
- `metadata` - Corpus statistics (7.3M words, 116K lemmas)
- `words` - Main word form index (451K forms) with aggregated statistics
- `lemma_index` - Reverse index from lemmas to word forms (alphabetically sorted)
- `ambiguous_words` - Words with multiple competing lemma interpretations (14K words)
- `method_analytics` - Performance statistics for each lemmatization method (76 methods)
- `morphological_patterns` - Distribution of POS + morphological form combinations (81 patterns)
- `quality_tiers` - Quality categorization (4 tiers: high/medium/low/needs_review)
- `corpus_timeline` - Progressive statistics as batches were processed (1,090 entries)

### Poem Index Structure (poems_index.json.gz)

```json
{
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
        }
      ],
      "batch": "batch_00001",
      "num_words": 80
    }
  }
}
```

## Processing Pipeline Resumability

### Checkpoint System
- State file: `checkpoints/review_state.json` tracks current batch/priority
- Batch files: `checkpoints/priority1_batch_XXXX.json` store individual results
- Automatic state saving after each successful batch
- Resume commands check state and continue from last completed batch

### Handling Interruptions
1. **Internet outage**: Retry mechanism handles temporary failures (5s, 10s, 20s delays)
2. **Script termination**: Use `--resume` to continue from last checkpoint
3. **Rate limits**: 2-second delay between batches prevents API throttling

## Critical Processing Notes

### Batch Size Selection
- **DeepSeek**: 25 pairs maximum (131K token context limit)
- **Claude**: 35 pairs possible (larger context window)

Batch size calculated based on:
- System prompt: ~1,200 tokens
- Per-pair context: ~3,500 tokens (word forms + text fragments)
- Response: ~40 tokens per pair

### Notification System
- Terminal bell on completion (\a)
- macOS system sound (Glass.aiff chime)
- macOS Notification Center popup
- Implemented in both review and extraction scripts

### Progress Tracking
Current status files:
- `checkpoints/review_state.json` - Shows current batch (e.g., 901/3,470)
- Batch completion: ~8.9% done in example (309/3,470 batches)

## Estonian Linguistic Standards

### Lemma Selection Rules (EKSS)
1. **Nouns (S)**: Singular nominative (sg_n)
2. **Verbs (V)**: ma-infinitive (supine)
3. **Adjectives (A)**: Singular nominative positive form
4. **Invariable words**: Same written form

### Dialectal Considerations
- Estonian runosongs contain archaic and dialectal forms
- Use closest EKSS dictionary form when available
- For unknown dialectal words, provide best linguistic judgment
- Diminutives: Use -ke form (not -kene)

## Performance Metrics

### Corpus Statistics (v7 - Current)
- Total words: 7,344,568
- Unique word forms: 451,371
- Unique lemmas: 102,361 (-12.2% from v6 via DeepSeek merges)
- DeepSeek merge corrections: 223,374
- Unknown words: 6,190 (0.08%)
- Average confidence: 0.92

### Previous Version (v6)
- Unique lemmas: 116,572
- Neurotõlge VRO corrections: 35,874

### Method Distribution (v7)
- manual_override: 36.6% (expert annotations)
- estnltk+dict: 30.2% (morphology + dictionary)
- estnltk: 8.7% (pure morphological analysis)
- dict: 7.5% (dictionary only)
- *_deepseek_merged: 2.3% (DeepSeek lemma consolidations)
- Other methods: 14.7% (Levenshtein, LLM corrections, etc.)

### Review Pipeline Scale
- Total lemma pairs: 86,741
- Batches to process: 3,470 (batch size 25)
- Estimated processing time: ~48 hours
- Checkpoint frequency: After each batch

## Accessing Poems Index

The `poems_index.json.gz` file (81 MB compressed) requires special handling:

```python
import json
import gzip

# Load poems index
with gzip.open('poems_index.json.gz', 'rt', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total poems: {len(data['poems']):,}")  # 108,969 poems
```

## Common Error Patterns

### API Issues
- **Rate limiting**: Increase `--batch-delay` (default: 2 seconds)
- **Timeout**: Retry mechanism handles automatically
- **Invalid response**: Raw response saved to `responses/batch_XXXX_response_raw.txt`

### Data Extraction Issues
- **Missing word forms**: Script now extracts from prompt files, not checkpoints
- **Incorrect merge targets**: Fixed to use `suggested_lemma_1`/`suggested_lemma_2`
- **Context truncation**: Prompts preserve full 5-fragment context per lemma

## Related Documentation

- `README.md` - Comprehensive corpus documentation
- `EXTRACTION_README.md` - Decision extraction tool details
- `LLM_ANNOTATION_PILOT_README.md` - LLM annotation pilot test guide
- `CHANGELOG.md` - Version history

## Evaluation Documentation

Detailed evaluation methodology and results are documented in:

| Document | Location | Description |
|----------|----------|-------------|
| PUBLICATION_READY_EVALUATION_METHODOLOGY.md | `estnltk_dict_only/updated_scripts_with_manual_seed_corpus/` | Academic paper methodology |
| TRAIN_TEST_SPLIT_README.md | `estnltk_dict_only/updated_scripts_with_manual_seed_corpus/` | Split methodology explanation |
| MANUAL_OVERRIDE_ANALYSIS.md | `estnltk_dict_only/updated_scripts_with_manual_seed_corpus/` | Analysis of manual annotations |
| ENHANCED_EVALUATION_REPORT.md | `estnltk_dict_only/updated_scripts_with_manual_seed_corpus/` | Three-tier evaluation results |

### Evaluation Summary

- **Gold standard:** 6,405 words from 94 poems
- **Excluded from evaluation:** 4,053 words (manual lemmas imported as `manual_override`)
- **Evaluation set:** 2,352 words (automatic methods only)
- **Automatic method accuracy:** 66.35% on 1,988 pure automatic words
- **Best method:** estnltk+dict at 84.08% (50.9% coverage)

## Python Environment

**Required for corpus scripts:**
```bash
# EstNLTK 1.7.4 environment
/Users/kaarelveskis/miniconda3/envs/estnltk-latest-test/bin/python
```

**Required for review pipeline:**
```bash
pip install anthropic  # DeepSeek API client
pip install pandas     # CSV processing
pip install tqdm       # Progress bars
```

## File Naming Conventions

### Corpus Files
- `corpus_*.json.gz` - Main corpus data (gzip compressed)
- `poems_index.json.gz` - Complete poem annotations
- `lemma_overview_v2.csv` - Human-readable lemma summary

### Pipeline Files
- `batch_XXXX_prompt.txt` - Generated prompts with full context
- `batch_XXXX_response.json` - Parsed LLM responses
- `priority1_batch_XXXX.json` - Checkpoint files (resumable)
- `review_state.json` - Current pipeline state

### Extraction Outputs
- `extracted_merge_decisions.csv` - All MERGE/SUGGEST_MERGE decisions
- `extracted_keep_separate_corrected.csv` - KEEP_SEPARATE with corrections

## Development Workflow

1. **Generate similarity pairs** from corpus
2. **Run review pipeline** with DeepSeek API
3. **Extract decisions** with context analysis
4. **Manual review** of extracted CSVs
5. **Apply corrections** to corpus
6. **Regenerate corpus** with improved lemmas
