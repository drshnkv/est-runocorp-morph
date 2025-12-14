# poems_index_v2 - Split Archive

This folder contains `poems_index_v2.json.gz` split into parts for GitHub compatibility (100 MB file size limit).

## Quick Assembly

### Unix/macOS (Recommended)
```bash
./assemble.sh
```

### Windows/Cross-platform (Python)
```bash
python assemble.py
```

### Manual (Any Unix/macOS)
```bash
cat poems_index_v2.json.gz.* > ../poems_index_v2.json.gz
gzip -t ../poems_index_v2.json.gz  # Verify integrity
```

## File Parts

| Part | Size | Bytes |
|------|------|-------|
| `poems_index_v2.json.gz.aa` | 50.0 MB | 52,428,800 |
| `poems_index_v2.json.gz.ab` | 50.0 MB | 52,428,800 |
| `poems_index_v2.json.gz.ac` | 34.6 MB | 36,325,312 |
| **Total** | **134.6 MB** | **141,182,912** |

## Verification

### Automatic (via scripts)
Both `assemble.sh` and `assemble.py` automatically verify:
1. gzip integrity (file is valid gzip)
2. MD5 checksum (matches original file)

### Manual
```bash
# Verify gzip integrity
gzip -t ../poems_index_v2.json.gz

# Verify MD5 checksum
md5 ../poems_index_v2.json.gz
# Should output: fdc32d9aed1097717f86fd69fa77fccd
```

## What is poems_index_v2?

Version 2 of the poems index adds verse line structure and enhanced metadata to the morphologically annotated Estonian runosong corpus.

### Key Features
- **verse_lines**: Array of verse strings (split by `/` markers)
- **verse_index**: Per-word position indicating which verse the word belongs to
- **word_in_verse**: Word position within its verse
- **text**: Original text with `/` verse markers preserved
- **metadata**: Places, collectors, types, year, collection

### Statistics
| Metric | Value |
|--------|-------|
| Total poems | 108,969 |
| Total words | 7,344,574 |
| Total verses | 2,005,147 |
| Empty poems | 844 |

### Example Structure
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
      },
      ...
    ],
    "is_empty": false,
    "metadata": {
      "title": "AES, MT 3, 1 (1)",
      "collection": "erab",
      "places": ["Viru-Jaagupi", "Viru-Nigula"],
      ...
    }
  }
}
```

---

**Created:** 2025-12-14
**MD5:** fdc32d9aed1097717f86fd69fa77fccd
