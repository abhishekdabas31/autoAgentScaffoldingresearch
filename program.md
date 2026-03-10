# autoAgentScaffoldingresearch — Research Program

## Goal
Maximize `task_success_rate` while minimizing token usage per task.
Score = success_rate - 0.1 * (avg_tokens / 2000)
Higher is better. Target: score > 0.80 within 50 experiments.

## What You May Change
- ONLY `scaffold.py`
- You may change: prompt structure, reflection loops, tool call handling,
  context window strategy, answer extraction logic, retry logic,
  system messages, model selection (haiku vs sonnet — note cost tradeoff)

## What You Must Never Change
- `tasks.py` — the eval suite is sacred
- `runner.py` — the measurement harness is fixed
- The function signature: `run_task(task, client) -> dict`

## Current Hypotheses to Explore (in rough priority order)
1. Does adding a brief chain-of-thought step before extracting the final answer improve success rate?
2. Does a reflection step ("was my answer correct given the question?") help on error_recovery tasks?
3. Does tool-category routing (detect if calculator is needed, call it explicitly via the mock) improve tool_use tasks?
4. Does shrinking the prompt on context tasks (stripping explanation, going ultra-terse) reduce tokens without hurting accuracy?
5. Can you detect task category from the prompt text and apply a different strategy per category?

## Known Good Moves (from prior sessions)
- (empty at start — agent fills this in via commit messages)

## Coding Style Rules
- Keep scaffold.py under 150 lines
- No external imports beyond anthropic and re/json/os
- Every function must have a one-line docstring
- No global state
