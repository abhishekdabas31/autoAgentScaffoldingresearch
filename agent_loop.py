# agent_loop.py — The autonomous research loop
# Run: python agent_loop.py --experiments 50

import os
import sys
import argparse
import subprocess
import anthropic

SCAFFOLD_FILE = "scaffold.py"
PROGRAM_FILE = "program.md"
RESULTS_FILE = "results/history.jsonl"


def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str):
    """Write content to a file."""
    with open(path, "w") as f:
        f.write(content)


def get_experiment_count() -> int:
    """Return the number of experiments completed so far."""
    try:
        with open(RESULTS_FILE) as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def propose_scaffold_change(client: anthropic.Anthropic) -> str:
    """Ask Claude to read program.md + scaffold.py and propose an improved scaffold.py."""
    program = read_file(PROGRAM_FILE)
    scaffold = read_file(SCAFFOLD_FILE)
    n = get_experiment_count()

    user_message = f"""You are an autonomous AI research agent. Your job is to improve agentic scaffolding code.

## Research Program (your instructions)
{program}

## Current scaffold.py (experiment #{n})
```python
{scaffold}
```

## Your Task
1. Review the research program hypotheses.
2. Pick ONE hypothesis to test that hasn't been tried yet (or a natural follow-up to a recent commit).
3. Propose a MINIMAL change to scaffold.py that tests it.
4. Output ONLY the complete new scaffold.py — no explanation, no markdown fences, just raw Python.

Rules:
- Keep the file under 150 lines
- The function signature `run_task(task, client)` must remain identical
- No new external dependencies
- One focused change per experiment — do NOT change everything at once
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text.strip()


def run_evaluation() -> float:
    """Run runner.py and return the score."""
    result = subprocess.run(
        [sys.executable, "runner.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"[agent] Runner error: {result.stderr}")
        return -999.0
    for line in result.stdout.split("\n"):
        if "Score:" in line:
            try:
                return float(line.split("Score:")[1].split("|")[0].strip())
            except Exception:
                pass
    return -999.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiments", type=int, default=20)
    args = parser.parse_args()

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    print(f"[agent] Starting autoScaffold — {args.experiments} experiments planned")
    print(f"[agent] Current experiment count: {get_experiment_count()}")

    for i in range(args.experiments):
        print(f"\n{'='*50}")
        print(f"[agent] Experiment {i+1}/{args.experiments}")
        print(f"{'='*50}")

        print("[agent] Proposing scaffold change...")
        new_scaffold = propose_scaffold_change(client)

        write_file(SCAFFOLD_FILE, new_scaffold)
        print("[agent] scaffold.py updated. Running evaluation...")

        score = run_evaluation()
        print(f"[agent] Experiment complete. Score: {score:.4f}")

    print(f"\n[agent] Done. {args.experiments} experiments complete.")
    print(f"[agent] Check results/history.jsonl and git log for progress.")


if __name__ == "__main__":
    main()
