# scaffold.py — v0 baseline scaffold
# This is the ONLY file the agent modifies.
# It must export exactly one function: run_task(task: dict, client) -> dict

import re


def run_task(task: dict, client) -> dict:
    """
    Given a task dict and an Anthropic client, return:
    {
        "answer": str,         # the agent's final answer
        "tokens_used": int,    # total input + output tokens
        "reasoning": str       # brief explanation (optional, for debugging)
    }
    """
    # --- v0: Single-shot prompt, no tools, no reflection ---
    tools_available = task.get("tools_available", [])
    prompt = _build_prompt(task["prompt"], tools_available)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_answer = response.content[0].text.strip()
    tokens_used = response.usage.input_tokens + response.usage.output_tokens

    return {
        "answer": _extract_answer(raw_answer),
        "tokens_used": tokens_used,
        "reasoning": raw_answer
    }


def _build_prompt(task_prompt: str, tools_available: list) -> str:
    """Construct the prompt sent to the model."""
    system_note = ""
    if tools_available:
        system_note = f"\nYou have access to these tools: {tools_available}. State 'TOOL_ERROR' if a tool fails."

    return f"""Answer the following question concisely. Return ONLY the answer, no explanation.
{system_note}

Question: {task_prompt}

Answer:"""


def _extract_answer(raw: str) -> str:
    """Clean up model output to extract the final answer."""
    for prefix in ["Answer:", "answer:", "The answer is", "Result:"]:
        if raw.startswith(prefix):
            raw = raw[len(prefix):].strip()
    return raw.split("\n")[0].strip()
