# ThirdBrAIn-Tools Scripts

Helper scripts for AI-powered research, presentations, note management, and image generation.

## Quick Start (Remote Execution)

All scripts can be run directly from GitHub - no local installation required. Just have `uv` installed.

```bash
# Research with OpenAI
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "What are the latest AI breakthroughs?" --provider openai

# Generate Gamma presentation
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-file content.md

# Manage Google Keep notes
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep find "shopping list"

# Generate images with Gemini
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "isometric cyberpunk office"
```

**Tip:** Add `--help` to any command to see all available options.

---

## Understanding `uvx --from`

The `uvx --from` syntax provides flexible remote execution. Here's how it works:

### Basic Format

```bash
uvx --from "PACKAGE_SOURCE[EXTRAS]" COMMAND [ARGS]
```

| Component | Description |
|-----------|-------------|
| `uvx` | UV's tool runner (like `npx` for Python) |
| `--from` | Specifies where to get the package |
| `PACKAGE_SOURCE` | Git URL, PyPI package, or local path |
| `[EXTRAS]` | Optional dependency groups to install |
| `COMMAND` | The script/command to run |
| `[ARGS]` | Arguments passed to the command |

### Package Sources

```bash
# From GitHub (main branch)
uvx --from "git+https://github.com/user/repo" command

# From GitHub (specific branch)
uvx --from "git+https://github.com/user/repo@develop" command

# From GitHub (specific tag/version)
uvx --from "git+https://github.com/user/repo@v1.0.0" command

# From GitHub (specific commit)
uvx --from "git+https://github.com/user/repo@abc123def" command

# From PyPI
uvx --from "package-name" command

# From PyPI (specific version)
uvx --from "package-name==1.2.3" command
```

### Optional Extras (Dependency Groups)

Extras let you install only the dependencies you need:

```bash
# Install with "research" extras (includes httpx)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "query"

# Install with "keep" extras (includes gkeepapi)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep find "notes"

# Install with multiple extras
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research,gamma]" research "query"

# Install all extras
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[all]" research "query"
```

### Available Extras for ThirdBrAIn-Tools

| Extra | Dependencies | Commands |
|-------|--------------|----------|
| `research` | `httpx` | `research`, `poll_research`, `extract_json` |
| `gamma` | (base only) | `generate_gamma_presentation`, `get_gamma_assets` |
| `keep` | `gkeepapi` | `google_keep` |
| `nanobanana` | `google-generativeai`, `pillow` | `nanobanana` |
| `all` | All dependencies | All commands |

### Documentation

- [uv Tools Guide](https://docs.astral.sh/uv/guides/tools/) - Official `uvx` documentation
- [uv Git Dependencies](https://docs.astral.sh/uv/pip/packages/#git) - Git URL formats

---

## Scripts Overview

### Research Scripts

#### `research` - Unified Deep Research

Primary script for AI-powered research with OpenAI and DeepSeek.

```bash
# OpenAI deep research
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "What is quantum computing?" --provider openai

# DeepSeek reasoning
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "Explain transformers" --provider deepseek

# From file with custom output
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research --query-file query.md --output report.md --provider openai
```

**Features:**
- Supports OpenAI and DeepSeek providers
- Adaptive polling intervals (10s → 30s → 1m → 5m)
- Auto-saves both raw JSON and extracted markdown
- YAML frontmatter with metadata

#### `poll_research` - Reconnect to Research Jobs

Reconnect to long-running research jobs and retrieve results.

```bash
# Poll and retrieve results
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research resp_abc123

# Check status only
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research resp_abc123 --check-only

# Custom timeout (1 hour)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research resp_abc123 --timeout 3600
```

#### `extract_json` - JSON Extraction Helper

Extract markdown from OpenAI's nested JSON response.

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" extract_json input.json output.md
```

### Gamma Scripts

#### `generate_gamma_presentation` - Create Presentations

Generate presentations, documents, and more using Gamma API.

```bash
# From text
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-text "Your content here"

# From file
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-file content.md --format presentation
```

#### `get_gamma_assets` - Download Exports

Retrieve and download presentation exports (PDF, PPTX).

```bash
# Get URLs
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" get_gamma_assets --generation-id abc123

# Download files
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" get_gamma_assets --generation-id abc123 --download --output-dir ./exports
```

### Google Keep

#### `google_keep` - Manage Notes

CLI for managing Google Keep notes.

```bash
# Search notes
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep find "shopping list"

# Create note
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep create --title "New Note" --text "Content here"

# Update note
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep update <note_id> --title "Updated Title"

# Delete note
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep delete <note_id>

# List labels
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep labels
```

### Image Generation

#### `nanobanana` - Gemini Image Generation

Generate and edit images with Google Gemini.

```bash
# Generate image
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "isometric cyberpunk office" --size 1024x1024

# Edit existing image
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "add a cat" --input photo.jpg --output edited.png
```

---

## Environment Variables

Set these in your shell or `.env` file:

```bash
# Research
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"

# Gamma
export GAMMA_API_KEY="your-key"

# Google Keep
export GOOGLE_EMAIL="your-email"
export GOOGLE_MASTER_TOKEN="your-token"

# NanoBanana
export GEMINI_API_KEY="your-key"
```

**Loading from custom .env file:**

All scripts support `--env-file /path/to/.env` to load credentials from a specific location.

---

## Alternative: Direct Script Execution

If you prefer running scripts directly (without package installation):

```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/research.py "query" --provider openai
```

This method uses PEP 723 inline metadata - dependencies are resolved automatically.

---

## Common Workflows

### Workflow 1: Quick Research (Wait for Completion)

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research \
  --query-file query.md \
  --output result.md \
  --provider openai \
  --verbose
```

### Workflow 2: Submit and Reconnect Later

**Step 1: Submit**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research --query-file query.md --provider openai
# Note the Request ID displayed
```

**Step 2: Check status (anytime)**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research resp_abc123 --check-only
```

**Step 3: Retrieve results**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" poll_research resp_abc123 --output report.md
```

### Workflow 3: Research to Presentation Pipeline

```bash
# 1. Research a topic
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[research]" research "AI trends 2026" --provider openai --output research.md

# 2. Generate presentation from research
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-file research.md --format presentation

# 3. Download the presentation
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" get_gamma_assets --generation-id <ID> --download
```

---

## Output Files

**Filename format:**
- `{provider}_{model}_{timestamp}.md` - Markdown report with YAML frontmatter
- `{provider}_{model}_{timestamp}-raw.json` - Raw JSON response
- Timestamp format: `YYMMDD_HHMM` (e.g., `260111_1430` = Jan 11, 2026 at 2:30 PM)

**Frontmatter structure:**
```yaml
---
provider: openai
model: o4-mini-deep-research
request_id: resp_abc123...
timestamp: 260111_1430
---
```

---

## Troubleshooting

**Common issues:**

| Issue | Solution |
|-------|----------|
| Missing API key | Set environment variable or use `--env-file` |
| Timeout | Increase with `--timeout` or run `poll_research` again |
| Lost request ID | Check `-raw.json` files for `"id"` field |
| cmd.exe errors in WSL | Use full paths (`/usr/bin/python3`) |

---

## See Also

- [AGENTS.md](../AGENTS.md) - Complete skill documentation
- [uv Documentation](https://docs.astral.sh/uv/) - Package manager docs
