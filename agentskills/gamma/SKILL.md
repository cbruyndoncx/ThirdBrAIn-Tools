---
name: gamma
description: Generate presentations, documents, social media posts, and websites using the Gamma API. Create executive presentations with presets, generate detailed reports as PDF, or customize fully. Use when creating presentations, reports, or visual content programmatically.
---

# Gamma Presentation Generator

Generate presentations, documents, social media posts, and websites using the Gamma API. This skill provides two core scripts for maximum flexibility:

- **generate_gamma_presentation.py** - Full customization of any generation
- **get_gamma_assets.py** - Retrieve and download exports

## Usage

**In Claude Code:**
```bash
/gamma "Generate a presentation about Q4 results"
```

**Via uvx from GitHub:**
```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation [OPTIONS]
```

**Local development:**
```bash
python -m scripts.generate_gamma_presentation [OPTIONS]
python -m scripts.get_gamma_assets [OPTIONS]
```

## Quick Start

### Generate a Basic Presentation from File

```bash
# Generate presentation from input file
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --format presentation \
  --num-cards 10
```

### Generate Executive Presentation as PowerPoint (PPTX)

```bash
# Generate as PPTX presentation from input file
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
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
# Generate as PDF document from same input file
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
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

### Generate Both PPTX and PDF from Same Content

```bash
# Generate PPTX
PPTX_RESPONSE=$(uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/executive_summary.md \
  --format presentation \
  --text-mode condense \
  --export-as pptx \
  --card-split inputTextBreaks \
  --text-amount medium \
  --text-tone "professional and confident" \
  --text-audience "executives and senior leadership" \
  --image-source aiGenerated \
  --image-style photorealistic \
  --card-dimensions "16x9")

PPTX_ID=$(echo $PPTX_RESPONSE | jq -r '.generation_id')

# Generate PDF
PDF_RESPONSE=$(uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
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
  --card-dimensions a4)

PDF_ID=$(echo $PDF_RESPONSE | jq -r '.generation_id')

# Retrieve both and download to output directory
sleep 5
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools get_gamma_assets \
  --generation-id $PPTX_ID \
  --download \
  --output-dir 99-TMP/OUTPUT

uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools get_gamma_assets \
  --generation-id $PDF_ID \
  --download \
  --output-dir 99-TMP/OUTPUT
```

### Retrieve Assets

```bash
# Get URLs
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools get_gamma_assets --generation-id abc123

# Download files to output directory
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools get_gamma_assets \
  --generation-id abc123 \
  --download \
  --output-dir 99-TMP/OUTPUT
```

---

## Core Scripts

### generate_gamma_presentation.py

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
- `--additional-instructions-file` - Path to file with custom instructions (alternative to --additional-instructions)
- `--card-header-footer` - Header/footer config as JSON
- `--folder-ids` - Target folders as JSON array
- `--sharing-workspace-access` - Workspace access level
- `--sharing-external-access` - External sharing level

**Output:** JSON with `url`, `generation_id`, and `error` fields

### get_gamma_assets.py

Retrieve presentation exports and optionally download them.

**Inputs:**
- `--generation-id` (required) - ID from generate_gamma_presentation
- `--download` - Flag to download files locally
- `--output-dir` - Download destination (default: /tmp/gamma_exports)

**Output:** JSON with `pdf`, `pptx` URLs and optional local paths

---

## Preset Patterns

### Executive Presentation Pattern

Ideal for C-level presentations with professional defaults:

```bash
generate_gamma_presentation \
  --input-text "<your-content>" \
  --format presentation \
  --text-mode condense \
  --export-as pptx \
  --card-split inputTextBreaks \
  --text-amount medium \
  --text-tone "professional and confident" \
  --text-audience "executives and senior leadership" \
  --image-source aiGenerated \
  --image-style photorealistic \
  --card-dimensions "16x9"
```

**Features:**
- PPTX export for PowerPoint compatibility
- Condensed text mode for conciseness
- Medium detail level
- Photorealistic AI-generated images
- Professional tone for executive audiences
- 16x9 widescreen format

### Executive Report Pattern

Ideal for detailed A4 PDF reports with preserved content:

```bash
generate_gamma_presentation \
  --input-text "<your-content>" \
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

**Features:**
- PDF export for distribution
- Preserve text mode for exact content retention
- A4 document format for printing
- Detailed content level
- Automatic card splitting
- Photorealistic images
- Professional tone

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

## Advanced Usage

