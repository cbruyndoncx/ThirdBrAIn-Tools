---
name: deep-research
description: Conduct deep research with OpenAI and DeepSeek reasoning models. Use when you need comprehensive, well-reasoned analysis of complex topics.
allowed-tools:
  - Bash
  - Read
  - Write
context: fork
agent: general-purpose
user-invocable: true
---

# Deep Research Skill

Unified deep research across multiple AI providers using uvx. Create research requests, auto-poll for completion, and return formatted markdown reports.

## Quick Start

### 1. Install uvx (one-time)
```bash
pip install uv
```

### 2. Set API Keys
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="your-key-here"
export DEEPSEEK_API_KEY="your-key-here"
```

Then reload:
```bash
source ~/.bashrc
```

### 3. Run Research
```bash
# Quick research (synchronous)
uvx --from ~/.claude/skills/deep-research research "What is quantum computing?" --provider deepseek

# Complex research with OpenAI (auto-polls)
uvx --from ~/.claude/skills/deep-research research "Analyze AI trends" --provider openai --poll
```

### 4. Create Alias (optional)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias research='uvx --from ~/.claude/skills/deep-research research'
```

Then use simply:
```bash
research "your query" --provider deepseek
```

## How uvx Works

When you run:
```bash
uvx --from ~/.claude/skills/deep-research research "query"
```

uvx:
1. Reads `pyproject.toml` from `~/.claude/skills/deep-research/`
2. Finds entry point: `research = "deep_research.research:main"`
3. Installs dependencies (httpx) in isolated environment
4. Runs the `main()` function from `src/deep_research/research.py`
5. Passes arguments to the script

## Command Reference

### Basic Syntax
```bash
research [QUERY] [OPTIONS]
```

### Providers

| Provider | Speed | Cost | Default Model | Response |
|----------|-------|------|---------------|----------|
| **DeepSeek** | Fast ⚡ | Low 💰 | deepseek-reasoner | Synchronous (immediate) |
| **OpenAI** | Slower 🔄 | Higher 💸 | o1 | Async (requires polling) |

### Common Commands

**Quick research (DeepSeek)**
```bash
research "What is X?"
```

**Complex research (OpenAI with auto-polling)**
```bash
research "Explain X in detail" --provider openai --poll
```

**Read query from file**
```bash
research --query-file input.txt --provider deepseek
```

**Read from file, save to file**
```bash
research --query-file input.txt --output output.md --provider openai --poll
```

**Check status of running request**
```bash
research --check-status request_123 --provider openai
```

**Get results of completed request**
```bash
research --get-results request_123 --provider openai
```

## Options

| Option | Purpose | Default |
|--------|---------|---------|
| `QUERY` (positional) | Research query | - |
| `--query-file FILE` | Read query from file instead of CLI | - |
| `--provider {openai,deepseek}` | Which provider to use | `openai` |
| `--model MODEL` | Specific model | provider default |
| `--poll` | Auto-poll until complete | false |
| `--verbose` | Show detailed output | false |

## Adaptive Polling

When using `--poll`, the polling interval automatically increases based on elapsed time:

- **0-10 seconds**: Poll every 10 seconds (catch fast completions)
- **10-30 seconds**: Poll every 30 seconds
- **30 seconds - 5 minutes**: Poll every 1 minute
- **5-30 minutes**: Poll every 5 minutes (reduce API load for long-running tasks)

Maximum timeout is 30 minutes. This strategy balances responsiveness for quick tasks with reduced API load for long-running research.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `OPENAI_API_KEY` | - | OpenAI authentication (required for OpenAI) |
| `DEEPSEEK_API_KEY` | - | DeepSeek authentication (required for DeepSeek) |
| `REASONING_DEFAULT_PROVIDER` | `openai` | Default provider if not specified |
| `OPENAI_DEFAULT_MODEL` | `o1` | Default OpenAI model |
| `DEEPSEEK_DEFAULT_MODEL` | `deepseek-reasoner` | Default DeepSeek model |
| `RESEARCH_RESULTS_DIR` | `~/research-results/` | Where reports are saved |

## Use in Claude Code

Just use the skill directly:

```
/deep-research "What are the latest AI breakthroughs?" --provider deepseek
```

This internally runs:
```bash
uvx --from ~/.claude/skills/deep-research research "What are the latest AI breakthroughs?" --provider deepseek
```

## Workflow Examples

### Quick Research (DeepSeek - Synchronous)

```bash
research "What are the latest breakthroughs in quantum computing?"

# Results automatically saved to ~/research-results/deepseek_*.md
```

### Complex Research (OpenAI - Async with Auto-Polling)

```bash
research "Comprehensive analysis of transformer architecture" \
  --provider openai \
  --model o1 \
  --poll

# Auto-polls with adaptive intervals
# Outputs: markdown report with citations
# Saves to: ~/research-results/openai_*.md
```

### Manual Status Checking

```bash
# Submit request without polling
research "Your question" --provider openai
# Returns: request_id

# Check status later
research --check-status <request-id> --provider openai

# Get results when ready
research --get-results <request-id> --provider openai
```

## Troubleshooting

**"command not found: uvx"**
```bash
pip install uv
```

**"API key not configured"**
```bash
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
# Or add to ~/.bashrc / ~/.zshrc
```

**"cannot find package"**
- Verify path: `ls ~/.claude/skills/deep-research/pyproject.toml`
- Should exist at: `~/.claude/skills/deep-research/`

**OpenAI request timing out**
- The polling uses adaptive intervals (10s→30s→1m→5m) with a max 30min timeout
- Use `--verbose` to see polling progress and timing information
- Try a simpler query to test if the API is responding

**DeepSeek API errors**
- Verify API key: `echo $DEEPSEEK_API_KEY`
- Check rate limits (DeepSeek has usage tiers)
- Try a simpler query to test connectivity

## Requirements

- **uvx** - Install with: `pip install uv`
- **Python 3.10+** - Required for the research script (uvx handles this)
- **API Keys** - Set `OPENAI_API_KEY` and/or `DEEPSEEK_API_KEY`
- **~50MB disk** - For research reports in `~/research-results/`
- **Internet connection** - For API calls to OpenAI or DeepSeek

## Directory Structure

```
~/.claude/skills/deep-research/
├── src/
│   └── deep_research/
│       ├── research.py              (entry point)
│       ├── providers/
│       │   ├── openai.py
│       │   └── deepseek.py
│       └── shared/
│           ├── base.py
│           └── utils.py
├── pyproject.toml                   (defines entry point)
└── SKILL.md                         (this file)
```
