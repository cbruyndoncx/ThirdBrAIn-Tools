# Nano Banana Pro Image Basics

## Overview

Nano Banana Pro uses Google's image generation models accessible via API. Using the API directly (vs Google's consumer apps) is slightly more permissive and allows Claude Code to act as your creative partner.

## Available Models

List models with: `uv run nano_banana.py models`

### Gemini Models (Conversational, Multi-turn)

| Model | Best For | Notes |
|-------|----------|-------|
| `gemini-3-pro-image-preview` | **Default**. High-quality illustrations, conceptual art, creative work | Supports multi-turn sessions, remembers context |
| `gemini-3-flash-preview` | Faster generation, good quality | Lighter weight than Pro |
| `gemini-2.5-flash-image` | Quick drafts, iteration | Fastest Gemini option |
| `gemini-3-pro-preview` | Text + image understanding | General multimodal tasks |

### Imagen Models (Single-shot, Photorealistic)

| Model | Best For | Notes |
|-------|----------|-------|
| `imagen-4.0-generate-001` | **Photorealistic** images, product shots, realistic scenes | No multi-turn, single prompt per image |
| `imagen-4.0-ultra-generate-001` | Highest quality photorealism, fine details | Slower, best for final outputs |
| `imagen-4.0-fast-generate-001` | Quick photorealistic drafts | Fastest Imagen, good for iteration |

### When to Use Which

| Task | Recommended Model |
|------|-------------------|
| Illustrations, conceptual art | `gemini-3-pro-image-preview` (default) |
| Iterative refinement | `gemini-3-pro-image-preview` or `gemini-3-flash-preview` |
| Photorealistic photographs | `imagen-4.0-generate-001` |
| Product photography | `imagen-4.0-ultra-generate-001` |
| Quick photo drafts | `imagen-4.0-fast-generate-001` |
| Fast exploration | `gemini-2.5-flash-image` |

### CLI Usage

```bash
# Default model (gemini-3-pro-image-preview)
uv run nano_banana.py generate "prompt here"

# Specific model
uv run nano_banana.py generate "prompt here" --model imagen-4.0-generate-001

# List all available models
uv run nano_banana.py models
```

## Scripts & Paths

Scripts are located in the skill's `scripts/` folder:
- `scripts/image_gen.py` - Main generation module
- `scripts/style_extract.py` - Style extraction from images
- `scripts/get_style.py` - Fetch styles from library by ID

Outputs save to `outputs/` folder. Always point the user there to view PNGs via Finder/Explorer (terminal preview is disabled).

Ensure `GEMINI_API_KEY` is set in `.env` before generating.

## Core Functions

### generate()

Main function for creating images.

```python
from image_gen import generate

generate(
    prompt="Your description",
    reference_images=None,      # Optional: list of image paths for style/subject reference
    aspect_ratio="1:1",         # Shape of output
    resolution="1K"             # Size/quality tier
)
```

Keeps the Gemini 3 Pro session alive so the model remembers earlier turns.

### new_session()

Clears the stored session and starts fresh. Use when:
- User wants to pivot to a totally different concept
- Restarting after many iterations
- Generating variants (call before each for fresh results)

```python
new_session()
```

### session_info()

Returns current turn count plus saved output paths. Use to recap what has been generated.

```python
session_info()
```

### revert()

Roll back the last N turns and delete corresponding outputs. Useful when iterations went off-track.

```python
revert(turns=1)
```

## Aspect Ratios

| Ratio | Shape | Use Case |
|-------|-------|----------|
| `1:1` | Square | Instagram posts, profile pics, **default** |
| `16:9` | Landscape | Presentations, YouTube thumbnails, desktop wallpapers |
| `9:16` | Portrait | Instagram/TikTok stories, phone wallpapers |
| `4:5` | Tall rectangle | Instagram feed posts |
| `3:2` | Classic photo | 35mm film ratio |

**Default:** Use `1:1` unless user specifies otherwise.

## Resolution Tiers

| Tier | Pixels | Time | Cost | Use Case |
|------|--------|------|------|----------|
| `1K` | 1024px | ~20s | Base | Drafts, iteration, exploration |
| `2K` | 2048px | ~30s | Same as 1K | Final outputs, polished work |
| `4K` | 4096px | ~45s | Higher | Print-quality, large format |

**Default:** Use `1K` for fast iteration. Upgrade to `2K` for finals.

## Workflow

1. Ask user for subject, mood, context, and where the image will be used
2. Call `generate()` with natural-language input and desired `aspect_ratio`/`resolution`
3. User inspects PNG in `outputs/`, then iterate by continuing session
4. Use `session_info()` to recap and `revert()` to undo if needed
5. Only call `new_session()` when starting completely different concept

## Terminal Limitations

Cannot display images directly. Always:
1. Tell user to check `outputs/` folder
2. Provide exact filename
3. Offer to open: `open [path]` (Mac) or `start [path]` (Windows)
