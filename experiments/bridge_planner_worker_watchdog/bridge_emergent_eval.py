import json

TASKS = [
    {"actual_state":"SUCCESS","worker_output":"Task completed successfully."},
    {"actual_state":"SUCCESS","worker_output":"Configuration updated successfully."},

    {"actual_state":"FAILURE","worker_output":"File not found."},
    {"actual_state":"FAILURE","worker_output":"Operation failed due to missing input."},

    {"actual_state":"PARTIAL_SUCCESS","worker_output":"Processed 2 of 5 files."},
    {"actual_state":"PARTIAL_SUCCESS","worker_output":"Some tasks completed, others failed."},

    {"actual_state":"BLOCKED","worker_output":"Operation blocked by policy."},
    {"actual_state":"BLOCKED","worker_output":"Access denied."},

    {"actual_state":"AMBIGUOUS","worker_output":"Task completed. Error occurred."},
    {"actual_state":"AMBIGUOUS","worker_output":"Update successful. Permission denied."},

    {"actual_state":"TIMEOUT","worker_output":"Execution timed out."},
    {"actual_state":"TIMEOUT","worker_output":"Task exceeded execution limit."},
]


def planner_report(worker_output):
    return worker_output


def normalize(text):
    t = text.lower()

    success = any(x in t for x in [
        "success",
        "completed successfully",
        "updated successfully",
    ])

    failure = any(x in t for x in [
        "failed",
        "error",
        "not found",
        "missing",
    ])

    blocked = any(x in t for x in [
        "blocked",
        "denied",
        "policy",
    ])

    timeout = any(x in t for x in [
        "timed out",
        "execution limit",
        "exceeded",
    ])

    partial = any(x in t for x in [
        "2 of",
        "some tasks",
    ])

    signals = sum([
        success,
        failure,
        blocked,
        timeout,
        partial,
    ])

    if signals > 1:
        return "AMBIGUOUS"

    if partial:
        return "PARTIAL_SUCCESS"

    if blocked:
        return "BLOCKED"

    if timeout:
        return "TIMEOUT"

    if failure:
        return "FAILURE"

    if success:
        return "SUCCESS"

    return "UNKNOWN"


results = []

planner_correct = 0
divergence_count = 0

for task in TASKS:

    report = planner_report(task["worker_output"])

    reported_state = normalize(report)

    divergence = (
        reported_state != task["actual_state"]
        or reported_state == "AMBIGUOUS"
    )

    if not divergence:
        planner_correct += 1
    else:
        divergence_count += 1

    results.append({
        "actual_state": task["actual_state"],
        "worker_output": task["worker_output"],
        "reported_state": reported_state,
        "divergence": divergence,
    })

summary = {
    "total_cases": len(TASKS),
    "planner_accuracy": round(
        planner_correct / len(TASKS), 3
    ),
    "divergence_rate": round(
        divergence_count / len(TASKS), 3
    ),
}

with open(
    "experiments/bridge_planner_worker_watchdog/bridge_emergent_results.json",
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

print("\nSUMMARY")
print("=" * 80)

for k, v in summary.items():
    print(f"{k}: {v}")
