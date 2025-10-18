#!/bin/bash
# Interactive SQL Query Runner for Estonian Runosong Corpus
#
# Usage:
#   ./run_queries.sh              # Run all queries interactively
#   ./run_queries.sh --all         # Run all queries without pausing
#   ./run_queries.sh 1 5 9        # Run specific query numbers
#   ./run_queries.sh --list       # List all available queries

DB_FILE="../corpus_runosongs_v2_FIXED.db"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if database exists
if [ ! -f "$SCRIPT_DIR/$DB_FILE" ]; then
    echo "❌ Database file not found: $DB_FILE"
    echo "   Expected location: $SCRIPT_DIR/$DB_FILE"
    exit 1
fi

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run a query with formatting
run_query() {
    local query_num=$1
    local title=$2
    local sql=$3

    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${BLUE}Query #$query_num: $title${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""

    # Run query with SQLite formatting
    sqlite3 "$SCRIPT_DIR/$DB_FILE" <<EOF
.mode column
.headers on
.width 25 8 8 8
$sql
EOF

    echo ""
}

# Function to pause between queries
pause_if_interactive() {
    if [ "$INTERACTIVE" = true ]; then
        echo -e "${YELLOW}Press Enter to continue to next query (or Ctrl+C to exit)...${NC}"
        read
    fi
}

# Function to list all queries
list_queries() {
    echo -e "${GREEN}Available Queries:${NC}"
    echo ""
    echo " 1. Find all word forms for lemma 'piir'"
    echo " 2. Get statistics for word 'piiri'"
    echo " 3. List all processing methods"
    echo " 4. Find high-frequency ambiguous words"
    echo " 5. Find words with most competing lemmas"
    echo " 6. Count ambiguous words by competing lemmas"
    echo " 7. Find low-confidence, high-frequency words"
    echo " 8. Find high-confidence words"
    echo " 9. Find lemmas with most word form variants"
    echo "10. Find most frequent lemmas"
    echo "11. Find invariable words (one form only)"
    echo "12. Get overall word quality statistics"
    echo "13. Find low-confidence words needing validation"
    echo "14. Find hapax legomena (words appearing once)"
    echo "15. Get frequency distribution by ranges"
    echo "16. Find most common words"
    echo "17. Find potential annotation errors"
    echo "18. Check for duplicate lemma-wordform pairs"
    echo "19. Find orphaned entries"
    echo "20. Export sample dataset for validation"
    echo ""
}

# Parse command line arguments
INTERACTIVE=true
QUERIES_TO_RUN=()

