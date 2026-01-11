# Gamma API Reference

## Overview

This document describes the Gamma API integration used by the Gamma skill scripts. It specifies which version of the Gamma API is supported and which features are currently implemented.

**API Endpoint:** `https://public-api.gamma.app/v1.0/generations`
**Supported Version:** v1.0 (GA as of November 5, 2025)
**Last Updated:** 2025-01-11
**Deprecated Version:** v0.2 (sunset date: January 16, 2026)

---

## Authentication

All requests to the Gamma API require authentication via the `X-API-KEY` header:

```
X-API-KEY: sk-gamma-<your-api-key>
```

**Authentication Details:**
- API keys follow the format: `sk-gamma-xxxxxxxx`
- Pass as `X-API-KEY` header (NOT Bearer token)
- Available to Pro, Ultra, Teams, and Business plan subscribers
- Environment variable: `GAMMA_API_KEY`
- OAuth authentication is coming soon (not yet available)

**Rate Limits:**
- Most users: Hundreds of requests per hour, thousands per day

---

## Feature Support Matrix

### ✅ Fully Supported Features

| Feature Category | Supported Values |
|---|---|
| **Text Modes** | `generate`, `condense`, `preserve` |
| **Formats** | `presentation`, `document`, `social`, `webpage` |
| **Export Formats** | `pdf`, `pptx` |
| **Card Split Modes** | `auto`, `inputTextBreaks` |
| **Text Amount** | `brief`, `medium`, `detailed`, `extensive` |

### ✅ Image Source Options

- `aiGenerated` - AI-generated images (DALL-E or similar)
- `pictographic` - Icon/illustration style images
- `unsplash` - Unsplash free stock photos
- `giphy` - GIF animations from Giphy
- `webAllImages` - Any web images
- `webFreeToUse` - Creative Commons free-to-use images
- `webFreeToUseCommercially` - Commercially licensed images
- `placeholder` - Gray placeholder boxes
- `noImages` - No images (text only)

### ✅ Card Dimensions (Format-Specific)

**Presentation Format:**
- `fluid` - Responsive/flexible
- `16x9` - Widescreen (standard)
- `4x3` - Standard aspect ratio

**Document Format:**
- `fluid` - Responsive/flexible
- `pageless` - Continuous scroll
- `letter` - US Letter (8.5" × 11")
- `a4` - A4 (210 × 297 mm)

**Social Format:**
- `1x1` - Square (Instagram feed)
- `4x5` - Portrait (Instagram Stories)
- `9x16` - Tall portrait (TikTok/Reels)

### ✅ Header/Footer Features

**Positions:** `topLeft`, `topRight`, `topCenter`, `bottomLeft`, `bottomRight`, `bottomCenter`

**Element Types:**
- `text` - Custom text (requires `value` parameter)
- `image` - Image element (requires `source` parameter)
- `cardNumber` - Auto-numbered slide counter

**Image Sources:**
- `themeLogo` - Logo from selected theme
- `custom` - Custom image URL (requires `src` parameter)

**Sizes:** `sm`, `md`, `lg`, `xl`

**Additional Options:**
- `hideFromFirstCard` - Omit header/footer from title slide
- `hideFromLastCard` - Omit header/footer from last slide

### ✅ Text Customization Options

- `amount` - Content length/detail level
- `tone` - Voice and style (e.g., "professional and confident", "casual and friendly")
- `audience` - Target audience (e.g., "executives and senior leadership")
- `language` - Output language code (e.g., "en", "es", "fr")

### ✅ Image Customization Options

- `source` - Image source (see Image Source Options above)
- `model` - AI model for generation (e.g., "dall-e-3")
- `style` - Visual style (e.g., "photorealistic", "minimalist", "abstract")

### ✅ Sharing & Collaboration Options

- `sharingOptions.workspaceAccess` - Workspace access level (`noAccess`, `view`, `comment`, `edit`, `fullAccess`)
- `sharingOptions.externalAccess` - External sharing level (`noAccess`, `view`, `comment`, `edit`)
- `sharingOptions.emailOptions` - Email sharing configuration (recipients and access levels)

### ✅ Other Supported Parameters

- `themeId` - Apply a specific theme to the generation
- `folderIds` - Array of folder IDs for organization in Gamma workspace
- `additionalInstructions` - Custom instructions for content generation (1-2000 characters)
- `numCards` - Specific number of cards/slides (plan-dependent limits)

