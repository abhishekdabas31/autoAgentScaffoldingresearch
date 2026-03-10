# autoAgentScaffoldingresearch

> Closed labs master model weights. This repo masters the space between the weights.

An autonomous agent that iterates on its own agentic scaffolding code overnight.
Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch).

## The Idea

| autoresearch | autoAgentScaffoldingresearch |
|---|---|
| Fixed domain: LLM training | Fixed domain: agentic task suite |
| Editable: `train.py` | Editable: `scaffold.py` |
| Metric: validation BPB | Metric: task success - token penalty |
| Human writes: `program.md` | Human writes: `program.md` |

## Setup

```bash
git clone https://github.com/abhishekdabas31/autoAgentScaffoldingresearch.git
cd autoAgentScaffoldingresearch
pip install -r requirements.txt
git init && git add . && git commit -m "init"
export ANTHROPIC_API_KEY=sk-...
```

## Run

```bash
# Run 50 experiments overnight (~2.5 hours)
python agent_loop.py --experiments 50

# Inspect progress
cat results/history.jsonl | python -c "
import sys, json
for line in sys.stdin:
    r = json.loads(line)
    icon = '✓' if r['committed'] else '✗'
    print(f\"{icon} score={r['score']} success={r['success_rate']} tokens={r['avg_tokens']:.0f}\")
"

# See what the agent changed
git log --oneline
```

## File Roles

| File | Role | Who touches it |
|---|---|---|
| `scaffold.py` | Agentic orchestration code | Agent only |
| `tasks.py` | 25 fixed evaluation tasks | Nobody |
| `runner.py` | Measures score, handles git | Nobody |
| `program.md` | Research hypotheses | Human only |
| `agent_loop.py` | Outer agent loop | Nobody |
