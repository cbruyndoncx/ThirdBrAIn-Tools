# AGENTS.md

This file documents all Claude Code skills and agents available in this repository. It is the single source of truth for agent/skill architecture and development.

## Project Overview

ThirdBrAIn-Tools is a repository for building reusable Claude Code skills. Currently available skills:

- **deep-research** - Unified deep research across multiple AI providers (OpenAI and DeepSeek)
- **google-keep** - Google Keep note management CLI (search, create, update, delete notes)
- **gamma** - Presentation generation via Gamma API
- **notion** - Comprehensive Notion API CLI (pages, databases, todos, blocks, search)
- **notebooklm-pdf2ppt** - Convert NotebookLM PDF exports to PowerPoint with vector graphics and watermark removal
- **paperbanana-lite** - Generate publication-quality academic diagrams and plots via multi-agent Gemini pipeline

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

**Tip:** Run any helper with `--help` to review all available flags before invoking it.

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

---

### google-keep

**Manage Google Keep notes from the command line.**

Search, create, update, and delete notes with full JSON output. Built as a single-file UV script with inline dependencies.

- **Skill Name:** `google-keep`
- **Location:** `agentskills/google-keep/`
- **Script:** `scripts/google_keep.py`
- **Files:**
  - `SKILL.md` - Full skill documentation and usage guide
  - `scripts/google_keep.py` - Single-file UV script implementation

**Quick Start:**
```bash
# Set credentials
export GOOGLE_EMAIL="your-email@gmail.com"
export GOOGLE_MASTER_TOKEN="your-master-token"

# Search notes
uv run scripts/google_keep.py find "shopping"

# Create a note
uv run scripts/google_keep.py create --title "New Note" --text "Content"

# Get, update, delete
uv run scripts/google_keep.py get <note_id>
uv run scripts/google_keep.py update <note_id> --title "Updated"
uv run scripts/google_keep.py delete <note_id>
```

**Command Reference:**

| Command | Purpose |
|---------|---------|
| `find [query]` | Search notes |
| `get <id>` | Get note by ID |
| `create --title --text` | Create new note |
| `update <id> --title/--text` | Update note |
| `delete <id>` | Delete (trash) note |
| `labels` | List all labels |

**Key Options:**

| Option | Purpose |
|--------|---------|
| `--env-file` | Custom .env file path |
| `--pinned` | Pin note / filter pinned |
| `--archived` | Archive note / include archived |
| `--color` | Set note color |
| `--limit N` | Limit search results |

See `agentskills/google-keep/SKILL.md` for complete documentation, token setup, and troubleshooting.

---

### notion

**Comprehensive Notion API CLI - pages, databases, todos, blocks, and search.**

Single-file standalone CLI with 100% Notion API coverage, smart caching, and path-based navigation. Built as a PEP 723 UV script.

- **Skill Name:** `notion`
- **Location:** `agentskills/notion/`
- **Script:** `scripts/notion.py`
- **Files:**
  - `SKILL.md` - Full skill documentation and command reference
  - `scripts/notion.py` - Single-file UV script (~2,260 lines)

**Quick Start:**
```bash
# Set API key
export NOTION_API_KEY="ntn_your_integration_token_here"

# Verify connection
uv run scripts/notion.py verify-connection

# List pages, search, add content
uv run scripts/notion.py list pages
uv run scripts/notion.py search "project"
uv run scripts/notion.py add page --title "Notes" --parent "Work"
```

**Command Reference:**

| Command | Purpose |
|---------|---------|
| `verify-connection` | Test API connectivity |
| `check-config` | Show environment configuration |
| `search "query"` | Search Notion content |
| `list pages/databases` | List all pages or databases |
| `add page/database/todo` | Create pages, databases, or todos |
| `get page/database/block` | Retrieve by name/path or ID |
| `update page/database/block` | Update properties or content |
| `delete page/block` | Archive pages or delete blocks |
| `move page` | Move page to new parent |
| `query database` | Query with filters and sorts |
| `todos search` | Search todos with filter shortcuts |
| `blocks add/list/delete` | Manage 30+ block types |
| `blocks subtasks` | Add/list/check subtasks |
| `refresh-cache` | Refresh name-to-ID cache |

**Key Features:**

| Feature | Description |
|---------|-------------|
| Path navigation | Use `"Parent/Child"` names instead of UUIDs |
| Smart caching | Auto-caching with 24h refresh at `~/.cache/notion-cli/` |
| Database templates | `--template tasks\|notes\|contacts` |
| Filter shortcuts | `--status`, `--priority`, `--due-before` |
| JSON output | All commands return JSON |

See `agentskills/notion/SKILL.md` for complete documentation and command examples.

---

### notebooklm-pdf2ppt

**Convert NotebookLM PDF slide exports to PowerPoint with vector graphics quality.**

Single-file UV script using a PDF → SVG → EMF → PPTX pipeline. Preserves vector graphics, removes NotebookLM watermarks, supports batch conversion and parallel processing.

- **Skill Name:** `notebooklm-pdf2ppt`
- **Location:** `agentskills/notebooklm-pdf2ppt/`
- **Script:** `scripts/pdf2ppt.py`
- **Files:**
  - `SKILL.md` - Full skill documentation and usage guide
  - `scripts/pdf2ppt.py` - Single-file UV script (PEP 723 inline dependencies)

