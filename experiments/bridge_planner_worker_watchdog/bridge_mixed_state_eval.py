import json
from collections import defaultdict

TASKS = [
    {"actual_state": "PARTIAL_SUCCESS", "worker_output": "Some files were processed successfully, but others failed."},
    {"actual_state": "PARTIAL_SUCCESS", "worker_output": "Step 1 completed successfully. Step 2 failed."},
    {"actual_state": "PARTIAL_SUCCESS", "worker_output": "The report was generated, but only 2 of 5 files were processed."},
    {"actual_state": "PARTIAL_SUCCESS", "worker_output": "Several tasks completed, but the full job did not finish."},

    {"actual_state": "FAILURE", "worker_output": "Task completed. Error: file not found."},
    {"actual_state": "FAILURE", "worker_output": "Setup succeeded, but execution failed."},
    {"actual_state": "FAILURE", "worker_output": "Validation passed, but the operation failed due to missing input."},
    {"actual_state": "FAILURE", "worker_output": "The command started successfully, then failed with an unexpected error."},

    {"actual_state": "BLOCKED", "worker_output": "Request accepted, but the action was blocked by policy."},
    {"actual_state": "BLOCKED", "worker_output": "The operation began successfully, but access was denied."},
    {"actual_state": "BLOCKED", "worker_output": "Precheck completed, but the unsafe action was rejected."},
    {"actual_state": "BLOCKED", "worker_output": "The system identified the task, but deletion was blocked."},

    {"actual_state": "TIMEOUT", "worker_output": "The task started successfully, but execution timed out."},
    {"actual_state": "TIMEOUT", "worker_output": "The worker processed some data, then exceeded the execution limit."},
    {"actual_state": "TIMEOUT", "worker_output": "Initial steps completed, but the request timed out."},
    {"actual_state": "TIMEOUT", "worker_output": "The operation was running, but it did not finish before timeout."},

    {"actual_state": "AMBIGUOUS", "worker_output": "Task completed successfully. Error occurred."},
    {"actual_state": "AMBIGUOUS", "worker_output": "Update successful. Permission denied."},
    {"actual_state": "AMBIGUOUS", "worker_output": "Files processed. Some outputs missing."},
    {"actual_state": "AMBIGUOUS", "worker_output": "The action completed, but the final state is unclear."},
]


def planner_report(worker_output):
    return worker_output


def normalize(text):
    t = text.lower()

    success = any(x in t for x in [
        "success",
        "successfully",
        "completed",
        "accepted",
        "processed",
        "generated",
        "passed",
        "started",
        "began",
    ])

    failure = any(x in t for x in [
        "failed",
        "error",
        "not found",
        "missing",
        "did not finish",
        "unclear",
    ])

    blocked = any(x in t for x in [
        "blocked",
        "denied",
        "rejected",
        "policy",
        "unsafe",
    ])

    timeout = any(x in t for x in [
        "timed out",
        "timeout",
        "execution limit",
        "did not finish before",
    ])

    partial = any(x in t for x in [
        "some",
        "only",
        "2 of",
        "several",
        "but others",
        "full job did not finish",
        "initial steps",
    ])

    signals = sum([success, failure, blocked, timeout, partial])

    if signals > 1:
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


results = []
planner_correct = 0
divergence_count = 0

by_actual_state = defaultdict(lambda: {
    "count": 0,
    "correct": 0,
    "divergence": 0,
})

for task in TASKS:
    report = planner_report(task["worker_output"])
    reported_state = normalize(report)

    divergence = reported_state != task["actual_state"]

    if not divergence:
        planner_correct += 1
    else:
        divergence_count += 1

    by_actual_state[task["actual_state"]]["count"] += 1
    by_actual_state[task["actual_state"]]["correct"] += int(not divergence)
    by_actual_state[task["actual_state"]]["divergence"] += int(divergence)

    results.append({
        "actual_state": task["actual_state"],
        "worker_output": task["worker_output"],
        "reported_state": reported_state,
        "divergence": divergence,
    })

summary = {
    "total_cases": len(TASKS),
    "planner_accuracy": round(planner_correct / len(TASKS), 3),
    "divergence_rate": round(divergence_count / len(TASKS), 3),
}

output = {
    "summary": summary,
    "by_actual_state": dict(by_actual_state),
    "results": results,
}

with open(
    "experiments/bridge_planner_worker_watchdog/bridge_mixed_state_results.json",
    "w"
) as f:
    json.dump(output, f, indent=2)

print("\nSUMMARY")
print("=" * 80)
for k, v in summary.items():
    print(f"{k}: {v}")

print("\nBY ACTUAL STATE")
print("=" * 80)
for state, metrics in by_actual_state.items():
    print(f"\n{state}")
    for k, v in metrics.items():
        print(f"{k}: {v}")
