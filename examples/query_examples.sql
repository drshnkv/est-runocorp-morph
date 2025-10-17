-- Estonian Runosong Morphological Corpus - SQL Query Examples
-- Database: corpus_runosongs_v2_FIXED.db

-- ============================================================
-- BASIC QUERIES
-- ============================================================

-- 1. Find all word forms for a specific lemma
SELECT word_form, count, avg_confidence
FROM lemma_variants
WHERE lemma = 'piir'
ORDER BY count DESC;

-- 2. Get statistics for a specific word
SELECT *
FROM words
WHERE word = 'piiri';

-- 3. List all processing methods with their performance
SELECT method, word_count, percentage, avg_confidence
FROM method_stats
ORDER BY word_count DESC;

-- ============================================================
-- AMBIGUOUS WORDS ANALYSIS
-- ============================================================

-- 4. Find high-frequency words needing expert review
SELECT w.word, w.total_count, w.avg_confidence, a.num_competing_lemmas
FROM words w
JOIN ambiguous_words a ON w.word = a.word
WHERE a.needs_review = 1 AND w.total_count > 100
ORDER BY a.num_competing_lemmas DESC, w.total_count DESC
LIMIT 50;

-- 5. Find words with the most competing lemma interpretations
SELECT word, num_competing_lemmas
FROM ambiguous_words
WHERE needs_review = 1
ORDER BY num_competing_lemmas DESC
LIMIT 20;

-- 6. Count ambiguous words by number of competing lemmas
SELECT num_competing_lemmas, COUNT(*) as word_count
FROM ambiguous_words
GROUP BY num_competing_lemmas
ORDER BY num_competing_lemmas DESC;

-- ============================================================
-- QUALITY ANALYSIS
-- ============================================================

-- 7. Find low-confidence, high-frequency words (potential issues)
SELECT word, total_count, avg_confidence, primary_method
FROM words
WHERE avg_confidence < 0.5 AND total_count > 50
ORDER BY total_count DESC
LIMIT 100;

-- 8. Find high-confidence words processed by specific method
SELECT word, total_count, avg_confidence
FROM words
WHERE primary_method = 'estnltk+dict' AND avg_confidence > 0.95
ORDER BY total_count DESC
LIMIT 50;

-- ============================================================
-- LEMMA ANALYSIS
-- ============================================================

-- 9. Find lemmas with the most word form variants
SELECT lemma, COUNT(DISTINCT word_form) as variant_count, SUM(count) as total_occurrences
FROM lemma_variants
GROUP BY lemma
ORDER BY variant_count DESC
LIMIT 50;

-- 10. Find most frequent lemmas in the corpus
SELECT lemma, SUM(count) as total_count
FROM lemma_variants
GROUP BY lemma
ORDER BY total_count DESC
LIMIT 100;

-- 11. Find lemmas that appear in only one word form (invariable words)
SELECT lemma, word_form, count
FROM lemma_variants
WHERE lemma IN (
    SELECT lemma
    FROM lemma_variants
    GROUP BY lemma
    HAVING COUNT(DISTINCT word_form) = 1
)
ORDER BY count DESC
LIMIT 50;

-- ============================================================
-- METHOD COMPARISON
-- ============================================================

-- 12. Compare average confidence across different processing methods
SELECT primary_method,
       COUNT(*) as word_count,
       AVG(avg_confidence) as avg_conf,
       MIN(avg_confidence) as min_conf,
       MAX(avg_confidence) as max_conf
FROM words
GROUP BY primary_method
ORDER BY avg_conf DESC;

-- 13. Find words where multiple methods might apply (for validation)
SELECT w.word, w.total_count, w.avg_confidence, w.primary_method
FROM words w
WHERE w.primary_method IN ('levenshtein', 'compound', 'suffix_strip')
  AND w.total_count > 20
ORDER BY w.total_count DESC
LIMIT 100;

-- ============================================================
-- FREQUENCY ANALYSIS
-- ============================================================

-- 14. Find hapax legomena (words appearing only once)
SELECT word, primary_method, avg_confidence
FROM words
WHERE total_count = 1
ORDER BY avg_confidence DESC
LIMIT 100;

-- 15. Get frequency distribution (by count ranges)
SELECT
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
ORDER BY MIN(total_count);

-- 16. Find most common words in corpus
SELECT word, total_count, avg_confidence, primary_method
FROM words
ORDER BY total_count DESC
LIMIT 100;

-- ============================================================
-- VALIDATION QUERIES
-- ============================================================

-- 17. Find potential annotation errors (high frequency + low confidence)
SELECT word, total_count, avg_confidence, primary_method
FROM words
WHERE total_count > 100 AND avg_confidence < 0.6
ORDER BY total_count DESC;

-- 18. Check for duplicate lemma-wordform pairs (data integrity)
SELECT lemma, word_form, COUNT(*) as duplicate_count
FROM lemma_variants
GROUP BY lemma, word_form
HAVING COUNT(*) > 1;

-- 19. Find words without lemma variants (orphaned entries)
SELECT w.word, w.total_count
FROM words w
LEFT JOIN lemma_variants lv ON w.word = lv.word_form
WHERE lv.word_form IS NULL
LIMIT 100;

-- ============================================================
-- EXPORT QUERIES FOR RESEARCH
-- ============================================================

-- 20. Export sample dataset for manual validation
-- (High-frequency ambiguous words)
SELECT
    w.word,
    w.total_count as frequency,
    w.avg_confidence as confidence,
    a.num_competing_lemmas as alternatives,
    w.primary_method as method
FROM words w
JOIN ambiguous_words a ON w.word = a.word
WHERE a.needs_review = 1
  AND w.total_count BETWEEN 50 AND 500
ORDER BY RANDOM()
LIMIT 200;
