import json
from collections import defaultdict


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
        "incomplete",
        "not completed",
        "not processed",
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
        "processed successfully",
        "completed the first part",
    ])

    failure = any(x in r for x in [
        "failed",
        "could not",
        "error",
        "not found",
        "not completed",
        "did not complete",
        "incomplete",
        "missing",
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
        "some documents",
        "not all",
        "remaining files were not processed",
        "part of the task",
        "first part",
    ])

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

    failure_family = {"FAILURE", "BLOCKED", "TIMEOUT"}

    if actual_state in failure_family and normalized in failure_family:
        return False

    return normalized != actual_state


def evaluate(rows):
    results = []

    for case in rows:
        expected = case["expected_divergence"]

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
            "actual_state": case["actual_state"],
            "planner_report": case["planner_report"],
            "expected_divergence": expected,
            "lexical_flag": lexical_flag,
            "semantic_flag": semantic_flag,
            "lexical_correct": lexical_flag == expected,
            "semantic_correct": semantic_flag == expected,
        })

    return results


def summarize(results):
    summary = {
        "total_cases": len(results),
        "lexical_tp": 0,
        "lexical_fp": 0,
        "lexical_fn": 0,
        "semantic_tp": 0,
        "semantic_fp": 0,
        "semantic_fn": 0,
    }

    by_category = defaultdict(lambda: {
        "count": 0,
        "lexical_correct": 0,
        "semantic_correct": 0,
        "lexical_fp": 0,
        "semantic_fp": 0,
        "lexical_fn": 0,
        "semantic_fn": 0,
    })

    for r in results:
        expected = r["expected_divergence"]

        if r["lexical_flag"] and expected:
            summary["lexical_tp"] += 1
        if r["lexical_flag"] and not expected:
            summary["lexical_fp"] += 1
        if not r["lexical_flag"] and expected:
            summary["lexical_fn"] += 1

        if r["semantic_flag"] and expected:
            summary["semantic_tp"] += 1
        if r["semantic_flag"] and not expected:
            summary["semantic_fp"] += 1
        if not r["semantic_flag"] and expected:
            summary["semantic_fn"] += 1

        cat = by_category[r["category"]]
        cat["count"] += 1
        cat["lexical_correct"] += int(r["lexical_correct"])
        cat["semantic_correct"] += int(r["semantic_correct"])

        if r["lexical_flag"] and not expected:
            cat["lexical_fp"] += 1
        if r["semantic_flag"] and not expected:
            cat["semantic_fp"] += 1
        if not r["lexical_flag"] and expected:
            cat["lexical_fn"] += 1
        if not r["semantic_flag"] and expected:
            cat["semantic_fn"] += 1

    return summary, dict(by_category)


def main():
    with open("experiments/watchdog_evaluation/watchdog_failure_cases.json") as f:
        cases = json.load(f)

    results = evaluate(cases)
    summary, by_category = summarize(results)

    output = {
        "experiment": "watchdog_failure_modes_stress_test",
        "results": results,
        "summary": summary,
        "by_category": by_category,
    }

    with open("experiments/watchdog_evaluation/watchdog_failure_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nSUMMARY")
    print("=" * 80)
    for k, v in summary.items():
        print(f"{k}: {v}")

    print("\nBY CATEGORY")
    print("=" * 80)
    for category, metrics in by_category.items():
        print(f"\n{category}")
        for k, v in metrics.items():
            print(f"{k}: {v}")

    print("\nSaved results to watchdog_failure_results.json")


if __name__ == "__main__":
    main()