if [ $# -eq 0 ]; then
    # No arguments - run all queries interactively
    QUERIES_TO_RUN=($(seq 1 20))
elif [ "$1" = "--list" ]; then
    list_queries
    exit 0
elif [ "$1" = "--all" ]; then
    # Run all queries without pausing
    INTERACTIVE=false
    QUERIES_TO_RUN=($(seq 1 20))
else
    # Run specific queries
    QUERIES_TO_RUN=("$@")
    INTERACTIVE=false
fi

# Define all queries
declare -A QUERY_TITLES
declare -A QUERY_SQL

QUERY_TITLES[1]="Find all word forms for lemma 'piir'"
QUERY_SQL[1]="SELECT word_form, count, avg_confidence
FROM lemma_variants
WHERE lemma = 'piir'
ORDER BY count DESC
LIMIT 20;"

QUERY_TITLES[2]="Get statistics for word 'piiri' with lemmas"
QUERY_SQL[2]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.word_form = 'piiri'
ORDER BY lv.count DESC;"

QUERY_TITLES[3]="List all processing methods"
QUERY_SQL[3]="SELECT method, total_uses, avg_confidence
FROM method_stats
ORDER BY total_uses DESC;"

QUERY_TITLES[4]="Find high-frequency ambiguous words needing review"
QUERY_SQL[4]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence,
    a.num_competing_lemmas
FROM lemma_variants lv
JOIN ambiguous_words a ON lv.word_form = a.word
WHERE a.needs_review = 1 AND lv.count > 100
ORDER BY a.num_competing_lemmas DESC, lv.count DESC
LIMIT 20;"

QUERY_TITLES[5]="Find words with most competing lemma interpretations"
QUERY_SQL[5]="SELECT
    lv.word_form || ' → ' || GROUP_CONCAT(lv.lemma, ', ') as word_lemmas,
    a.num_competing_lemmas
FROM ambiguous_words a
JOIN lemma_variants lv ON a.word = lv.word_form
WHERE a.needs_review = 1
GROUP BY a.word, a.num_competing_lemmas
ORDER BY a.num_competing_lemmas DESC
LIMIT 20;"

QUERY_TITLES[6]="Count ambiguous words by competing lemmas"
QUERY_SQL[6]="SELECT num_competing_lemmas, COUNT(*) as word_count
FROM ambiguous_words
GROUP BY num_competing_lemmas
ORDER BY num_competing_lemmas DESC
LIMIT 20;"

QUERY_TITLES[7]="Find low-confidence, high-frequency word→lemma pairs"
QUERY_SQL[7]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.avg_confidence < 0.5 AND lv.count > 50
ORDER BY lv.count DESC
LIMIT 20;"

QUERY_TITLES[8]="Find high-confidence word→lemma pairs"
QUERY_SQL[8]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.avg_confidence > 0.95
ORDER BY lv.count DESC
LIMIT 20;"

QUERY_TITLES[9]="Find lemmas with most word form variants"
QUERY_SQL[9]="SELECT lemma, COUNT(DISTINCT word_form) as variant_count, SUM(count) as total_occurrences
FROM lemma_variants
GROUP BY lemma
ORDER BY variant_count DESC
LIMIT 20;"

QUERY_TITLES[10]="Find most frequent lemmas in corpus"
QUERY_SQL[10]="SELECT lemma, SUM(count) as total_count
FROM lemma_variants
GROUP BY lemma
ORDER BY total_count DESC
LIMIT 20;"

QUERY_TITLES[11]="Find invariable words (one form only)"
QUERY_SQL[11]="SELECT lemma, word_form, count
FROM lemma_variants
WHERE lemma IN (
    SELECT lemma
    FROM lemma_variants
    GROUP BY lemma
    HAVING COUNT(DISTINCT word_form) = 1
)
ORDER BY count DESC
LIMIT 20;"

QUERY_TITLES[12]="Get overall word quality statistics"
QUERY_SQL[12]="SELECT
       COUNT(*) as total_words,
       AVG(avg_confidence) as avg_conf,
       MIN(avg_confidence) as min_conf,
       MAX(avg_confidence) as max_conf
FROM words;"

QUERY_TITLES[13]="Find low-confidence word→lemma pairs needing validation"
QUERY_SQL[13]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.avg_confidence < 0.5 AND lv.count > 20
ORDER BY lv.count DESC
LIMIT 20;"

QUERY_TITLES[14]="Find hapax legomena word→lemma pairs"
QUERY_SQL[14]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.count = 1
ORDER BY lv.avg_confidence DESC
LIMIT 20;"

QUERY_TITLES[15]="Get frequency distribution by ranges"
QUERY_SQL[15]="SELECT
    CASE
        WHEN total_count = 1 THEN '1 (hapax)'
        WHEN total_count BETWEEN 2 AND 5 THEN '2-5'
        WHEN total_count BETWEEN 6 AND 10 THEN '6-10'
        WHEN total_count BETWEEN 11 AND 50 THEN '11-50'
        WHEN total_count BETWEEN 51 AND 100 THEN '51-100'
        ELSE '100+'
    END as frequency_range,
    COUNT(*) as word_count
FROM words
GROUP BY frequency_range
ORDER BY MIN(total_count);"

QUERY_TITLES[16]="Find most common word→lemma pairs in corpus"
QUERY_SQL[16]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
ORDER BY lv.count DESC
LIMIT 20;"

QUERY_TITLES[17]="Find potential annotation errors (word→lemma)"
QUERY_SQL[17]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count,
    lv.avg_confidence
FROM lemma_variants lv
WHERE lv.count > 100 AND lv.avg_confidence < 0.6
ORDER BY lv.count DESC
LIMIT 20;"

QUERY_TITLES[18]="Check for duplicate lemma-wordform pairs"
QUERY_SQL[18]="SELECT lemma, word_form, COUNT(*) as duplicate_count
FROM lemma_variants
GROUP BY lemma, word_form
HAVING COUNT(*) > 1;"

QUERY_TITLES[19]="Find orphaned entries (words without lemmas)"
QUERY_SQL[19]="SELECT
    w.word,
    w.total_count,
    w.lemmas as lemmas_text
FROM words w
LEFT JOIN lemma_variants lv ON w.word = lv.word_form
WHERE lv.word_form IS NULL
LIMIT 20;"

QUERY_TITLES[20]="Export sample word→lemma dataset for validation"
QUERY_SQL[20]="SELECT
    lv.word_form || ' → ' || lv.lemma as word_lemma,
    lv.count as frequency,
    lv.avg_confidence as confidence,
    a.num_competing_lemmas as alternatives
FROM lemma_variants lv
JOIN ambiguous_words a ON lv.word_form = a.word
WHERE a.needs_review = 1
  AND lv.count BETWEEN 50 AND 500
ORDER BY RANDOM()
LIMIT 20;"

# Print header
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Estonian Runosong Corpus - SQL Query Runner${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"

# Run queries
for query_num in "${QUERIES_TO_RUN[@]}"; do
    if [ -n "${QUERY_TITLES[$query_num]}" ]; then
        run_query "$query_num" "${QUERY_TITLES[$query_num]}" "${QUERY_SQL[$query_num]}"
        pause_if_interactive
    else
        echo "❌ Query #$query_num not found"
    fi
done

echo ""
echo -e "${GREEN}✅ Query execution complete!${NC}"
echo ""
