---
name: nano-banana-images
description: Nano Banana Pro (Gemini 3 Pro image) workflow for Claude Code. Trigger when users ask about Nano Banana, Gemini 3 Pro image generation, or building style libraries/visual assets with Claude Code.
---

# Nano Banana Pro Image Generation

## When to use this skill

- When a user asks to generate or refine an image with Nano Banana Pro / Gemini 3 Pro
- When they want to iterate on a prior render, switch aspect ratio/resolution, or explore natural-language prompts
- When they mention building a style library, pulling from past renders, or extracting a look from an existing image

## Authentication

Uses `GEMINI_API_KEY` from the runtime environment. No `.env` files needed.

## Available Models

List models: `uv run scripts/nano_banana.py models`

### Gemini Models (Multi-turn, Conversational)

| Model | Best For |
|-------|----------|
| `gemini-3-pro-image-preview` | **Default**. Illustrations, conceptual art, creative work. Supports multi-turn sessions. |
| `gemini-3-flash-preview` | Faster generation, good quality. Lighter than Pro. |
| `gemini-2.5-flash-image` | Fastest Gemini. Quick drafts, iteration. |

### Imagen Models (Single-shot, Photorealistic)

| Model | Best For |
|-------|----------|
| `imagen-4.0-generate-001` | **Photorealistic** images, product shots, realistic scenes. |
| `imagen-4.0-ultra-generate-001` | Highest quality photorealism, fine details. Slower. |
| `imagen-4.0-fast-generate-001` | Quick photorealistic drafts. Fastest Imagen. |

### Quick Reference

| Task | Model |
|------|-------|
| Illustrations, conceptual art | `gemini-3-pro-image-preview` (default) |
| Iterative refinement | Gemini models (multi-turn support) |
| Photorealistic photographs | `imagen-4.0-generate-001` |
| Product photography | `imagen-4.0-ultra-generate-001` |
| Fast exploration | `gemini-2.5-flash-image` or `imagen-4.0-fast-generate-001` |

### CLI Model Selection

```bash
# Default (gemini-3-pro-image-preview)
uv run scripts/nano_banana.py generate "prompt"

# Specific model
uv run scripts/nano_banana.py generate "prompt" --model imagen-4.0-generate-001
```

## Skill Structure

```
nano-banana-images/
├── SKILL.md                    # This file
├── references/
│   ├── nano_banana_basics.md   # API functions, aspect ratios, resolutions
│   ├── golden_rules.md         # Four Golden Rules of prompting
│   └── style_library.md        # Style library usage and management
├── scripts/
│   └── nano_banana.py          # Single-file module (PEP 723, uv-compatible)
├── style-library/
│   ├── style-library.html      # Interactive browser UI
│   └── thumbnails/             # Style preview images
└── outputs/                    # Generated images land here
```

## High-level Flow

### 1. Gather Intent
Ask for:
- Subject, mood, lighting
- Context (for what product, platform, narrative)
- Where PNG will be used (presentation, hero image, story card)

This determines aspect ratio and resolution.

### 2. Generate with the Module

```python
import sys
sys.path.insert(0, '[skill_path]/scripts')
import nano_banana as nb

nb.generate("Your natural language prompt", aspect_ratio="1:1", resolution="1K")
```

Refer to `references/nano_banana_basics.md` for:
- Default aspect ratio: `1:1`
- Resolution tiers: `1K` (drafts), `2K` (finals), `4K` (prints)

Continue the existing session unless user asks to start fresh with `nb.new_session()`.

### 3. Surface Outputs
- PNGs save to `outputs/` folder
- Ask user to open in Finder/Explorer (CLI can't display images)
- Use `nb.session_info()` to recap prior turns
- Use `nb.revert()` to undo bad iterations

### 4. Improve the Prompt
When wording needs refinement, consult `references/golden_rules.md`:

1. **Edit, don't re-roll** - iterate on what's working
2. **Use natural language** - talk to it like a designer
3. **Be specific** - layer in details
4. **Provide context** - tell it the "why"

Generate comparison pairs when teaching the rules.

### 5. Leverage the Style Library
If user wants to reuse a saved aesthetic:

1. Consult `references/style_library.md`
2. Run `python scripts/get_style.py <id>` to fetch prompt
3. Combine with current subject
4. Call `generate()` with merged prompt

## Style Library & Extraction

### Using Saved Styles
Style library lives in `style-library/style-library.html`. Open in browser to browse.

```bash
uv run scripts/nano_banana.py styles 3        # Get style #3
uv run scripts/nano_banana.py styles --list   # List all styles
```

### Saving New Styles
When user says "save this style":
1. Copy final PNG to `style-library/thumbnails/` (kebab-case name)
2. Update `styles` array in `style-library.html`
3. Use canonical categories/tags from `references/style_library.md`

### Extracting Styles from Images

```python
# Get verbose style description
result = nb.extract_style("path/to/image.png")

# Or save to markdown
nb.extract_and_save("path/to/image.png")
```

Feed extracted text into `nb.generate()` to recreate the aesthetic, then add to library.

## Workflow Reminders

- **Encourage iteration:** Session remembers full conversation - refining gives better continuity than restarting
- **CLI limitation:** Can't display images - always point to `outputs/` folder with exact filenames
- **Opening images:** Offer `open [path]` (Mac) or `start [path]` (Windows)
- **File naming:** Use kebab-case for thumbnails and outputs
