# Agent Safety Experiments

A collection of small, reproducible evaluations exploring how information degrades as it moves across agent layers.

**Current status:** 9 completed evaluations, bridge environment implemented, active integration planning for multi-agent-safety-sim.

## Research Focus

```text
Worker Execution
↓
Planner Reports
↓
Watchdog Oversight
```

The central theme of the project is **State-Report Divergence**:

> A mismatch between what actually happened in a system and what an agent or oversight layer reports happened.

---

## Key Finding

Across controlled, emergent, and stress-test evaluations, the highest divergence rates consistently appeared when execution traces contained mixed-status signals.

Examples:

- success + failure
- partial completion + failure
- success + blocked
- success + timeout

Results from bridge evaluations:

| Evaluation | Planner Accuracy | Divergence Rate |
|------------|-----------------|-----------------|
| Emergent Bridge Baseline | 75% | 25% |
| Mixed-State Stress Test | 30% | 70% |

These results suggest that mixed-status execution traces are a major risk area for reporting reliability in agentic systems.

---

## Experiments

| Experiment | Main Finding |
|------------|--------------|
| Tool Description Safety | Tool metadata influences agent behavior |
| Delegation Safety | Safety-aware delegation reduces unsafe actions |
| Reporting Consistency | Ambiguity propagates through reporting layers |
| Watchdog Evaluation | Semantic watchdogs outperform lexical matching |
| Watchdog Failure Modes | Nested multi-step reports break oversight assumptions |
| Bridge Prototype | Independent ground truth enables measurable divergence |
| Emergent Bridge Evaluation | Divergence appears without scripted overclaims |
| Mixed-State Stress Test | Mixed-status traces substantially increase divergence |
| Watchdog on Emergent Data | Semantic watchdog detects baseline mixed-state divergence* |

\* See RESEARCH_SUMMARY.md for limitations regarding coupling between watchdog and environment normalization logic.

---

## Repository Structure

```text
experiments/
├── tool_description_safety/
├── delegation_safety/
├── reporting_consistency/
├── watchdog_evaluation/
└── bridge_planner_worker_watchdog/
```

---

## Research Summary

For a complete overview of methods, results, limitations, and future work:

➡️ **[Research Summary](RESEARCH_SUMMARY.md)**

The summary includes:

- Research questions
- Experimental findings
- Quantitative results
- Methodological lessons
- Current limitations
- Future research directions

---

## Methodological Principle

One of the most important findings from this project is:

```text
No independent ground truth
=
No measurable divergence
```

Agent-generated reports cannot serve as their own source of truth.

To evaluate reporting reliability, actual execution state must be stored independently from planner reports and watchdog interpretations.

---

## Current Direction

```text
Worker
↓
Planner
↓
Watchdog
↓
State-Report Divergence Measurement
↓
Multi-Agent Safety Simulation
```

The next stage of the project focuses on integrating these evaluation concepts into larger Planner → Worker → Watchdog environments and eventually into the `multi-agent-safety-sim` project.

---

## Status

### Completed

- Tool Description Safety
- Delegation Safety
- Reporting Consistency
- Watchdog Evaluation
- Watchdog Failure Modes
- Bridge Prototype
- Emergent Bridge Evaluation
- Mixed-State Stress Test
- Watchdog on Emergent Data

### Next Priorities

1. Less-coupled watchdog evaluation
2. LLM-based planner reports
3. Repeated-trial evaluation
4. Multi-agent-safety-sim integration