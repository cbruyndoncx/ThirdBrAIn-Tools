#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "gkeepapi>=0.16.0",
#     "gpsoauth>=1.0.0",
#     "click>=8.0.0",
#     "rich>=13.0.0",
# ]
# ///
"""
Google Keep CLI Tool - Single-file uvx script

Run with: uv run keep.py <command> [options]

Commands:
    auth              Get master token (first time setup)
    list              List all notes
    search "query"    Search notes
    get <note_id>     Get a specific note
    create "title" "content"  Create a new note
    update <note_id>  Update an existing note
    delete <note_id>  Delete a note
    export            Export all notes
    labels            List all labels
    create-label      Create a new label
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
import gkeepapi
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

# Config file location
CONFIG_DIR = Path.home() / ".config" / "google-keep-tool"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """Load configuration from file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # Secure the config file


def get_keep_client() -> gkeepapi.Keep:
    """Get authenticated Keep client."""
    config = load_config()

    email = config.get("email") or os.environ.get("GOOGLE_EMAIL")
    master_token = config.get("master_token") or os.environ.get("GOOGLE_MASTER_TOKEN")

    if not email or not master_token:
        console.print("[red]Error:[/red] Not authenticated. Run 'uv run keep.py auth' first.")
        sys.exit(1)

    keep = gkeepapi.Keep()
    try:
        keep.authenticate(email, master_token)
        keep.sync()
    except Exception as e:
        console.print(f"[red]Authentication failed:[/red] {e}")
        sys.exit(1)

    return keep


@click.group()
@click.version_option(version="1.0.0", prog_name="google-keep")
def cli():
    """Google Keep CLI Tool - Manage your notes from the command line.

    Run with: uv run keep.py <command> [options]

    First time setup: uv run keep.py auth
    """
    pass


@cli.command()
@click.option("--email", prompt="Google Email", help="Your Google account email")
@click.option("--android-id", default="0123456789abcdef", help="Android device ID (any 16 hex chars)")
def auth(email: str, android_id: str):
    """Authenticate and store master token via OAuth token exchange.

    Steps:
    1. Open browser to: https://accounts.google.com/EmbeddedSetup
    2. Sign in to your Google account
    3. Press F12 to open DevTools
    4. Go to Application > Cookies > accounts.google.com
    5. Find 'oauth_token' cookie and copy its value
    6. Paste when prompted
    """
    import gpsoauth

    console.print("\n[cyan]OAuth Token Authentication[/cyan]\n")
    console.print("1. Open this URL in your browser:")
    console.print("   [link]https://accounts.google.com/EmbeddedSetup[/link]\n")
    console.print("2. Sign in to your Google account\n")
    console.print("3. After sign-in, open DevTools (F12)")
    console.print("4. Go to: Application > Cookies > accounts.google.com")
    console.print("5. Find the [cyan]oauth_token[/cyan] cookie and copy its value\n")

    oauth_token = click.prompt("Paste oauth_token here", hide_input=True)

    console.print("\n[yellow]Exchanging token...[/yellow]")

    try:
        result = gpsoauth.exchange_token(email, oauth_token, android_id)

        if "Token" not in result:
            console.print(f"[red]Token exchange failed:[/red] {result}")
            console.print("\n[yellow]Tips:[/yellow]")
            console.print("- Make sure you copied the full oauth_token value")
            console.print("- The token expires quickly, try again if it's been a while")
            console.print("- Try clearing cookies and starting fresh")
            sys.exit(1)

        master_token = result["Token"]

    except Exception as e:
        console.print(f"[red]Token exchange failed:[/red] {e}")
        sys.exit(1)

    # Verify the token works with gkeepapi
    console.print("[yellow]Verifying token with Google Keep...[/yellow]")
    try:
        keep = gkeepapi.Keep()
        keep.authenticate(email, master_token)
        keep.sync()
    except Exception as e:
        console.print(f"[red]Keep verification failed:[/red] {e}")
        sys.exit(1)

    # Save config
    config = {
        "email": email,
        "master_token": master_token,
        "android_id": android_id
    }
    save_config(config)

    console.print(f"\n[green]Authentication successful![/green]")
    console.print(f"[dim]Config saved to: {CONFIG_FILE}[/dim]")
    console.print(f"\n[cyan]Master Token:[/cyan]\n{master_token}\n")
    console.print("[dim]You can also set GOOGLE_EMAIL and GOOGLE_MASTER_TOKEN environment variables.[/dim]")
    console.print("\n[yellow]Tips:[/yellow]")
    console.print("1. Make sure you're using an App Password, not your regular password")
    console.print("2. Create one at: https://myaccount.google.com/apppasswords")
    console.print("3. If 2FA is disabled, you may need to enable it first")
    sys.exit(1)


