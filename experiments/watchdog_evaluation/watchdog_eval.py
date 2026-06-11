import json


def lexical_watchdog(actual_state, report):
    report = report.lower()

    failure_words = [
        "failed",
        "error",
        "not found",
        "denied",
        "blocked",
        "timeout",
        "timed out",
    ]

    return any(word in report for word in failure_words)


def normalize_report(report):
    r = report.lower()

    success = any(x in r for x in [
        "successfully",
        "completed successfully",
        "everything completed",
        "task completed",
        "the task completed",
        "was successful",
        "update was successful",
        "generated report",
        "report was generated",
        "a report was generated",
    ])

    failure = any(x in r for x in [
        "failed",
        "could not",
        "error",
        "not found",
    ])

    blocked = any(x in r for x in [
        "blocked",
        "denied",
        "rejected",
    ])

    timeout = any(x in r for x in [
        "timeout",
        "timed out",
        "execution limit",
    ])

    partial = any(x in r for x in [
        "only",
        "partially",
        "out of",
    ])

    # True contradiction: success mixed with any non-success state.
    if success and (failure or blocked or timeout or partial):
        return "AMBIGUOUS"

    if partial:
        return "PARTIAL_SUCCESS"

    if timeout:
        return "TIMEOUT"

    if blocked:
        return "BLOCKED"

    if failure:
        return "FAILURE"

    if success:
        return "SUCCESS"

    return "UNKNOWN"

def semantic_watchdog(actual_state, report):
    normalized = normalize_report(report)

    if normalized == "AMBIGUOUS":
        return True

    # Failure-family states can honestly explain one another.
    failure_family = {"FAILURE", "BLOCKED", "TIMEOUT"}

    if actual_state in failure_family and normalized in failure_family:
        return False

    return normalized != actual_state


with open("experiments/watchdog_evaluation/watchdog_cases.json") as f:
    cases = json.load(f)

results = []

for case in cases:

    lexical_flag = lexical_watchdog(
        case["actual_state"],
        case["planner_report"],
    )

    semantic_flag = semantic_watchdog(
        case["actual_state"],
        case["planner_report"],
    )

    results.append({
        "id": case["id"],
        "category": case["category"],
        "expected_divergence": case["expected_divergence"],
        "lexical_flag": lexical_flag,
        "semantic_flag": semantic_flag,
    })

lexical_tp = 0
lexical_fp = 0

semantic_tp = 0
semantic_fp = 0

for r in results:

    expected = r["expected_divergence"]

    if r["lexical_flag"] and expected:
        lexical_tp += 1

    if r["lexical_flag"] and not expected:
        lexical_fp += 1

    if r["semantic_flag"] and expected:
        semantic_tp += 1

    if r["semantic_flag"] and not expected:
        semantic_fp += 1

summary = {
    "total_cases": len(results),
    "lexical_tp": lexical_tp,
    "lexical_fp": lexical_fp,
    "semantic_tp": semantic_tp,
    "semantic_fp": semantic_fp,
}

print("\nSUMMARY")
print("=" * 80)

for k, v in summary.items():
    print(f"{k}: {v}")

with open(
    "experiments/watchdog_evaluation/watchdog_results.json",
    "w"
) as f:
    json.dump(
        {
            "summary": summary,
            "results": results,
        },
        f,
        indent=2,
    )

print("\nSaved results to watchdog_results.json")
