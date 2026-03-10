# runner.py — DO NOT MODIFY
# Runs one full evaluation, measures score, manages git commits.

import os
import sys
import time
import json
import subprocess
from datetime import datetime
import anthropic
import importlib.util

from tasks import TASKS, TOOLS


MAX_RUN_SECONDS = 180  # 3 minutes hard wall
RESULTS_FILE = "results/history.jsonl"
BEST_SCORE_FILE = "results/best_score.txt"


def load_scaffold():
    """Dynamically reload scaffold.py on each run."""
    spec = importlib.util.spec_from_file_location("scaffold", "scaffold.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def evaluate(scaffold_mod, client) -> dict:
    """Run all tasks, return aggregate results."""
    results = []
    start = time.time()

    for task in TASKS:
        if time.time() - start > MAX_RUN_SECONDS:
            print(f"  [runner] Time limit hit after {len(results)} tasks")
            break

        try:
            result = scaffold_mod.run_task(task, client)
            answer = str(result.get("answer", "")).strip()
            tokens = int(result.get("tokens_used", 999))
        except Exception as e:
            answer = "SCAFFOLD_ERROR"
            tokens = 0
            print(f"  [runner] Task {task['id']} failed: {e}")

        correct = _check_answer(task, answer)
        results.append({
            "task_id": task["id"],
            "category": task["category"],
            "correct": correct,
            "tokens": tokens,
            "answer": answer,
            "expected": task["answer"]
        })

    success_rate = sum(r["correct"] for r in results) / len(results)
    avg_tokens = sum(r["tokens"] for r in results) / max(len(results), 1)
    score = success_rate - 0.1 * (avg_tokens / 2000.0)

    return {
        "score": round(score, 4),
        "success_rate": round(success_rate, 4),
        "avg_tokens": round(avg_tokens, 1),
        "n_tasks": len(results),
        "results": results
    }


def _check_answer(task: dict, answer: str) -> bool:
    """Check if the agent's answer is correct."""
    expected = str(task["answer"]).strip().lower()
    answer_clean = answer.strip().lower()
    eval_type = task.get("eval_type", "exact")

    if eval_type == "exact":
        return answer_clean == expected or expected in answer_clean
    elif eval_type == "count_check":
        import re
        numbers = re.findall(r'\d+', answer_clean)
        target = re.findall(r'\d+', expected)[0] if re.findall(r'\d+', expected) else "0"
        return target in numbers
    elif eval_type == "ordered_steps":
        return True
    return False


def get_best_score() -> float:
    """Read the best score from disk."""
    os.makedirs("results", exist_ok=True)
    if not os.path.exists(BEST_SCORE_FILE):
        return -999.0
    with open(BEST_SCORE_FILE) as f:
        return float(f.read().strip())


def set_best_score(score: float):
    """Write the best score to disk."""
    with open(BEST_SCORE_FILE, "w") as f:
        f.write(str(score))


def git_commit(message: str):
    """Commit scaffold.py with a descriptive message."""
    subprocess.run(["git", "add", "scaffold.py"], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)


def git_revert_scaffold():
    """Revert scaffold.py to the last committed version."""
    subprocess.run(["git", "checkout", "HEAD", "--", "scaffold.py"], check=True)


def log_result(eval_result: dict, committed: bool):
    """Append experiment result to the history log."""
    os.makedirs("results", exist_ok=True)
    with open(RESULTS_FILE, "a") as f:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "score": eval_result["score"],
            "success_rate": eval_result["success_rate"],
            "avg_tokens": eval_result["avg_tokens"],
            "committed": committed
        }
        f.write(json.dumps(entry) + "\n")


def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    scaffold_mod = load_scaffold()

    print(f"\n[runner] Starting evaluation — {datetime.utcnow().isoformat()}")
    eval_result = evaluate(scaffold_mod, client)
    score = eval_result["score"]
    best = get_best_score()

    print(f"[runner] Score: {score:.4f} | Success: {eval_result['success_rate']:.1%} | Avg tokens: {eval_result['avg_tokens']:.0f}")
    print(f"[runner] Best so far: {best:.4f}")

    if score > best:
        print(f"[runner] ✓ Improvement! Committing scaffold.")
        commit_msg = f"score={score:.4f} success={eval_result['success_rate']:.1%} tokens={eval_result['avg_tokens']:.0f}"
        git_commit(commit_msg)
        set_best_score(score)
        committed = True
    else:
        print(f"[runner] ✗ No improvement. Reverting scaffold.py.")
        git_revert_scaffold()
        committed = False

    log_result(eval_result, committed)
    return score


if __name__ == "__main__":
    main()
