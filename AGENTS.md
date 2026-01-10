# AGENTS.md

This file documents all Claude Code skills and agents available in this repository. It is the single source of truth for agent/skill architecture and development.

## Project Overview

ThirdBrAIn-Tools is a repository for building reusable Claude Code skills. Currently, it contains the **deep-research** skill, which provides unified deep research capabilities across multiple AI providers (OpenAI and DeepSeek).

## Available Skills

### deep-research

**Conduct deep research with OpenAI and DeepSeek reasoning models.**

Unified deep research across multiple AI providers using uvx. Create research requests, auto-poll for completion, and return formatted markdown reports.

- **Skill Name:** `deep-research`
- **Location:** `agentskills/deep-research/`
- **Files:**
  - `SKILL.md` - Full skill documentation and usage guide
  - `pyproject.toml` - Package definition with entry point
  - `src/deep_research/` - Python implementation

**Quick Start:**
```bash
# Install uv (one-time)
pip install uv

# Set API keys
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"

# Use in Claude Code
/deep-research "What is quantum computing?" --provider deepseek

# Or run directly
uvx --from ~/.claude/skills/deep-research research "What is quantum computing?" --provider deepseek
```

**Command Reference:**

| Command | Purpose |
|---------|---------|
| `research "query"` | Quick research (DeepSeek - synchronous) |
| `research "query" --provider openai --poll` | Complex research with auto-polling |
| `research --query-file input.txt --provider deepseek` | Read query from file |
| `research --query-file input.txt --output output.md --provider openai --poll` | Read from file, save to file |
| `research --check-status request_123 --provider openai` | Check status of running request |
| `research --get-results request_123 --provider openai` | Get results of completed request |

**Key Options:**

| Option | Purpose | Default |
|--------|---------|---------|
| `QUERY` (positional) | Research query | - |
| `--query-file FILE` | Read query from file instead of CLI | - |
| `--provider {openai,deepseek}` | Which provider to use | `openai` |
| `--model MODEL` | Specific model | provider default |
| `--poll` | Auto-poll until complete | false |
| `--verbose` | Show detailed output | false |

**Provider Comparison:**

| Provider | Speed | Cost | Model | Response |
|----------|-------|------|-------|----------|
| DeepSeek | Fast ⚡ | Low 💰 | deepseek-reasoner | Synchronous (immediate) |
| OpenAI | Slower 🔄 | Higher 💸 | o1 | Async (requires polling) |

See `agentskills/deep-research/SKILL.md` for complete documentation, examples, and troubleshooting.

## Architecture: Claude Code Skills

### Skill Structure

Each skill in `agentskills/` contains:
- **SKILL.md** - User-facing documentation and command reference
- **pyproject.toml** - Python package definition with entry point
- **src/** - Python implementation

### How Skills Are Invoked

1. User runs `/skill-name` in Claude Code
2. Claude Code reads the skill's SKILL.md metadata (name, description, allowed-tools, etc.)
3. When invoked, skill runs via `uvx --from ~/.claude/skills/skill-name` with isolated environment
4. PyProject entry point (e.g., `research = "module:main"`) maps to the main function
5. Results are returned to Claude Code

**SKILL.md Front Matter (YAML):**
```yaml
---
name: skill-name
description: Brief description of what the skill does
allowed-tools:
  - Bash
  - Read
  - Write
---
```

## Adding New Skills

When creating a new skill:

1. Create directory structure under `agentskills/skill-name/`
2. Write SKILL.md with YAML metadata front matter (name, description)
3. Create pyproject.toml with package definition and entry point under `[project.scripts]`
4. Implement `src/skill-name/module.py` with `def main():` entry point
5. Accept command-line arguments via `argparse`
6. Output results to stdout (will be captured by Claude Code)
7. Use stderr for status/debug output

### Entry Point Pattern

```python
# src/my_skill/skill.py
#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Skill description")
    parser.add_argument("query", nargs="?", help="Main input")
    parser.add_argument("--option", help="Optional flag")
    args = parser.parse_args()

    # ... implementation ...

    # Output to stdout (captured by Claude Code)
    print(results)
    print("Debug info", file=sys.stderr)

if __name__ == "__main__":
    main()
```

### pyproject.toml Entry Point

```toml
[project.scripts]
skill-command = "module_name.skill:main"
```

This maps `uvx --from ~/.claude/skills/skill-name skill-command` to the `main()` function.

## Repository Structure

```
ThirdBrAIn-Tools/
├── agentskills/               # Container for all Claude Code skills
│   └── deep-research/         # Deep research skill
│       ├── src/
│       │   └── deep_research/
│       │       ├── research.py           # Entry point
│       │       ├── providers/
│       │       │   ├── openai.py
│       │       │   └── deepseek.py
│       │       └── shared/
│       │           ├── base.py           # Abstract provider
│       │           └── utils.py
│       ├── pyproject.toml
│       └── SKILL.md
├── AGENTS.md                  # This file (single source of truth)
├── CLAUDE.md                  # General guidance (references this file)
└── README.md
```

## Key Dependencies

- **httpx** - HTTP client for API calls (used by deep-research)
- **setuptools** - Python packaging
- **uv/uvx** - Fast Python package installer and script runner (required for skill execution)
- **pytest** - Testing (optional, for development)
- **black** - Code formatting (optional, for development)
- **ruff** - Linting (optional, for development)
