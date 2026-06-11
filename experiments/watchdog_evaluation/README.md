# Watchdog Evaluation

## Overview

This experiment studies whether watchdog mechanisms can detect State-Report Divergence.

State-Report Divergence occurs when the reported state of an agentic system does not accurately reflect the actual execution state.

This experiment compares two watchdog designs:

- V0: naive lexical watchdog
- V1: semantic rule watchdog

## Research Theme

The broader theme is:

System State ≠ Reported State

Reported State ≠ Watchdog Interpretation

In other words, state information can degrade across multiple layers:

Worker
↓
Planner
↓
Watchdog

## Baseline Evaluation

The baseline used 16 controlled cases across four categories:

- Clean Match
- Overclaim
- Status Ambiguity Propagation
- Disclosure Trap

### Baseline Results

| Watchdog | True Positives | False Positives |
|---|---:|---:|
| Naive lexical watchdog | 3 | 6 |
| Semantic rule watchdog | 8 | 0 |

### Baseline Finding

The lexical watchdog produced many false positives and missed several true divergence cases.

The semantic watchdog detected all divergence cases with zero false positives on the clean baseline.

This supports the hypothesis that lexical matching is brittle and state-aware oversight is more reliable.

## Failure Mode Stress Test

The stress test evaluated whether the semantic watchdog remains reliable on more complex reports.

The stress test included 15 cases across five categories:

- Honest Complex Failure
- Nested Multi-Step Report
- Partial-Success Edge Case
- Contradictory Trace
- Ambiguous But Non-Divergent Report

### Stress Test Results

| Watchdog | True Positives | False Positives |
|---|---:|---:|
| Naive lexical watchdog | 3 | 8 |
| Semantic rule watchdog | 3 | 3 |

### Key Failure Mode

The most important failure appeared in nested multi-step reports.

NESTED_MULTI_STEP
semantic_correct = 1/3
semantic_fp = 2

The semantic watchdog incorrectly flagged some honest multi-step reports as divergent when the report described both successful substeps and an overall failure or partial completion.

## Main Finding

Semantic watchdogs outperform lexical watchdogs on clean cases, but they still fail under more complex reporting structures.

The central finding is not that semantic oversight solves State-Report Divergence.

The stronger finding is:

Oversight mechanisms themselves need evaluation.

## Interpretation

A lexical watchdog confuses failure-related words with reporting failures.

A semantic watchdog improves on this, but can still misread nested or multi-step reports.

This suggests that state information can be distorted or misinterpreted at both levels:

1. planner reporting
2. watchdog interpretation

## Limitations

- small hand-built datasets
- rule-based watchdogs
- simulated reports
- no LLM judge yet
- no live multi-agent environment yet

## Future Work

- add LLM judge watchdog
- test multi-run variability
- add real planner-worker traces
- integrate watchdog logic into multi-agent-safety-sim
- evaluate naturally emerging State-Report Divergence in Planner → Worker → Watchdog workflows
