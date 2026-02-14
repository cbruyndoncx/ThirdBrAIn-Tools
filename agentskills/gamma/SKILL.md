---
name: gamma
description: Generate presentations, documents, social media posts, and websites using the Gamma API. Create executive presentations with presets, generate detailed reports as PDF, or customize fully. Use when creating presentations, reports, or visual content programmatically.
---

# Gamma Presentation Generator

Generate presentations, documents, social media posts, and websites using the Gamma API. This skill provides two core scripts for maximum flexibility:

- **generate_gamma_presentation** - Full customization of any generation
- **get_gamma_assets** - Retrieve and download exports

## Usage

**Via uvx from GitHub:**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-file content.md
```

**Alternative (direct script):**
```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/generate_gamma_presentation.py --input-file content.md
```

## Quick Start

### Generate a Basic Presentation from File

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --format presentation \
  --num-cards 10
```

### Generate Executive Presentation as PowerPoint (PPTX)

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation \
  --input-file 99-TMP/INPUT/executive_summary.md \
  --format presentation \
  --text-mode condense \
  --num-cards 8 \
  --export-as pptx \
  --card-split inputTextBreaks \
  --text-amount medium \
  --text-tone "professional and confident" \
  --text-audience "executives and senior leadership" \
  --image-source aiGenerated \
  --image-style photorealistic \
  --card-dimensions "16x9"
```

### Generate Executive Presentation as PDF Report

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation \
  --input-file 99-TMP/INPUT/executive_summary.md \
  --format document \
  --text-mode preserve \
  --export-as pdf \
  --card-split auto \
  --text-amount detailed \
  --text-tone "professional and confident" \
  --text-audience "executives and senior leadership" \
  --image-source aiGenerated \
  --image-style photorealistic \
  --card-dimensions a4
```

### Retrieve Assets

```bash
# Get URLs
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" get_gamma_assets --generation-id abc123

# Download files to output directory
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" get_gamma_assets \
  --generation-id abc123 \
  --download \
  --output-dir 99-TMP/OUTPUT
```

---

## Core Scripts

### generate_gamma_presentation

Generate a new presentation with full customization options.

**Inputs:** All parameters are optional except one of `--input-text` or `--input-file` is required

**Common Parameters:**
- `--input-text` - Content for the presentation (supports markdown and image URLs)
- `--input-file` - Path to a file containing the presentation content (alternative to --input-text)
- `--format` - `presentation` (default), `document`, `social`, or `webpage`
- `--text-mode` - `generate` (default), `condense`, or `preserve`
- `--num-cards` - Number of slides/cards (default: 10)
- `--export-as` - `pdf` or `pptx` for direct export

**Customization Parameters:**
- `--text-amount` - `brief`, `medium`, `detailed`, `extensive`
- `--text-tone` - Voice/style (e.g., "professional and confident")
- `--text-audience` - Target audience (e.g., "executives")
- `--text-language` - Language code (e.g., "en", "es", "fr")
- `--image-source` - Image source (see options below)
- `--image-model` - AI model for images (e.g., "dall-e-3")
- `--image-style` - Visual style (e.g., "photorealistic", "minimalist")
- `--card-dimensions` - Format-specific aspect ratio

**Advanced Parameters:**
- `--card-split` - `auto` or `inputTextBreaks`
- `--theme-id` - Theme ID to apply
- `--additional-instructions` - Custom generation instructions (text)
- `--additional-instructions-file` - Path to file with custom instructions
- `--env-file` - Load credentials from specific .env file

**Output:** JSON with `url`, `generation_id`, and `error` fields

### get_gamma_assets

Retrieve presentation exports and optionally download them.

**Inputs:**
- `--generation-id` (required) - ID from generate_gamma_presentation
- `--download` - Flag to download files locally
- `--output-dir` - Download destination (default: 99-TMP/OUTPUT)
- `--env-file` - Load credentials from specific .env file

**Output:** JSON with `pdf`, `pptx` URLs and optional local paths

---

## Image Source Options

- `aiGenerated` - AI-generated images (DALL-E)
- `pictographic` - Icon/illustration style
- `unsplash` - Free stock photos
- `giphy` - Animated GIFs
- `webAllImages` - Any web images
- `webFreeToUse` - Creative Commons free
- `webFreeToUseCommercially` - Commercial use licensed
- `placeholder` - Gray placeholder boxes
- `noImages` - Text only

---

## Card Dimensions by Format

**Presentation:**
- `fluid` - Responsive
- `16x9` - Widescreen (standard)
- `4x3` - Standard aspect ratio

**Document:**
- `fluid` - Responsive
- `pageless` - Continuous scroll
- `letter` - US Letter (8.5" × 11")
- `a4` - A4 (210 × 297 mm)

**Social:**
- `1x1` - Square (Instagram)
- `4x5` - Portrait (Stories)
- `9x16` - Tall portrait (TikTok/Reels)

---

## Environment Setup

Required environment variable:
```bash
export GAMMA_API_KEY=sk-gamma-xxxxxxxx
```

Available to: Pro, Ultra, Teams, and Business plan subscribers.

---

## Understanding `uvx --from`

The `uvx --from` syntax provides flexible remote execution:

```bash
# From GitHub (main branch)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation ...

# From specific branch
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@develop[gamma]" generate_gamma_presentation ...

# From specific tag/version
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@v1.0.0[gamma]" generate_gamma_presentation ...
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

## Troubleshooting

### "Either --input-text or --input-file is required"
Provide one of:
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-text "Content here" ...
# OR
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[gamma]" generate_gamma_presentation --input-file content.md ...
```

### "GAMMA_API_KEY environment variable not set"
Set your API key:
```bash
export GAMMA_API_KEY=sk-gamma-xxxxxxxx
```

### Generation returns no URL
Use `get_gamma_assets` with the `generation_id` to check status and retrieve exports.

---

## Support

- Official Docs: https://developers.gamma.app/docs
- API Reference: https://developers.gamma.app/reference/
- Complete API Reference: [references/GAMMA_API_REFERENCE.md](references/GAMMA_API_REFERENCE.md)
