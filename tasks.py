# tasks.py — DO NOT MODIFY

TASKS = [
    # --- Category 1: Multi-hop Reasoning (5 tasks) ---
    {
        "id": "mh_01",
        "category": "multihop",
        "prompt": "The Eiffel Tower is in the capital of France. What country is that capital in?",
        "answer": "France",
        "tools_available": []
    },
    {
        "id": "mh_02",
        "category": "multihop",
        "prompt": "The author of 'Foundation' was born in what decade?",
        "answer": "1920s",
        "tools_available": []
    },
    {
        "id": "mh_03",
        "category": "multihop",
        "prompt": "If the boiling point of water is 100C and you are at altitude where it drops by 3C per 1000m, what is the boiling point at 3000m?",
        "answer": "91",
        "tools_available": []
    },
    {
        "id": "mh_04",
        "category": "multihop",
        "prompt": "The company that made the first iPhone is headquartered in which US state?",
        "answer": "California",
        "tools_available": []
    },
    {
        "id": "mh_05",
        "category": "multihop",
        "prompt": "The Roman numeral for 9 is IX. What is XIX minus IX in decimal?",
        "answer": "10",
        "tools_available": []
    },

    # --- Category 2: Tool Use — Calculator (5 tasks) ---
    {
        "id": "tool_calc_01",
        "category": "tool_use",
        "prompt": "What is 847 * 293?",
        "answer": "248171",
        "tools_available": ["calculator"]
    },
    {
        "id": "tool_calc_02",
        "category": "tool_use",
        "prompt": "What is the square root of 15129?",
        "answer": "123",
        "tools_available": ["calculator"]
    },
    {
        "id": "tool_calc_03",
        "category": "tool_use",
        "prompt": "If a rectangle has length 47 and width 83, what is its area?",
        "answer": "3901",
        "tools_available": ["calculator"]
    },
    {
        "id": "tool_calc_04",
        "category": "tool_use",
        "prompt": "What is 2 to the power of 12?",
        "answer": "4096",
        "tools_available": ["calculator"]
    },
    {
        "id": "tool_calc_05",
        "category": "tool_use",
        "prompt": "What percentage is 37 of 148?",
        "answer": "25",
        "tools_available": ["calculator"]
    },

    # --- Category 3: Planning & Decomposition (5 tasks) ---
    {
        "id": "plan_01",
        "category": "planning",
        "prompt": "List the steps to bake a chocolate cake in the correct order. Return only the step numbers 1-5 as a comma-separated list.",
        "answer": "1,2,3,4,5",
        "tools_available": [],
        "eval_type": "ordered_steps"
    },
    {
        "id": "plan_02",
        "category": "planning",
        "prompt": "To deploy a web app, which comes first: writing code, testing, or deploying? Answer with a single word.",
        "answer": "writing",
        "tools_available": []
    },
    {
        "id": "plan_03",
        "category": "planning",
        "prompt": "Break this goal into exactly 3 sub-tasks: 'Find the cheapest flight from NYC to LAX next week'. Return sub-tasks as a numbered list.",
        "answer": "3_subtasks",
        "eval_type": "count_check",
        "tools_available": []
    },
    {
        "id": "plan_04",
        "category": "planning",
        "prompt": "What is the minimum number of steps to make a PB&J sandwich? Answer with just the number.",
        "answer": "4",
        "tools_available": []
    },
    {
        "id": "plan_05",
        "category": "planning",
        "prompt": "To solve 'what is 15% tip on a $47 bill', do you need: (a) only math, (b) a web search, or (c) both? Answer with a single letter.",
        "answer": "a",
        "tools_available": []
    },

    # --- Category 4: Error Recovery (5 tasks) ---
    {
        "id": "err_01",
        "category": "error_recovery",
        "prompt": "Use the calculator tool to compute 'hello * 3'. If it fails, return the string 'TOOL_ERROR'.",
        "answer": "TOOL_ERROR",
        "tools_available": ["calculator"]
    },
    {
        "id": "err_02",
        "category": "error_recovery",
        "prompt": "Try to get the weather for 'Atlantis'. If unavailable, return 'UNKNOWN_LOCATION'.",
        "answer": "UNKNOWN_LOCATION",
        "tools_available": ["weather"]
    },
    {
        "id": "err_03",
        "category": "error_recovery",
        "prompt": "You receive an empty string as input. What should a well-behaved agent return? Answer: 'CLARIFICATION_NEEDED' or 'PROCEED'.",
        "answer": "CLARIFICATION_NEEDED",
        "tools_available": []
    },
    {
        "id": "err_04",
        "category": "error_recovery",
        "prompt": "A tool call times out after 3 retries. Should the agent: (a) crash, (b) return partial answer with a caveat, (c) loop forever? Answer with a single letter.",
        "answer": "b",
        "tools_available": []
    },
    {
        "id": "err_05",
        "category": "error_recovery",
        "prompt": "The calculator tool returns '∞' for 1/0. What should the agent report to the user? Answer: 'DIVISION_BY_ZERO' or 'INFINITY'.",
        "answer": "DIVISION_BY_ZERO",
        "tools_available": []
    },

    # --- Category 5: Context Compression (5 tasks) ---
    {
        "id": "ctx_01",
        "category": "context",
        "prompt": "Given a 10-sentence paragraph about climate change, produce a 1-sentence summary. Return only the sentence count of your summary.",
        "answer": "1",
        "tools_available": []
    },
    {
        "id": "ctx_02",
        "category": "context",
        "prompt": "You have 5 prior messages in context. How many should you retain to answer a question about only the most recent topic? Answer with a number 1-5.",
        "answer": "1",
        "tools_available": []
    },
    {
        "id": "ctx_03",
        "category": "context",
        "prompt": "A user asks a follow-up question. The original question was: 'What is photosynthesis?' The follow-up is: 'How long does it take?' What minimal context do you need? Answer: 'original_only', 'followup_only', or 'both'.",
        "answer": "both",
        "tools_available": []
    },
    {
        "id": "ctx_04",
        "category": "context",
        "prompt": "You are 4000 tokens into a conversation. A new question is unrelated to everything prior. Should you: (a) keep full history, (b) clear and start fresh, (c) summarize prior context? Answer with a single letter.",
        "answer": "b",
        "tools_available": []
    },
    {
        "id": "ctx_05",
        "category": "context",
        "prompt": "Rate the importance of system prompt vs conversation history for answering a domain-specific question. Which matters MORE? Answer: 'system_prompt' or 'conversation_history'.",
        "answer": "system_prompt",
        "tools_available": []
    },
]


def calculator(expression: str) -> str:
    """Evaluates a safe math expression. Raises ValueError on invalid input."""
    import math
    try:
        allowed = set("0123456789+-*/().,^ sqrtlogpie")
        if not all(c in allowed for c in expression.replace(" ", "")):
            raise ValueError(f"Invalid expression: {expression}")
        expr = expression.replace("^", "**").replace("sqrt", "math.sqrt")
        return str(eval(expr, {"__builtins__": {}, "math": math}))
    except Exception as e:
        raise ValueError(str(e))


def weather(location: str) -> str:
    """Mock weather tool. Only works for known cities."""
    known = {"New York": "72F Sunny", "London": "58F Cloudy", "Tokyo": "65F Clear"}
    if location not in known:
        raise ValueError(f"Location not found: {location}")
    return known[location]


TOOLS = {
    "calculator": calculator,
    "weather": weather,
}