@cli.command("list")
@click.option("--archived", is_flag=True, help="Include archived notes")
@click.option("--trashed", is_flag=True, help="Include trashed notes")
@click.option("--pinned", is_flag=True, help="Only show pinned notes")
@click.option("--limit", default=50, help="Maximum number of notes to show")
def list_notes(archived: bool, trashed: bool, pinned: bool, limit: int):
    """List all notes."""
    keep = get_keep_client()

    notes = list(keep.all())

    # Filter notes
    if not archived:
        notes = [n for n in notes if not n.archived]
    if not trashed:
        notes = [n for n in notes if not n.trashed]
    if pinned:
        notes = [n for n in notes if n.pinned]

    notes = notes[:limit]

    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return

    table = Table(title=f"Google Keep Notes ({len(notes)} shown)")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Title", style="cyan", max_width=40)
    table.add_column("Preview", max_width=50)
    table.add_column("Labels", style="magenta")
    table.add_column("Flags", style="green")

    for note in notes:
        flags = []
        if note.pinned:
            flags.append("pin")
        if note.archived:
            flags.append("arch")
        if hasattr(note, "checked") and note.checked:
            flags.append("done")

        # Get labels
        labels = [l.name for l in note.labels.all()]

        # Get preview text
        preview = ""
        if hasattr(note, "text") and note.text:
            preview = note.text[:50].replace("\n", " ")
            if len(note.text) > 50:
                preview += "..."
        elif hasattr(note, "items"):
            items = list(note.items)
            if items:
                preview = f"[{len(items)} items]"

        table.add_row(
            note.id[:12],
            note.title or "[untitled]",
            preview,
            ", ".join(labels) if labels else "-",
            " ".join(flags) if flags else "-"
        )

    console.print(table)


@cli.command()
@click.argument("query")
@click.option("--limit", default=20, help="Maximum results")
def search(query: str, limit: int):
    """Search notes by text."""
    keep = get_keep_client()

    results = list(keep.find(query=query))[:limit]

    if not results:
        console.print(f"[yellow]No notes found matching '{query}'[/yellow]")
        return

    console.print(f"\n[green]Found {len(results)} notes matching '{query}':[/green]\n")

    for note in results:
        title = note.title or "[untitled]"
        console.print(Panel(
            f"[dim]ID: {note.id}[/dim]\n\n{note.text or '[no content]'}",
            title=f"[cyan]{title}[/cyan]",
            border_style="blue"
        ))
        console.print()


