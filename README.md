# ThirdBrAIn-Tools

Collection of reusable Claude Code skills with unified Python entry points.

## Quick Start

### Install
```bash
pip install uv
```

### Use from GitHub
```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools research "quantum computing"
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation --input-text "Q4 results"
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools nanobanana \  
  --prompt "ultra wide shot of a futuristic boardroom" \
  --size 1344x768

```

### Local development
```bash
python -m scripts.research "quantum computing" --provider deepseek
python -m scripts.generate_gamma_presentation --input-text "Q4 results"
python -m scripts.get_gamma_assets --generation-id abc123
```

## Available Skills

- **research** - Deep research with OpenAI and DeepSeek
  - See `agentskills/deep-research/SKILL.md` for full docs
- **gamma** - Generate presentations, documents, social media posts, and websites with the Gamma API
  - Entry points: `generate_gamma_presentation`, `get_gamma_assets`
  - See `agentskills/gamma/SKILL.md` for full docs
- **nanobanana** – Image generation and editing with Gemini Nano Banana  
  - See `agentskills/nanobanana/SKILL.md` for full docs
  
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
