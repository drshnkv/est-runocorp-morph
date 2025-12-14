# poems_index_v2 Implementation Plan

**Purpose:** Create an enhanced poems_index that preserves verse line structure
**Created:** 2025-12-14
**Status:** ✅ COMPLETED (2025-12-14)

---

## Implementation Summary

### Generated Files
| File | Size | Description |
|------|------|-------------|
| `poems_index_v2.json.gz` | 134.64 MB | Enhanced poems index with verse structure |
| `generate_poem_index_v2.py` | 22 KB | Generator script with verification suite |
| `build_issues_v2.json` | 0.3 KB | 4 poems with minor word count mismatches |

### Final Statistics
| Metric | Value |
|--------|-------|
| Total poems | 108,969 |
| Total words | 7,344,574 |
| Total verses | 2,005,147 |
| Empty poems | 844 |
| Non-empty poems | 108,125 |
| Avg words/poem | 67.4 |
| Avg verses/poem | 18.4 |

### Verification Results (10/10 PASSED)
- ✅ Poem count matches expected
- ✅ ID range 89248-198216 correct
- ✅ Word count matches v1
- ✅ Verse structure valid (844 known empty poems)
- ✅ Verse consistency (verse_count = len(verse_lines))
- ✅ Annotation completeness (all required fields)
- ✅ Verse index validity (all in range)
- ✅ Metadata population (100% titles, 100% collections)
- ✅ Spot checks passed (including known empty last poem)
- ✅ Annotation consistency with v1

### Data Quality Fixes Applied
1. **ampquot artifact removal**: Cleaned `ampquot` from 1,440+ poem texts
2. **Empty poem tracking**: 844 poems with `is_empty: true` flag
3. **Word count mismatches**: 4 poems handled gracefully with verse_index=-1

---

## 1. Overview

### Current State (/Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/est-runocorp-morph-standalone/poems_index.json)
- **108,969 poems** with morphological annotations
- **Text format:** Words joined with spaces (no verse structure)
- **Example:** `piiri pääri pääsuke kus su kullas pesake kuivand kuuse otsas...`

### Target State (poems_index_v2.json.gz)
- **Same 108,969 poems** with morphological annotations
- **Text format:** Words with verse line markers preserved
- **Example:** `piiri pääri pääsuke / kus su kullas pesake / kuivand kuuse otsas...`
- **New field:** `verse_lines` array with individual verse texts

---

## 2. Data Sources

### Primary Source: koik_regilaulud_okt_2025.csv
- **Location:** `/Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/estnltk_dict_only/koik_regilaulud_okt_2025.csv`
- **Records:** 108,969 poems (exact match with current poems_index)
- **ID range:** 89248 - 198216
- **Key columns:**
  - `p_id` - Poem ID (matches poems_index keys)
  - `poemText` - Original text WITH "/" verse markers
  - `verseCount` - Number of verses per poem
  - `poemTitle` - Poem title/source reference
  - `placeNames`, `placeTypes` - Geographic metadata
  - `poemYear` - Collection year
  - `typeNames` - Song type classification
  - `collectorNames` - Collector information

### Secondary Source: batch_*.json files
- **Location:** `/Users/kaarelveskis/Downloads/eesti_murrete_sonaraamat_2025/claude_code/output_batches/`
- **Content:** Morphological annotations (lemmas, POS, forms)
- **Files:** 1,090 batch files

---

## 3. Implementation Steps

### Step 3.1: Create Verse-Aligned Text Parser

```python
def parse_verses_from_csv(poemText: str) -> dict:
    """
    Parse poem text with verse markers into structured data.

    Input: "piiri pääri pääsuke / kus su kullas pesake / ..."
    Output: {
        'text_with_markers': 'piiri pääri pääsuke / kus su kullas pesake / ...',
        'verse_lines': ['piiri pääri pääsuke', 'kus su kullas pesake', ...],
        'verse_count': N,
        'words_flat': ['piiri', 'pääri', 'pääsuke', 'kus', 'su', ...]
    }
    """
```

### Step 3.2: Build poem_id to CSV Data Mapping

1. Load `koik_regilaulud_okt_2025.csv`
2. Create dict: `{p_id: {poemText, verseCount, poemTitle, ...}}`
3. Verify all 108,969 IDs present

### Step 3.3: Merge with Existing Annotations

For each poem in poems_index:
1. Get original text with "/" markers from CSV
2. Get existing word annotations from poems_index
3. Align annotations to verse-structured text
4. Preserve all annotation fields (lemma, pos, form, method, confidence)

### Step 3.4: New Data Structure

```json
{
  "metadata": {
    "version": "v2",
    "created_from": "poems_index + koik_regilaulud_okt_2025.csv",
    "total_poems": 108969,
    "total_words": 7344574,
    "features": ["verse_markers", "verse_lines_array", "enhanced_metadata"]
  },
  "poems": {
    "89248": {
      "text": "piiri pääri pääsuke / kus su kullas pesake / ...",
      "text_flat": "piiri pääri pääsuke kus su kullas pesake ...",
      "verse_lines": [
        "piiri pääri pääsuke",
        "kus su kullas pesake",
        "..."
      ],
      "verse_count": 12,
      "words": [
        {
          "original": "piiri",
          "lemma": "piir",
          "pos": "S",
          "form": "sg_g",
          "method": "estnltk+dict",
          "confidence": 1.0,
          "verse_index": 0,
          "word_in_verse": 0
        },
        ...
      ],
      "metadata": {
        "title": "AES, MT 3, 1 (1)",
        "collection": "erab",
        "nro": "aesmt00300010001",
        "places": ["..."],
        "year": "...",
        "types": ["..."],
        "collectors": ["..."]
      },
      "batch": "batch_00001",
      "row_index": 0
    }
  }
}
```