### ℹ️ Plan-Specific Limits

| Feature | Pro | Ultra |
|---------|-----|-------|
| **Max Cards** | 1-60 | 1-75 |
| **API Access** | Yes | Yes |

### ℹ️ Language Support

The API supports 60+ languages via the `language` parameter in `textOptions`. Common codes include: `en`, `es`, `fr`, `de`, `it`, `pt`, `ja`, `zh`, `ko`, and many others.

---

## Request Format

### POST /v1.0/generations

Generate a new presentation.

**Headers:**
```
X-API-KEY: <your-api-key>
Content-Type: application/json
```

**Request Body Schema:**

```json
{
  "inputText": "string (required) - Content with text and image URLs",
  "textMode": "generate | condense | preserve (required)",
  "format": "presentation | document | social | webpage (optional, default: presentation)",
  "numCards": "number (optional, default: 10, plan-dependent max)",
  "exportAs": "pdf | pptx (optional)",
  "cardSplit": "auto | inputTextBreaks (optional)",
  "themeId": "string (optional)",
  "folderIds": ["string (optional)"],
  "additionalInstructions": "string (optional, 1-2000 characters)",
  "textOptions": {
    "amount": "brief | medium | detailed | extensive (optional)",
    "tone": "string (optional)",
    "audience": "string (optional)",
    "language": "string (optional, supports 60+ languages)"
  },
  "imageOptions": {
    "source": "aiGenerated | pictographic | unsplash | giphy | webAllImages | webFreeToUse | webFreeToUseCommercially | placeholder | noImages (optional)",
    "model": "string (optional, auto-selected if unspecified)",
    "style": "string (optional)"
  },
  "cardOptions": {
    "dimensions": "string (optional, format-specific)",
    "headerFooter": {
      "topLeft": { "type": "text | image | cardNumber", "value": "string", "source": "themeLogo | custom", "src": "string", "size": "sm | md | lg | xl" },
      "topRight": { ... },
      "topCenter": { ... },
      "bottomLeft": { ... },
      "bottomRight": { ... },
      "bottomCenter": { ... },
      "hideFromFirstCard": "boolean (optional)",
      "hideFromLastCard": "boolean (optional)"
    }
  },
  "sharingOptions": {
    "workspaceAccess": "noAccess | view | comment | edit | fullAccess (optional)",
    "externalAccess": "noAccess | view | comment | edit (optional)",
    "emailOptions": { "recipients": [], "accessLevel": "string (optional)" }
  }
}
```

---

## Response Format

### Successful Generation (201 Created or 200 OK)

```json
{
  "generationId": "string",
  "status": "pending | processing | completed | failed",
  "gammaUrl": "string (optional, available when completed)",
  "exportUrl": "string (optional, for exports)",
  "pdfUrl": "string (optional, if PDF export)",
  "pptxUrl": "string (optional, if PPTX export)"
}
```

**Note:** Response field names vary. The scripts normalize variations including:
- `generationId` / `generation_id` / `id`
- `gammaUrl` / `gamma_url` / `url` / `exportUrl` / `export_url` / `outputUrl` / `output_url`
- Fields may also appear in arrays: `outputs[0].url`, `exports[]`, `artifacts[].url`

### GET /v1.0/generations/{generationId}

Poll generation status.

**Response (same schema as above, reflects current status)**

**Status Values:**
- `pending` - Queued for processing
- `processing` - Currently generating
- `completed` / `succeeded` - Successfully completed
- `failed` / `error` - Generation failed

---

## Generation Polling Behavior

### Timeout & Polling Configuration

- **Total Timeout:** 10 minutes (600 seconds)
- **Poll Interval:** 30 seconds between status checks
- **Behavior:** Synchronous polling until generation completes or timeout occurs

### Polling Flow

1. POST request submitted to create generation
2. Response returns `generationId` immediately
3. Client polls `/v1.0/generations/{generationId}` every 30 seconds
4. On completion, response includes `gammaUrl` or export URLs
5. If no URL after completion, generation was created but exports not yet available
6. Timeout returns error after 10 minutes of polling

---

## Additional APIs

### Create from Template API
An alternative to the Generate API is available for creating gammas from existing templates. See the official Gamma documentation for details on this separate endpoint.

### List Themes API
Retrieve available themes for the `themeId` parameter.

