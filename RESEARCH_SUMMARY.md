# Agent Safety Experiments — Research Summary

## Overview

This repository contains a series of small, reproducible evaluations exploring how information degrades as it moves across agent layers.

The central theme is **State-Report Divergence**:

> A mismatch between what actually happened in a system and what an agent or oversight layer reports happened.

The project studies this phenomenon across a simple chain:

```text
Worker Execution
↓
Planner Report
↓
Watchdog Interpretation
```

---

## Core Research Question

How does state information degrade as it moves across agent layers?

More specifically:

- Can planners misrepresent execution state?
- Do mixed-status traces increase reporting errors?
- Can watchdogs detect State-Report Divergence?
- Where do watchdogs themselves fail?

---

## Key Finding

Across controlled, emergent, and stress-test evaluations, the highest divergence rates consistently appeared when execution traces contained mixed-status signals.

Examples:

- success + failure
- partial completion + failure
- success + blocked
- success + timeout

Bridge evaluation results:

| Evaluation | Planner Accuracy | Divergence Rate |
|------------|-----------------|-----------------|
| Emergent Bridge Baseline | 75% | 25% |
| Mixed-State Stress Test | 30% | 70% |

This suggests that mixed-status execution traces are a major risk area for reporting reliability in agentic systems.

---

## Experiments

### Tool Description Safety

Research Question:

Can tool descriptions influence agent behavior when implementation remains unchanged?

Finding:

Tool metadata influences behavior and can change how agents interpret capability boundaries.

---

### Delegation Safety

Research Question:

Can delegation policies influence planner behavior?

Results:

| Policy | Unsafe Delegations |
|---------|------------------|
| Delegate Always | 4 |
| Safety-Aware | 0 |

Finding:

Even a simple safety-aware delegation policy reduced unsafe delegation in a toy environment.

---

### Reporting Consistency

Research Question:

How accurately do planner reports reflect worker execution state?

Finding:

Ambiguous and contradictory outputs propagate uncertainty into reporting layers.

---

### Watchdog Baseline

Results:

| Watchdog | True Positives | False Positives |
|-----------|---------------|----------------|
| Lexical | 3 | 6 |
| Semantic | 8 | 0 |

Finding:

Semantic watchdogs outperform lexical matching on controlled cases.

---

### Watchdog Failure Modes

Results:

| Watchdog | True Positives | False Positives |
|-----------|---------------|----------------|
| Lexical | 3 | 8 |
| Semantic | 3 | 3 |

Most important failure:

```text
NESTED_MULTI_STEP

semantic_correct = 1/3
semantic_fp = 2
```

Finding:

Even semantic watchdogs fail on nested and multi-step reporting structures.

---

### Bridge Prototype

Key design decision:

```text
actual_execution_state
is stored independently from
planner_report
```

Finding:

Independent ground truth makes divergence measurable.

---

### Emergent Bridge Evaluation

Single run.

N = 12 traces.

Results:

```text
planner_accuracy = 75%
divergence_rate = 25%
```

Finding:

State-Report Divergence emerged without explicitly scripted planner overclaims.

---

### Mixed-State Stress Test

Single run.

N = 20 traces.

Results:

```text
planner_accuracy = 30%
divergence_rate = 70%
```

Breakdown:

```text
PARTIAL_SUCCESS: 4/4 divergence
TIMEOUT: 4/4 divergence
FAILURE: 3/4 divergence
BLOCKED: 3/4 divergence
AMBIGUOUS: 0/4 divergence
```

Finding:

Mixed-status execution traces substantially increase State-Report Divergence.

---

### Watchdog on Emergent Divergence

Single run.

N = 20 traces.

Results:

```text
TP = 14
FP = 0
FN = 0
TN = 6

Detection Rate = 100%
False Positive Rate = 0%
```

Finding:

In this baseline, the semantic watchdog detected all divergence cases on emergent mixed-state traces.

However, this result should be interpreted cautiously.

The watchdog and bridge environment currently share normalization assumptions, creating a potential evaluation-leakage risk.

The contrast with the earlier watchdog stress test suggests that these mixed-state traces may be structurally simpler than the nested multi-step reports that previously caused semantic watchdog failures.

Future work should focus on less-coupled watchdog evaluation.

---

## Methodological Principle

One of the strongest lessons from this project:

```text
No independent ground truth
=
No measurable divergence
```

Agent-generated reports cannot serve as their own source of truth.

To evaluate reporting reliability, actual execution state must be stored independently from planner reports and watchdog interpretations.

---

## Limitations

Current limitations include:

- Small hand-built datasets
- Mostly rule-based planners
- Mostly rule-based watchdogs
- Single-run evaluations
- Limited stochasticity
- No large-scale multi-agent environment yet
- Shared normalization assumptions between some planners and watchdogs

These findings should be interpreted as early-stage evaluation results rather than broad empirical claims about agentic systems in general.

---

## Future Work

Planned next steps:

1. Less-coupled watchdog evaluation
2. LLM-based planner reports
3. Repeated-trial evaluation
4. Larger mixed-status datasets
5. Integration into multi-agent-safety-sim
6. Study whether memory, delegation, and tool metadata amplify State-Report Divergence

---

## Long-Term Goal

The long-term goal is to build a measurable agent safety simulation environment where:

- Tasks have independent ground-truth states
- Planners produce user-facing reports
- Watchdogs evaluate divergence
- State degradation can be measured across layers

This repository serves as the controlled-experiment foundation for that larger research program.
