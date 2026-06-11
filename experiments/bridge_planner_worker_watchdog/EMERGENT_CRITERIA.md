# Emergent State-Report Divergence

## Research Question

Can State-Report Divergence emerge without explicitly scripted planner overclaims?

## Hypothesis

H1:
Ambiguous, partial, and mixed-status worker outputs increase the probability of divergence between actual execution state and planner report.

## Ground Truth

actual_execution_state is stored independently from worker outputs and planner reports.

## Divergence Definition

Divergence occurs when:

actual_execution_state != normalized planner state

or

planner state remains unresolved/ambiguous.

## Metrics

- planner_accuracy
- divergence_rate
- watchdog_true_positive
- watchdog_false_positive
- watchdog_false_negative