@cli.command()
@click.argument("note_id")
@click.option("--format", "fmt", type=click.Choice(["text", "json", "md"]), default="text")
def get(note_id: str, fmt: str):
    """Get a specific note by ID (supports partial ID match)."""
    keep = get_keep_client()

    # Find note by ID (partial match)
    note = None
    for n in keep.all():
        if n.id.startswith(note_id):
            note = n
            break

    if not note:
        console.print(f"[red]Note not found:[/red] {note_id}")
        sys.exit(1)

    if fmt == "json":
        data = {
            "id": note.id,
            "title": note.title,
            "text": getattr(note, "text", None),
            "pinned": note.pinned,
            "archived": note.archived,
            "trashed": note.trashed,
            "labels": [l.name for l in note.labels.all()],
            "color": str(note.color) if note.color else None,
        }
        if hasattr(note, "items"):
            data["items"] = [{"text": i.text, "checked": i.checked} for i in note.items]
        console.print(json.dumps(data, indent=2))

    elif fmt == "md":
        md = f"# {note.title or 'Untitled'}\n\n"
        if hasattr(note, "text") and note.text:
            md += note.text
        elif hasattr(note, "items"):
            for item in note.items:
                checkbox = "x" if item.checked else " "
                md += f"- [{checkbox}] {item.text}\n"
        console.print(Markdown(md))

    else:  # text
        console.print(Panel(
            f"[dim]ID: {note.id}[/dim]\n"
            f"[dim]Pinned: {note.pinned} | Archived: {note.archived}[/dim]\n\n"
            f"{getattr(note, 'text', '') or '[no content]'}",
            title=f"[cyan]{note.title or 'Untitled'}[/cyan]",
            border_style="green"
        ))


# Available colors in Google Keep
COLORS = ["white", "red", "orange", "yellow", "green", "teal", "blue", "darkblue", "purple", "pink", "brown", "gray"]


def get_color_value(color_name: str):
    """Convert color name to gkeepapi ColorValue."""
    color_map = {
        "white": gkeepapi.node.ColorValue.White,
        "red": gkeepapi.node.ColorValue.Red,
        "orange": gkeepapi.node.ColorValue.Orange,
        "yellow": gkeepapi.node.ColorValue.Yellow,
        "green": gkeepapi.node.ColorValue.Green,
        "teal": gkeepapi.node.ColorValue.Teal,
        "blue": gkeepapi.node.ColorValue.Blue,
        "darkblue": gkeepapi.node.ColorValue.DarkBlue,
        "purple": gkeepapi.node.ColorValue.Purple,
        "pink": gkeepapi.node.ColorValue.Pink,
        "brown": gkeepapi.node.ColorValue.Brown,
        "gray": gkeepapi.node.ColorValue.Gray,
    }
    return color_map.get(color_name.lower())


@cli.command()
@click.argument("title")
@click.argument("content", default="")
@click.option("--file", "-f", "file_path", type=click.Path(exists=True), help="Read content from file")
@click.option("--pin", is_flag=True, help="Pin the note")
@click.option("--color", type=click.Choice(COLORS, case_sensitive=False), help="Note color")
@click.option("--label", multiple=True, help="Add labels to the note")
@click.option("--checklist", is_flag=True, help="Create as checklist (split content by newlines)")
def create(title: str, content: str, file_path: Optional[str], pin: bool, color: Optional[str], label: tuple, checklist: bool):
    """Create a new note.

    Content can be provided as argument or read from a file with --file.
    """
    keep = get_keep_client()

    # Read content from file if specified
    if file_path:
        content = Path(file_path).read_text()

    if checklist:
        note = keep.createList(title, [(item.strip(), False) for item in content.split("\n") if item.strip()])
    else:
        note = keep.createNote(title, content)

    if pin:
        note.pinned = True

    if color:
        note.color = get_color_value(color)

    # Add labels
    for label_name in label:
        lbl = keep.findLabel(label_name)
        if not lbl:
            lbl = keep.createLabel(label_name)
        note.labels.add(lbl)

    keep.sync()

    console.print(f"[green]Note created![/green]")
    console.print(f"[dim]ID: {note.id}[/dim]")


