---
name: nanobanana
description: Generate or edit images using Google's Gemini Nano Banana (image) models.
entry: nanobanana
category: ai-image
---

# NanoBanana Skill

Generate or edit images using Gemini image models via a single-file `uv` script.

## Usage

**Via uvx from GitHub:**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "isometric cyberpunk office" --size 1024x1024
```

**Alternative (direct script):**
```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/nanobanana.py --prompt "your prompt"
```

## Examples

### Generate new image

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana \
  --prompt "isometric cyberpunk office, neon lights" \
  --size 1024x1024
```

### Edit existing image

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana \
  --prompt "add a glowing holographic dashboard" \
  --input ./input.png \
  --output ./edited.png
```

## Options

| Option | Purpose |
|--------|---------|
| `--prompt` | Text description of desired image (required) |
| `--input` | Input image(s) for editing |
| `--output` | Output PNG path (default: nanobanana-<id>.png) |
| `--model` | `gemini-3-pro-image-preview` (default) or `gemini-2.5-flash-image` |
| `--size` | Resolution preset: `768x1344`, `1024x1024`, `1344x768`, etc. |
| `--resolution` | Scale factor: `1K`, `2K`, or `4K` |

## Environment Variables

```bash
export GEMINI_API_KEY="your-key"
```

Or create `~/.nanobanana.env` or `.env` with:
```
GEMINI_API_KEY=your-key
```

---

## Understanding `uvx --from`

The `uvx --from` syntax provides flexible remote execution:

```bash
# From GitHub (main branch)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "..."

# From specific branch
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@develop[nanobanana]" nanobanana --prompt "..."

# From specific tag/version
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@v1.0.0[nanobanana]" nanobanana --prompt "..."
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