**System Dependencies:** Requires `pdf2svg` and `inkscape` installed on the system.

**Quick Start:**
```bash
# Check system dependencies
uv run scripts/pdf2ppt.py --check-deps

# Install if needed (Ubuntu/Debian)
sudo apt install pdf2svg inkscape

# Convert with watermark removal
uv run scripts/pdf2ppt.py input.pdf --remove-watermark --force

# Batch convert
for f in *.pdf; do uv run scripts/pdf2ppt.py "$f" --rw --force -j 4; done
```

**Command Reference:**

| Command | Purpose |
|---------|---------|
| `--check-deps` | Check system dependencies (JSON output) |
| `--remove-watermark` / `--rw` | Remove NotebookLM watermark |
| `--pages 1-5,7` | Convert specific pages |
| `--parallel 4` / `-j 4` | Parallel SVG→EMF workers |
| `--force` / `-f` | Overwrite existing output |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic error |
| 2 | Missing system dependencies |
| 101 | PDF→SVG failure |
| 102 | SVG→EMF failure |

See `agentskills/notebooklm-pdf2ppt/SKILL.md` for complete documentation.

---

### paperbanana-lite

**Generate publication-quality academic diagrams and statistical plots from text.**

Multi-agent Gemini pipeline (Retriever → Planner → Stylist → Visualizer ↔ Critic) distilled into a single-file script. Supports methodology diagrams via image generation and statistical plots via matplotlib code execution.

- **Skill Name:** `paperbanana-lite`
- **Location:** `agentskills/paperbanana-lite/`
- **Script:** `scripts/paperbanana_lite.py`
- **Files:**
  - `SKILL.md` - Full skill documentation and usage guide
  - `scripts/paperbanana_lite.py` - Single-file pipeline script

**Quick Start:**
```bash
# Set API key
export GEMINI_API_KEY="your-key"

# Install dependencies
pip install google-genai pillow tenacity

# Generate a methodology diagram
python scripts/paperbanana_lite.py generate \
  --input methodology.txt \
  --caption "Overview of our architecture" \
  --reference-dir path/to/references

# Generate a statistical plot
python scripts/paperbanana_lite.py plot \
  --data results.json \
  --intent "Bar chart comparing accuracy" \
  --reference-dir path/to/references
```

**Command Reference:**

| Command | Purpose |
|---------|---------|
| `generate --input FILE --caption TEXT` | Generate methodology diagram |
| `plot --data FILE --intent TEXT` | Generate statistical plot |

**Key Options:**

| Option | Purpose | Default |
|--------|---------|---------|
| `--reference-dir PATH` | Reference set directory | `data/reference_sets` |
| `--iterations N` | Refinement iterations | 3 |
| `--output-dir PATH` | Output directory | `outputs` |

See `agentskills/paperbanana-lite/SKILL.md` for complete documentation.

---

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
│   ├── deep-research/         # Deep research skill
│   │   ├── src/
│   │   │   └── deep_research/
│   │   │       ├── research.py           # Entry point
│   │   │       ├── providers/
│   │   │       │   ├── openai.py
│   │   │       │   └── deepseek.py
│   │   │       └── shared/
│   │   │           ├── base.py           # Abstract provider
│   │   │           └── utils.py
│   │   ├── pyproject.toml
│   │   └── SKILL.md
│   ├── google-keep/           # Google Keep skill
│   │   └── SKILL.md
│   ├── notion/                # Notion API CLI skill
│   │   └── SKILL.md
│   ├── notebooklm-pdf2ppt/   # NotebookLM PDF to PowerPoint skill
│   │   └── SKILL.md
│   └── paperbanana-lite/     # Academic diagram/plot generation skill
│       └── SKILL.md
├── scripts/                   # Standalone UV scripts
│   ├── google_keep.py         # Google Keep CLI (single-file UV script)
│   ├── notion.py              # Notion API CLI (single-file UV script)
│   ├── pdf2ppt.py             # NotebookLM PDF to PPTX (single-file UV script)
│   ├── paperbanana_lite.py    # Academic illustration pipeline (single-file)
│   ├── research.py
│   ├── generate_gamma_presentation.py
│   └── get_gamma_assets.py
├── AGENTS.md                  # This file (single source of truth)
├── CLAUDE.md                  # General guidance (references this file)
└── README.md
```

## Key Dependencies

- **httpx** - HTTP client for API calls (used by deep-research, notion)
- **click** - CLI framework (used by notion)
- **structlog** - Structured logging (used by notion)
- **google-genai** - Google Gemini SDK (used by paperbanana-lite)
- **tenacity** - Retry with exponential backoff (used by paperbanana-lite)
- **gkeepapi** - Google Keep API client (used by google-keep)
- **python-dotenv** - Environment variable loading
- **setuptools** - Python packaging
- **uv/uvx** - Fast Python package installer and script runner (required for skill execution)
- **pytest** - Testing (optional, for development)
- **black** - Code formatting (optional, for development)
- **ruff** - Linting (optional, for development)
