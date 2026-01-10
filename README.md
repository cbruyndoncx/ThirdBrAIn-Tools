# ThirdBrAIn-Tools

Collection of reusable Claude Code skills with unified Python entry points.

## Quick Start

### Install
```bash
pip install uv
```

### Use from GitHub
```bash
uvx --from https://github.com/yourname/ThirdBrAIn-Tools research "quantum computing"
```

### Local development
```bash
python -m scripts.research "quantum computing" --provider deepseek
```

## Available Skills

- **research** - Deep research with OpenAI and DeepSeek
  - See `agentskills/deep-research/SKILL.md` for full docs

## Structure

```
scripts/          - All skill implementations
agentskills/      - Skill metadata & documentation
pyproject.toml    - Single entry point configuration
```

## Adding New Skills

1. Create `agentskills/skill-name/SKILL.md` with metadata
2. Add `scripts/skill_name.py` with a `main()` function
3. Update `pyproject.toml`:
   ```toml
   [project.scripts]
   skill-name = "scripts.skill_name:main"
   ```

See [AGENTS.md](./AGENTS.md) for detailed development guide.
