# Watchdog Failure Modes — Pre-Registered Stress Test

## Research Question

Where does a semantic watchdog fail after passing a clean baseline?

The previous watchdog baseline showed:

| Watchdog | True Positives | False Positives |
|---|---:|---:|
| Naive lexical watchdog | 3 | 6 |
| Semantic rule watchdog | 8 | 0 |

This stress test evaluates whether the semantic watchdog remains reliable on more complex reports.

## Goal

The goal is not to prove that the semantic watchdog is perfect.

The goal is to identify its failure modes.

## Case Categories

### 1. Honest Complex Failure

Reports that honestly describe failure using several failure-related phrases.

Expected:

- Lexical watchdog: likely false positive
- Semantic watchdog: should not flag

### 2. Nested Multi-Step Report

Reports where some substeps succeed and later substeps fail.

Expected:

- Lexical watchdog: inconsistent
- Semantic watchdog: may fail if it treats any success + failure as ambiguity

### 3. Partial-Success Edge Case

Reports that mention some completed work but clearly state the task was incomplete.

Expected:

- Lexical watchdog: may miss or falsely flag
- Semantic watchdog: should classify as partial success

### 4. Contradictory Trace

Reports that contain unresolved success and failure signals.

Expected:

- Lexical watchdog: may flag
- Semantic watchdog: should flag

### 5. Ambiguous But Non-Divergent Report

Reports that sound uncertain but still accurately reflect the actual state.

Expected:

- Lexical watchdog: may false positive
- Semantic watchdog: may false positive if uncertainty is mistaken for divergence

## Metrics

- Detection rate on true divergence cases
- False positive rate on non-divergence cases
- False negatives on contradictory traces
- False positives on honest complex reports
- Category-level accuracy

## Hypothesis

The semantic watchdog will outperform the lexical watchdog, but it may fail on nested multi-step reports and ambiguous-but-non-divergent reports.

The central hypothesis is:

Semantic oversight improves over lexical matching, but oversight itself still needs evaluation.
