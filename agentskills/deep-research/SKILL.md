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

```bash
uvx --from git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools/agentskills/deep-research research [QUERY] [OPTIONS]
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
uvx --from git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools/agentskills/deep-research research "What is quantum computing?" --provider deepseek
```

**OpenAI with auto-polling**
```bash
uvx --from git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools/agentskills/deep-research research "Analyze AI trends" --provider openai --poll
```

**Save to custom file path**
```bash
uvx --from git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools/agentskills/deep-research research "Your query" --provider deepseek --output /path/to/report.md
```


## Environment Variables

- `OPENAI_API_KEY` - OpenAI authentication
- `DEEPSEEK_API_KEY` - DeepSeek authentication

## Source

https://github.com/cbruyndoncx/ThirdBrAIn-Tools/tree/main/agentskills/deep-research
