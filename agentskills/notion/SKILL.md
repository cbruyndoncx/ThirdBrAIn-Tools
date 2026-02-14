---
name: notion
description: Manage Notion workspace via CLI - pages, databases, todos, blocks, and search. Use when the user wants to create, read, update, delete, or query Notion pages, databases, todos, or blocks. Also use for searching Notion content, managing block types (30+), querying databases with filters/sorts, and todo management with priorities/tags/due dates.
---

# Notion CLI

Single-file CLI with complete Notion API coverage. Run with `uv run scripts/notion.py`.

## Environment

```bash
# Required
export NOTION_API_KEY="ntn_..."

# Optional defaults
export NOTION_DATABASE_ID="your_database_id"
export NOTION_PARENT_PAGE_ID="your_parent_page_id"
```

Verify setup: `uv run scripts/notion.py verify-connection`

## Command Reference

```bash
# Diagnostics
uv run scripts/notion.py verify-connection
uv run scripts/notion.py check-config

# Search & list
uv run scripts/notion.py search "query"
uv run scripts/notion.py list pages
uv run scripts/notion.py list databases --refresh

# Pages (supports name paths like "Work/Projects/Q1")
uv run scripts/notion.py add page --title "Title" --parent "Parent" --icon "📝" --content "text"
uv run scripts/notion.py get page "Page Name"
uv run scripts/notion.py update page "Name" --title "New Title"
uv run scripts/notion.py update page "Name" --archive
uv run scripts/notion.py move page "Name" --to "Destination"
uv run scripts/notion.py delete page "Name"

# Databases
uv run scripts/notion.py add database --title "Tasks" --parent "Work" --template tasks
uv run scripts/notion.py get database "Tasks"
uv run scripts/notion.py query database "Tasks" --status "In Progress" --priority High
uv run scripts/notion.py query database "Tasks" --filter '{"property":"Status","status":{"equals":"Done"}}'
uv run scripts/notion.py query database "Tasks" --all  # paginate all results
uv run scripts/notion.py update database "Tasks" --title "My Tasks"

# Todos
uv run scripts/notion.py add todo --database "Tasks" --title "Task" --priority High --tags "work,urgent" --due-date "2026-12-31" --status "In Progress"
uv run scripts/notion.py todos search --database "Tasks" --status "In Progress" --priority High

# Blocks (30+ types: paragraph, heading_1-3, bulleted_list_item, numbered_list_item, to_do, code, quote, toggle, callout, image, video, bookmark, divider, equation, table_of_contents, etc.)
uv run scripts/notion.py blocks add "Page" --type paragraph --text "content"
uv run scripts/notion.py blocks add "Page" --type code --text "print('hi')" --language python
uv run scripts/notion.py blocks add "Page" --type callout --text "Note" --icon "💡"
uv run scripts/notion.py blocks add "Page" --type image --url "https://..."
uv run scripts/notion.py blocks list "Page"
uv run scripts/notion.py get block <block-id>
uv run scripts/notion.py update block <block-id> --text "new content"
uv run scripts/notion.py blocks delete <block-id>

# Subtasks
uv run scripts/notion.py blocks subtasks add <todo-block-id> --text "Subtask"
uv run scripts/notion.py blocks subtasks list <todo-block-id>
uv run scripts/notion.py blocks subtasks check <subtask-id>

# Cache
uv run scripts/notion.py refresh-cache
```

## Key Features

- **Path navigation**: Use `"Parent/Child"` names instead of UUIDs everywhere
- **Smart caching**: Name-to-ID resolution cached at `~/.cache/notion-cli/cache.json`, auto-refreshes every 24h
- **Database templates**: `--template tasks|notes|contacts` for quick setup
- **Filter shortcuts**: `--status`, `--priority`, `--due-before` instead of raw JSON filters
- **All output is JSON**: Pipe-friendly for downstream processing

## Tips

- Run `--help` on any command for full option details
- Use `refresh-cache` after creating new pages/databases if name lookup fails
- The `--all` flag on query paginates through all results (use sparingly on large databases)
- Blocks can be nested - add blocks to a toggle or page to create hierarchy
