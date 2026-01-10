# Claude Code Skills

This directory contains reusable Claude Code skills.

## Available Skills

### deep-research
**Conduct deep research with OpenAI and DeepSeek reasoning models using uvx.**

Unified deep research across multiple AI providers using uvx. Create research requests, auto-poll for completion, and return formatted markdown reports.

- **Skill Name:** `deep-research`
- **Files:**
  - `deep-research/SKILL.md` - Full skill documentation and usage guide
  - `deep-research/src/` - Python implementation
  - `deep-research/pyproject.toml` - Dependencies and entry point

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

### 3. Use in Claude Code
```
/deep-research "What is quantum computing?" --provider deepseek
```

Or run directly:
```bash
uvx --from ~/.claude/skills/deep-research research "What is quantum computing?" --provider deepseek
```

## Installation

Copy the skill to your Claude Code skills folder:
```bash
cp -r deep-research ~/.claude/skills/
```

The skill will be automatically available in Claude Code.

## How It Works

When you invoke the skill, it uses uvx to:
1. Read `pyproject.toml` from the skill directory
2. Install dependencies in an isolated environment
3. Run the research script with your arguments
4. Return formatted markdown reports

## Requirements

- **uvx** - Install with: `pip install uv`
- **Python 3.10+** - Required for the research script
- **API Keys** - Set `OPENAI_API_KEY` and/or `DEEPSEEK_API_KEY`
- **Internet connection** - For API calls to OpenAI or DeepSeek

## Learn More

See [deep-research/SKILL.md](deep-research/SKILL.md) for:
- Complete command reference
- Provider comparison (OpenAI vs DeepSeek)
- Adaptive polling strategies
- Troubleshooting guide
- Workflow examples
