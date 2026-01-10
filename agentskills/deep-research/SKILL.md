---
name: deep-research
description: Conduct deep research with OpenAI and DeepSeek reasoning models. Use when you need comprehensive, well-reasoned analysis of complex topics.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Deep Research Skill

Unified deep research across multiple AI providers. Create research requests, auto-poll for completion, and return formatted markdown reports.

## Usage

**In Claude Code:**
```bash
/deep-research "Your research query" --provider deepseek
```

**Via uvx from GitHub:**
```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools research [QUERY] [OPTIONS]
```

**Local development:**
```bash
python -m scripts.research [QUERY] [OPTIONS]
```

## Options

| Option | Purpose |
|--------|---------|
| `QUERY` | Research query |
| `--provider {openai,deepseek}` | Which provider to use (default: openai) |
| `--model MODEL` | Specific model to use |
| `--query-file FILE` | Read query from file |
| `--output FILE` | Save results to specified file path |
| `--poll` | Auto-poll until complete (for OpenAI) |
| `--check-status ID` | Check status of running request |
| `--get-results ID` | Get results of completed request |
| `--verbose` | Show detailed output |

## Examples

**DeepSeek (fast, synchronous)**
```bash
python -m scripts.research "What is quantum computing?" --provider deepseek
```

**OpenAI with auto-polling**
```bash
python -m scripts.research "Analyze AI trends" --provider openai --poll
```

**Save to custom file path**
```bash
python -m scripts.research "Your query" --provider deepseek --output /path/to/report.md
```

**From GitHub via uvx**
```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools research "What is quantum computing?" --provider deepseek
```


## Environment Variables

- `OPENAI_API_KEY` - OpenAI authentication
- `DEEPSEEK_API_KEY` - DeepSeek authentication

## Source

https://github.com/cbruyndoncx/ThirdBrAIn-Tools/tree/main/agentskills/deep-research