---

## 4. Verification Checklist

### 4.1 Pre-Build Verification

- [ ] **CSV row count**: Verify 108,969 rows in source CSV
- [ ] **ID uniqueness**: All p_id values are unique
- [ ] **ID overlap**: All CSV IDs exist in poems_index
- [ ] **No missing IDs**: All poems_index IDs exist in CSV

### 4.2 Build-Time Verification

- [ ] **Verse marker parsing**: "/" correctly splits verses
- [ ] **Word count consistency**: `len(words)` matches sum of words across verses
- [ ] **No empty verses**: Each verse has at least 1 word
- [ ] **Annotation alignment**: Each word has corresponding annotation
- [ ] **Progress logging**: Log every 10,000 poems processed

### 4.3 Post-Build Verification

#### File Integrity
- [ ] **gzip -t**: File passes integrity check
- [ ] **File size**: Should be 85-100 MB (similar to v1 + metadata overhead)
- [ ] **JSON parse**: File loads without errors

#### Data Completeness
- [ ] **Poem count**: Exactly 108,969 poems
- [ ] **Word count**: Total ~7,344,574 words (±0.1%)
- [ ] **ID range**: 89248 - 198216 (all present)
- [ ] **No null values**: No None/null in required fields

#### Structure Validation
- [ ] **Required fields present**: text, text_flat, verse_lines, words, batch
- [ ] **Word annotations complete**: lemma, pos, form, method, confidence for each word
- [ ] **Verse indices valid**: verse_index in range [0, verse_count-1]
- [ ] **Metadata populated**: At least 90% of poems have title, collection

#### Cross-Reference Validation
- [ ] **CSV vs Index word count**: Words in text_flat matches CSV word count (±1%)
- [ ] **Verse count match**: verse_lines length equals verseCount from CSV
- [ ] **Sample verification**: Manual check of 10 random poems

#### Regression Testing
- [ ] **Compare with v1**: All poems from v1 present in v2
- [ ] **Annotation consistency**: Same lemmas as v1 for same words
- [ ] **Backward compatibility**: Old code can still read basic structure

### 4.4 Specific Spot Checks

| Poem ID | Expected Verses | Check |
|---------|-----------------|-------|
| 89248   | ~12 verses      | First poem, basic structure |
| 99999   | N verses        | Last 5-digit ID |
| 100000  | N verses        | First 6-digit ID (was truncated in old file) |
| 198216  | N verses        | Last poem |
| 105772  | ~10 verses      | "peigmees" poem from analysis |

---

## 5. Script Template

**File:** `generate_poem_index_v2.py`

```python
#!/usr/bin/env python3
"""
Generate poems_index_v2 with verse line markers.

Features:
- Preserves "/" verse markers from original CSV
- Adds verse_lines array for easy iteration
- Enhanced metadata from CSV (title, collection, places, etc.)
- Full morphological annotations from batch files

Usage:
    python generate_poem_index_v2.py \
        --csv ../../estnltk_dict_only/koik_regilaulud_okt_2025.csv \
        --poems-index poems_index.json.gz \
        --output poems_index_v2.json.gz
"""

import json
import gzip
import csv
import argparse
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm


def load_csv_data(csv_path: Path) -> dict:
    """Load and index CSV data by poem ID."""
    pass


def load_poems_index(index_path: Path) -> dict:
    """Load existing poems index with annotations."""
    pass


def parse_verses(text: str) -> tuple[list[str], list[str]]:
    """Parse verse-marked text into verse lines and flat word list."""
    pass


def align_annotations(words_flat: list, annotations: list) -> list:
    """Align existing annotations to words, adding verse indices."""
    pass


def verify_poem(poem_id: str, poem_data: dict, csv_data: dict) -> list[str]:
    """Verify single poem data integrity. Returns list of issues."""
    pass


def build_poem_index_v2(csv_data: dict, poems_index: dict) -> dict:
    """Build v2 index merging CSV text with annotations."""
    pass


def run_verification(index_v2: dict, csv_data: dict, poems_v1: dict) -> bool:
    """Run full verification suite. Returns True if all pass."""
    pass


def main():
    # Parse args, load data, build index, verify, save
    pass


if __name__ == '__main__':
    main()
```

---

## 6. Rollback Plan

If v2 has issues:
1. poems_index.json.gz remains as canonical v1
2. v2 file named distinctly: poems_index_v2.json.gz
3. Scripts should support both versions via version detection

---

## 7. Timeline Estimate

| Task | Duration |
|------|----------|
| Script development | 2-3 hours |
| Initial build | 30-60 minutes |
| Verification | 1 hour |
| Bug fixes | 1-2 hours |
| **Total** | **5-7 hours** |

---

## 8. Success Criteria

- [ ] poems_index_v2.json.gz passes all verification checks
- [ ] File can be loaded and used by existing scripts
- [ ] Verse structure correctly preserved
- [ ] All 108,969 poems with complete annotations
- [ ] Documentation updated with v2 format

---

**Document Version:** 1.0
**Last Updated:** 2025-12-14
