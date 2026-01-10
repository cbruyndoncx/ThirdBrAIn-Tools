# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ThirdBrAIn-Tools is a repository for building reusable Claude Code skills. This repository contains utilities, frameworks, and example implementations for creating custom Claude Code agent skills.

**For detailed information about available skills, their architecture, and development patterns, see [AGENTS.md](./AGENTS.md) - this is the single source of truth for all agents/skills.**

## Development Commands

### Setup
```bash
# Install uv (required for skill development)
pip install uv

# Set API keys in ~/.bashrc or ~/.zshrc (if using skills that need them)
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
```

### Running Skills
```bash
# Use a skill in Claude Code
/skill-name "query" --option value

# Or run directly via uvx
uvx --from ~/.claude/skills/skill-name command "query" --option value
```

### Testing & Linting (for individual skills)
```bash
cd agentskills/skill-name

# Run tests
pytest

# Format code
black src/

# Lint
ruff check src/
ruff check --fix src/
```

## Repository Structure

```
ThirdBrAIn-Tools/
├── agentskills/           # Container for all Claude Code skills
│   └── deep-research/     # Example: Deep research skill
└── AGENTS.md              # Single source of truth for skills/agents
```

## Documentation

- **[AGENTS.md](./AGENTS.md)** - Complete skill documentation, architecture patterns, and development guide
- **agentskills/[skill-name]/SKILL.md** - User documentation for individual skills
