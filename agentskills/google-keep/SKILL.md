---
name: google-keep
description: Manage Google Keep notes - search, create, update, delete, and export notes. Includes interactive auth setup, Rich-formatted output, checklist support, and partial ID matching.
---

# Google Keep CLI

Manage your Google Keep notes from the command line with Rich-formatted output, interactive auth, checklist support, and bulk export.

## Usage

**Via uvx from GitHub:**
```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep list
```

**Alternative (direct script):**
```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/google_keep.py list
```

## First Time Setup

### Interactive Auth

The easiest way to authenticate is with the built-in `auth` command:

```bash
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep auth --email your-email@gmail.com
```

This walks you through OAuth token exchange and stores credentials securely in `~/.config/google-keep-tool/config.json`.

### Manual Setup (Environment Variables)

Alternatively, set environment variables directly:

```bash
export GOOGLE_EMAIL="your-email@gmail.com"
export GOOGLE_MASTER_TOKEN="your-master-token"
```

See the gkeepapi documentation for obtaining a master token:
- https://gkeepapi.readthedocs.io/en/latest/#obtaining-a-master-token
- https://github.com/simon-weber/gpsoauth?tab=readme-ov-file#alternative-flow

---

## Quick Start

### List Notes

```bash
# List all notes (default limit: 50)
google_keep list

# Only pinned notes
google_keep list --pinned

# Include archived notes
google_keep list --archived

# Limit results
google_keep list --limit 10
```

### Search Notes

```bash
google_keep search "shopping list"

# Limit results
google_keep search "meeting" --limit 5
```

### Get a Specific Note

```bash
# By full ID
google_keep get abc123def456

# By partial ID (prefix match)
google_keep get abc123

# Output as JSON
google_keep get abc123 --format json

# Output as rendered Markdown
google_keep get abc123 --format md
```

### Create a Note

```bash
# Simple note
google_keep create "My Note" "Content goes here"

# Pinned note with color
google_keep create "Important" "Don't forget!" --pin --color yellow

# Read content from file
google_keep create "From File" --file notes.txt

# Create a checklist (splits content by newlines)
google_keep create "Shopping" "Milk
Eggs
Bread" --checklist

# With labels
google_keep create "Work Task" "Finish report" --label work --label urgent
```

### Update a Note

```bash
# Update title
google_keep update abc123 --title "New Title"

# Update text
google_keep update abc123 --text "New content"

# Read new content from file
google_keep update abc123 --file updated.txt

# Pin/unpin
google_keep update abc123 --pin
google_keep update abc123 --unpin

# Archive/unarchive
google_keep update abc123 --archive
google_keep update abc123 --unarchive

# Change color
google_keep update abc123 --color teal
```

### Delete a Note

```bash
# Move to trash (with confirmation prompt)
google_keep delete abc123

# Skip confirmation
google_keep delete abc123 --yes

# Permanently delete
google_keep delete abc123 --permanent --yes
```

### Labels

```bash
# List all labels
google_keep labels

# Create a new label
google_keep create-label "my-label"
```

### Export Notes

```bash
# Export all notes as JSON
google_keep export

# Export as Markdown
google_keep export --format md

# Export to file
google_keep export --output notes.json

# Include archived notes
google_keep export --include-archived
```

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `auth` | Interactive authentication setup |
| `list` | List all notes (Rich table) |
| `search <query>` | Search notes by text |
| `get <note_id>` | Get a specific note (supports partial ID) |
| `create <title> [content]` | Create a new note or checklist |
| `update <note_id>` | Update an existing note |
| `delete <note_id>` | Delete a note (trash or permanent) |
| `labels` | List all labels |
| `create-label <name>` | Create a new label |
| `export` | Export all notes to JSON or Markdown |

---

## Command Options

### list

| Option | Purpose |
|--------|---------|
| `--archived` | Include archived notes |
| `--trashed` | Include trashed notes |
| `--pinned` | Only show pinned notes |
| `--limit N` | Max notes to show (default: 50) |

### search

| Option | Purpose |
|--------|---------|
| `query` | Search query (required) |
| `--limit N` | Max results (default: 20) |

### get

| Option | Purpose |
|--------|---------|
| `note_id` | Note ID or prefix (required) |
| `--format` | Output format: `text`, `json`, or `md` (default: text) |

### create

| Option | Purpose |
|--------|---------|
| `title` | Note title (required) |
| `content` | Note content (optional) |
| `--file, -f` | Read content from file |
| `--pin` | Pin the note |
| `--color` | Note color (see colors below) |
| `--label` | Add label (repeatable) |
| `--checklist` | Create as checklist |

### update

| Option | Purpose |
|--------|---------|
| `note_id` | Note ID or prefix (required) |
| `--title` | New title |
| `--text` | New text content |
| `--file, -f` | Read new content from file |
| `--color` | Note color |
| `--pin / --unpin` | Pin or unpin |
| `--archive / --unarchive` | Archive or unarchive |

### delete

| Option | Purpose |
|--------|---------|
| `note_id` | Note ID or prefix (required) |
| `--permanent` | Permanently delete (not just trash) |
| `--yes, -y` | Skip confirmation prompt |

### export

| Option | Purpose |
|--------|---------|
| `--format` | `json` or `md` (default: json) |
| `--output, -o` | Output file path |
| `--include-archived` | Include archived notes |

### Available Colors

`white`, `red`, `orange`, `yellow`, `green`, `teal`, `blue`, `darkblue`, `purple`, `pink`, `brown`, `gray`

---

## Output Format

The CLI uses Rich-formatted output by default (colored tables, panels). Use `--format json` on the `get` command or `export` for machine-readable JSON output.

### Example JSON (via `get --format json` or `export`)

```json
{
  "id": "abc123",
  "title": "Shopping List",
  "text": "Milk, eggs, bread",
  "pinned": false,
  "archived": false,
  "trashed": false,
  "labels": ["groceries"],
  "color": "ColorValue.Yellow"
}
```

---

## Understanding `uvx --from`

The `uvx --from` syntax provides flexible remote execution:

```bash
# From GitHub (main branch)
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[keep]" google_keep list

# From specific branch
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@develop[keep]" google_keep list

# From specific tag/version
uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools@v1.0.0[keep]" google_keep list
```

### Available Extras

| Extra | Dependencies | Commands |
|-------|--------------|----------|
| `research` | `httpx` | `research`, `poll_research`, `extract_json` |
| `gamma` | (base only) | `generate_gamma_presentation`, `get_gamma_assets` |
| `keep` | `gkeepapi`, `gpsoauth`, `click`, `rich` | `google_keep` |
| `nanobanana` | `google-generativeai`, `pillow` | `nanobanana` |
| `all` | All dependencies | All commands |

See [scripts/README.md](../../scripts/README.md) for full documentation on `uvx --from` options.

---

## Troubleshooting

### "Not authenticated" Error

Run `google_keep auth` to set up credentials, or set environment variables:
```bash
export GOOGLE_EMAIL="your-email@gmail.com"
export GOOGLE_MASTER_TOKEN="your-master-token"
```

### "Authentication failed" Error

Your master token may be expired or invalid. Run `google_keep auth` to obtain a new one.

### "DeviceManagementRequiredOrSyncDisabled" Error

If using Google Workspace:
1. Go to https://admin.google.com/ac/devices/settings/general
2. Turn "Mobile management" to "Unmanaged"

---

## Support

- gkeepapi docs: https://gkeepapi.readthedocs.io/
- GitHub Issues: Report problems with the script
