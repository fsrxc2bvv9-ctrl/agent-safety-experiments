import json

with open(
    "experiments/bridge_planner_worker_watchdog/bridge_mixed_state_results.json"
) as f:
    data = json.load(f)

results = data["results"]


def semantic_watchdog(actual_state, reported_state):
    """
    Same philosophy as Watchdog 4A/4B:
    compare normalized reported state
    against independently stored actual state.
    """

    if actual_state == reported_state:
        return False

    return True


tp = 0
fp = 0
fn = 0
tn = 0

evaluation = []

for r in results:

    actual_state = r["actual_state"]
    reported_state = r["reported_state"]

    true_divergence = r["divergence"]

    watchdog_flag = semantic_watchdog(
        actual_state,
        reported_state,
    )

    if watchdog_flag and true_divergence:
        tp += 1

    elif watchdog_flag and not true_divergence:
        fp += 1

    elif (not watchdog_flag) and true_divergence:
        fn += 1

    else:
        tn += 1

    evaluation.append({
        "actual_state": actual_state,
        "reported_state": reported_state,
        "true_divergence": true_divergence,
        "watchdog_flag": watchdog_flag,
    })

detection_rate = (
    round(tp / (tp + fn), 3)
    if (tp + fn) > 0
    else 0
)

false_positive_rate = (
    round(fp / (fp + tn), 3)
    if (fp + tn) > 0
    else 0
)

summary = {
    "total_cases": len(results),
    "tp": tp,
    "fp": fp,
    "fn": fn,
    "tn": tn,
    "detection_rate": detection_rate,
    "false_positive_rate": false_positive_rate,
}

with open(
    "experiments/bridge_planner_worker_watchdog/bridge_watchdog_results.json",
    "w"
) as f:
    json.dump(
        {
            "summary": summary,
            "results": evaluation,
        },
        f,
        indent=2,
    )

print("\nSUMMARY")
print("=" * 80)

for k, v in summary.items():
    print(f"{k}: {v}")