### Custom Header/Footer

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --card-header-footer '{
    "topLeft": {"type": "image", "source": "themeLogo", "size": "sm"},
    "bottomRight": {"type": "cardNumber"},
    "hideFromFirstCard": true
  }'
```

### Email Sharing

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --sharing-email-options '{
    "recipients": ["stakeholder@company.com", "team@company.com"],
    "accessLevel": "view"
  }' \
  --sharing-external-access "edit"
```

### Multiple Folders & Workspace Sharing

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --folder-ids '["folder_sales_2025", "folder_exec_updates"]' \
  --sharing-workspace-access "fullAccess"
```

### Presentation with Custom AI Images

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/product_pitch.md \
  --format presentation \
  --image-source aiGenerated \
  --image-model "dall-e-3" \
  --image-style "minimalist, modern design, tech-focused" \
  --text-tone "innovative and forward-thinking" \
  --text-audience "venture capitalists and investors"
```

### Formatted Report with Instructions

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/quarterly_report.md \
  --additional-instructions-file 99-TMP/INPUT/report_guidelines.txt \
  --format document \
  --card-dimensions letter \
  --text-mode preserve \
  --text-amount extensive \
  --export-as pdf \
  --card-header-footer '{
    "topLeft": {"type": "image", "source": "themeLogo", "size": "md"},
    "topRight": {"type": "text", "value": "Q4 2024"},
    "bottomCenter": {"type": "cardNumber"},
    "hideFromFirstCard": true,
    "hideFromLastCard": true
  }'
```

---

## Environment Setup

Required environment variable:
```bash
export GAMMA_API_KEY=sk-gamma-xxxxxxxx
```

Available to: Pro, Ultra, Teams, and Business plan subscribers.

### Input/Output Directories

- **Input directory:** `99-TMP/INPUT/` - Place your content and instruction files here
- **Output directory:** `99-TMP/OUTPUT/` - Downloaded presentations will be saved here

All examples in this documentation use these standard directories.

---

## Complete API Reference

For detailed API documentation, supported parameters, limitations, and version info, see [references/GAMMA_API_REFERENCE.md](references/GAMMA_API_REFERENCE.md).

Key points:
- API v1.0 is GA (Generally Available)

---

## Examples

### Example 1: Quick Presentation from File

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/product_launch.md \
  --num-cards 5 \
  --export-as pptx
```

### Example 2: Marketing Social Post from File

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/social_post.md \
  --format social \
  --card-dimensions "1x1" \
  --image-source unsplash
```

### Example 3: Technical Documentation

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/api-docs.md \
  --format document \
  --card-dimensions pageless \
  --text-language en
```

### Example 4: Presentation with Custom Instructions from File

```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/presentation.md \
  --additional-instructions-file 99-TMP/INPUT/instructions.txt \
  --format presentation \
  --export-as pptx \
  --text-mode condense
```

### Example 5: Workflow - Generate Report then Download

```bash
# Generate
RESPONSE=$(uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation \
  --input-file 99-TMP/INPUT/sales_report.md \
  --format document \
  --export-as pdf)

GENERATION_ID=$(echo $RESPONSE | jq -r '.generation_id')

# Wait a moment for processing
sleep 5

# Download
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools get_gamma_assets \
  --generation-id $GENERATION_ID \
  --download \
  --output-dir 99-TMP/OUTPUT
```

---

## Troubleshooting

### "Either --input-text or --input-file is required"
Provide one of:
```bash
uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation --input-text "Content here" ...

# OR

uvx --from https://github.com/cbruyndoncx/ThirdBrAIn-Tools generate_gamma_presentation --input-file 99-TMP/INPUT/content.md ...
```

### "Error reading file"
Ensure the file path is correct and readable:
```bash
# Check file exists in input directory
ls -la 99-TMP/INPUT/content.md

# Verify input directory exists
ls -la 99-TMP/INPUT/
```

### "GAMMA_API_KEY environment variable not set"
Set your API key:
```bash
export GAMMA_API_KEY=sk-gamma-xxxxxxxx
```

### Generation returns no URL
Use `get_gamma_assets` with the `generation_id` to check status and retrieve exports.

### API Rate Limited (429 error)
Wait and retry. Most users have generous limits (hundreds per hour).

### Timeout during generation
Large generations (60+ cards) may take longer. Poll with `get_gamma_assets` using the `generation_id`.

---

## Support

- Official Docs: https://developers.gamma.app/docs
- API Reference: https://developers.gamma.app/reference/
- GitHub Issues: Report problems with the scripts
