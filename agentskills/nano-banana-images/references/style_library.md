# Nano Banana Style Library

The style library is your personal creative toolkit - a collection of proven styles you can reuse.

## Files

Located in the skill's `style-library/` folder:

| File | Purpose |
|------|---------|
| `style-library.html` | Interactive browser UI with thumbnails, tags, and prompts |
| `get_style.py` | CLI helper to fetch style prompts by ID |
| `thumbnails/` | PNG previews for each saved style |

## Using the Library

### Browse Styles

Open `style-library.html` in a browser. Each style card shows:
- Index number (e.g., "#02")
- Thumbnail preview (hover to enlarge)
- Name and tags
- Category filter
- Full prompt (hover to expand, click to copy)
- Example uses

### Fetch a Style by ID

```bash
python get_style.py 3          # Get style #3 prompt
python get_style.py --list     # List all style names
```

### Generate with a Saved Style

When user says "use style #3":
1. Run `get_style.py 3` to get the prompt
2. Combine with their subject
3. Call `generate()` with the merged prompt

---

## Growing the Library

Three methods to add new styles:

### Method 1: Save As You Go

When user creates something they like:
1. User says "add this to my library"
2. Copy output PNG to `thumbnails/` (kebab-case name)
3. Add entry to `styles` array in `style-library.html`

### Method 2: Collect From Online

Found a great prompt on social media or a database:
1. Test it with `generate()`
2. If it works well, save to library

### Method 3: Extract From Any Image (Power Move)

Use `style_extract.py` to analyze any image and extract its style as natural language.

```python
from style_extract import extract_style, extract_and_save

# Get style description
result = extract_style("path/to/image.png")
print(result)

# Or save directly to markdown
extract_and_save("path/to/image.png")
```

The extractor captures: color palette, lighting, composition, textures, mood, artistic style, typography, special effects.

**Workflow:**
1. Extract style from inspiration image
2. Use extracted text as prompt to recreate the aesthetic
3. Save the recreated render to your library

---

## Adding a Style Entry

### Required Fields

```javascript
{
  id: "07",                           // Next available number
  name: "Vintage Film Grain",         // Descriptive name
  category: "Artistic",               // From CATEGORIES list
  tags: ["retro", "photography"],     // 2-4 from CANONICAL_TAGS
  thumbnail: "thumbnails/vintage-film-grain.png",
  prompt: "Full natural language prompt...",
  exampleUse: "When to use this style"
}
```

### Categories (use exactly)

- Framework
- Flow
- Architecture
- Mockup
- Persona
- Marketing
- Artistic

### Canonical Tags by Category

**Framework:** `2x2-matrix`, `pyramid`, `venn`, `canvas`, `concentric`, `triangle`

**Flow:** `process`, `journey-map`, `flowchart`, `steps`, `sequence`

**Architecture:** `hierarchy`, `hub-spoke`, `system-diagram`, `org-chart`, `tree`

**Mockup:** `wireframe`, `device-frame`, `ui-concept`, `landing-page`, `mobile`, `desktop`

**Persona:** `portrait`, `lifestyle`, `headshot`, `context`, `illustrated`, `scene`

**Marketing:** `ad`, `social`, `announcement`, `banner`, `hero`

**Artistic:** `flat-illustration`, `hand-drawn`, `watercolor`, `photography`, `retro`, `minimalist`, `bold-graphic`, `3d-render`

**Important:** Do NOT invent new tags or categories. Reuse canonical tags to keep the library consistent.

---

## File Naming

Use kebab-case for thumbnails:
- ✅ `vaporwave-portrait.png`
- ✅ `90s-analog-snapshot.png`
- ❌ `Vaporwave Portrait.png`
- ❌ `vaporwave_portrait.png`

---

## Reference Images

For consistent subjects across styles, provide multiple reference photos:
- 3+ angles of the same subject gives better accuracy
- Mix style reference with subject references
- Store subject references in `references/` folder
