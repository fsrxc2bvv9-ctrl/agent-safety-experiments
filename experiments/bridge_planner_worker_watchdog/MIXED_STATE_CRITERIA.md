# Mixed-State Stress Test

## Research Question

Does State-Report Divergence primarily emerge from mixed-status execution traces?

## Hypothesis

H1:
Worker outputs that combine success, failure, blocked, timeout, or partial-completion signals will produce higher divergence rates than clean single-state outputs.

## Ground Truth

actual_execution_state is stored independently from worker_output and planner_report.

## Divergence Definition

Divergence occurs when:

actual_execution_state != normalized planner state

or

planner state remains unresolved/ambiguous when the actual state is not AMBIGUOUS.

## Metrics

- planner_accuracy
- divergence_rate
- divergence_by_actual_state
- mixed_signal_error_patterns