### List Folders API
Retrieve available folders for the `folderIds` parameter.

---

## Known Limitations & Quirks

### ⚠️ Async Generation with Polling

Generations are asynchronous and require polling for completion. The API returns a `generationId` immediately but the actual presentation URL may not be available for several minutes.

### ⚠️ Export Format Limitations

- Only `pdf` and `pptx` are supported for direct export
- HTML export is not available through this API version
- Exports may take additional time beyond generation completion

### ⚠️ Response Field Inconsistencies

The API returns different field names depending on context and response timing:
- `generationId` vs `generation_id` vs `id`
- Multiple URL field variations (`url`, `gammaUrl`, `exportUrl`, etc.)
- URLs may be nested in arrays (`outputs[0].url`, `exports[]`, etc.)

The scripts handle these variations automatically through field extraction logic.

### ⚠️ Card Number Constraints

- Default: 10 cards
- Pro plan: 1-60 cards
- Ultra plan: 1-75 cards
- Above 15 cards: May require increments of 5 (20, 25, 30, etc.)

The scripts automatically normalize card counts within plan-specific constraints.

### ⚠️ Format-Specific Validation

Different formats support different dimension options:
- Presentation: `fluid`, `16x9`, `4x3` only
- Document: `fluid`, `pageless`, `letter`, `a4` only
- Social: `1x1`, `4x5`, `9x16` only

Providing incompatible dimensions may result in API rejection or silent fallback to defaults.

---

## Error Handling

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| 200/201 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (quota exceeded or access denied) |
| 429 | Rate limited |
| 500 | Server error |

### Common Error Scenarios

**Missing or Invalid API Key:**
```
401 Unauthorized
```

**Quota Exceeded:**
```
403 Forbidden - Generation quota exceeded
```

**Rate Limited:**
```
429 Too Many Requests
Retry-After: <seconds>
```

**Invalid Parameters:**
```
400 Bad Request
Detail: Invalid format or textMode value
```

---

## Examples

### Basic Presentation Request

```json
{
  "inputText": "# Company Quarterly Review\n## Q4 Performance Summary\n- Revenue: +15%\n- Growth: Ahead of targets",
  "format": "presentation",
  "textMode": "generate",
  "numCards": 10,
  "exportAs": "pptx"
}
```

### Executive Report Request

```json
{
  "inputText": "Detailed report content...",
  "format": "document",
  "textMode": "preserve",
  "numCards": 12,
  "exportAs": "pdf",
  "cardOptions": {
    "dimensions": "a4",
    "headerFooter": {
      "topLeft": { "type": "image", "source": "themeLogo", "size": "sm" },
      "bottomRight": { "type": "cardNumber" }
    }
  },
  "textOptions": {
    "amount": "detailed",
    "tone": "professional and confident",
    "audience": "executives and senior leadership"
  },
  "imageOptions": {
    "source": "aiGenerated",
    "style": "photorealistic"
  }
}
```

### Polling for Completion

```bash
# Submit generation
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H "X-API-KEY: <key>" \
  -H "Content-Type: application/json" \
  -d '{"inputText": "...", "format": "presentation"}'

# Response: {"generationId": "abc123", "status": "pending"}

# Poll status every 30 seconds
curl -X GET https://public-api.gamma.app/v1.0/generations/abc123 \
  -H "X-API-KEY: <key>"

# Response when ready: {"generationId": "abc123", "status": "completed", "gammaUrl": "https://gamma.app/..."}
```

---

## Environment Variables

| Variable | Required | Description | Format |
|----------|----------|-------------|--------|
| `GAMMA_API_KEY` | Yes | API key for authentication | `sk-gamma-xxxxxxxx` |

---

## Version History

### v1.0 (Current)
- Public Gamma API v1.0
- Async generation with polling
- PDF and PPTX exports
- Theme and header/footer customization
- Full text and image options

---

## Support & Updates

**Official Documentation:** https://developers.gamma.app/docs

**Key Resources:**
- [Getting Started](https://developers.gamma.app/docs/getting-started)
- [Generate API Parameters Explained](https://developers.gamma.app/docs/generate-api-parameters-explained)
- [API Reference](https://developers.gamma.app/reference/)
- [Changelog](https://developers.gamma.app/changelog)

For issues with these Python scripts, see the main SKILL.md and examples.md files.