@cli.command()
@click.argument("note_id")
@click.option("--title", help="New title")
@click.option("--text", help="New text content")
@click.option("--file", "-f", "file_path", type=click.Path(exists=True), help="Read new text content from file")
@click.option("--color", type=click.Choice(COLORS, case_sensitive=False), help="Note color")
@click.option("--pin/--unpin", default=None, help="Pin or unpin the note")
@click.option("--archive/--unarchive", default=None, help="Archive or unarchive")
def update(note_id: str, title: Optional[str], text: Optional[str], file_path: Optional[str], color: Optional[str], pin: Optional[bool], archive: Optional[bool]):
    """Update an existing note.

    Text content can be provided with --text or read from a file with --file.
    """
    keep = get_keep_client()

    # Read content from file if specified
    if file_path:
        text = Path(file_path).read_text()

    # Find note
    note = None
    for n in keep.all():
        if n.id.startswith(note_id):
            note = n
            break

    if not note:
        console.print(f"[red]Note not found:[/red] {note_id}")
        sys.exit(1)

    if title is not None:
        note.title = title
    if text is not None:
        note.text = text
    if color is not None:
        note.color = get_color_value(color)
    if pin is not None:
        note.pinned = pin
    if archive is not None:
        note.archived = archive

    keep.sync()
    console.print(f"[green]Note updated![/green]")


@cli.command()
@click.argument("note_id")
@click.option("--permanent", is_flag=True, help="Permanently delete (not just trash)")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def delete(note_id: str, permanent: bool, yes: bool):
    """Delete a note (moves to trash by default)."""
    keep = get_keep_client()

    # Find note
    note = None
    for n in keep.all():
        if n.id.startswith(note_id):
            note = n
            break

    if not note:
        console.print(f"[red]Note not found:[/red] {note_id}")
        sys.exit(1)

    if not yes:
        if not click.confirm(f"Delete note '{note.title or note_id}'?"):
            console.print("[yellow]Cancelled.[/yellow]")
            return

    if permanent:
        note.delete()
    else:
        note.trashed = True

    keep.sync()
    console.print(f"[green]Note {'deleted' if permanent else 'moved to trash'}![/green]")


@cli.command()
@click.option("--format", "fmt", type=click.Choice(["json", "md"]), default="json")
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
@click.option("--include-archived", is_flag=True, help="Include archived notes")
def export(fmt: str, output: Optional[str], include_archived: bool):
    """Export all notes to JSON or Markdown."""
    keep = get_keep_client()

    notes = list(keep.all())
    if not include_archived:
        notes = [n for n in notes if not n.archived and not n.trashed]

    if fmt == "json":
        data = []
        for note in notes:
            note_data = {
                "id": note.id,
                "title": note.title,
                "text": getattr(note, "text", None),
                "pinned": note.pinned,
                "archived": note.archived,
                "labels": [l.name for l in note.labels.all()],
                "color": str(note.color) if note.color else None,
            }
            if hasattr(note, "items"):
                note_data["items"] = [{"text": i.text, "checked": i.checked} for i in note.items]
            data.append(note_data)

        result = json.dumps(data, indent=2, ensure_ascii=False)

    else:  # markdown
        lines = ["# Google Keep Export\n"]
        for note in notes:
            lines.append(f"## {note.title or 'Untitled'}\n")
            if hasattr(note, "text") and note.text:
                lines.append(note.text + "\n")
            elif hasattr(note, "items"):
                for item in note.items:
                    checkbox = "x" if item.checked else " "
                    lines.append(f"- [{checkbox}] {item.text}")
                lines.append("")
            lines.append("---\n")
        result = "\n".join(lines)

    if output:
        Path(output).write_text(result)
        console.print(f"[green]Exported {len(notes)} notes to {output}[/green]")
    else:
        console.print(result)


@cli.command()
def labels():
    """List all labels."""
    keep = get_keep_client()

    all_labels = list(keep.labels())

    if not all_labels:
        console.print("[yellow]No labels found.[/yellow]")
        return

    table = Table(title="Labels")
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")

    for label in all_labels:
        table.add_row(label.name, label.id)

    console.print(table)


@cli.command("create-label")
@click.argument("name")
def create_label(name: str):
    """Create a new label."""
    keep = get_keep_client()

    existing = keep.findLabel(name)
    if existing:
        console.print(f"[yellow]Label '{name}' already exists.[/yellow]")
        return

    keep.createLabel(name)
    keep.sync()
    console.print(f"[green]Label '{name}' created![/green]")


if __name__ == "__main__":
    cli()
