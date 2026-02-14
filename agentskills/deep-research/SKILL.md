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

**Via uvx from GitHub:**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "Your query" --provider openai
```

**Alternative (direct script):**
```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/research.py "Your query" --provider openai
```

## Quick Start

### OpenAI Deep Research
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "What are the latest AI breakthroughs?" --provider openai
```

### DeepSeek Reasoning
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "Explain quantum computing" --provider deepseek
```

### From File with Custom Output
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research --query-file query.md --output report.md --provider openai
```

## Options

| Option | Purpose |
|--------|---------|
| `QUERY` | Research query (positional) |
| `--provider {openai,deepseek}` | Which provider to use (default: openai) |
| `--model MODEL` | Specific model to use |
| `--query-file FILE` | Read query from file |
| `--output FILE` | Save results to specified file path |
| `--poll` | Auto-poll until complete (for OpenAI) |
| `--verbose` | Show detailed output |
| `--env-file FILE` | Load credentials from specific .env file |

## Related Commands

### Poll Research (reconnect to long-running jobs)
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research REQUEST_ID
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research REQUEST_ID --check-only
```

### Extract JSON (extract markdown from raw response)
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" extract_json input.json output.md
```

## Environment Variables

```bash
export OPENAI_API_KEY="your-key"      # For OpenAI provider
export DEEPSEEK_API_KEY="your-key"    # For DeepSeek provider
```

---

## Understanding `uvx --from`

The `uvx --from` syntax provides flexible remote execution:

```bash
# From GitHub (main branch)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "query"

# From specific branch
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@develop[research]" research "query"

# From specific tag/version
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@v1.0.0[research]" research "query"

# From specific commit
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@abc123[research]" research "query"
```

### Available Extras

| Extra | Dependencies | Commands |
|-------|--------------|----------|
| `research` | `httpx` | `research`, `poll_research`, `extract_json` |
| `gamma` | (base only) | `generate_gamma_presentation`, `get_gamma_assets` |
| `keep` | `gkeepapi` | `google_keep` |
| `nanobanana` | `google-generativeai`, `pillow` | `nanobanana` |
| `all` | All dependencies | All commands |

See [scripts/README.md](../../scripts/README.md) for full documentation on `uvx --from` options.

---

## Source

https://github.com/cbruyndoncx/ThirdBrAIn-Tools/tree/main/scripts
