---
name: notebooklm-pdf2ppt
description: "Convert NotebookLM PDF slide exports to PowerPoint (.pptx) preserving vector graphics quality. Use when the user wants to convert PDF slides (especially from Google NotebookLM) to PowerPoint, needs PDF-to-PPTX conversion with high fidelity, or asks to remove NotebookLM watermarks from exported slides. Triggers on tasks involving: (1) PDF to PowerPoint conversion, (2) NotebookLM slide export processing, (3) batch converting multiple PDF presentations, (4) removing NotebookLM watermarks from PDFs."
---

# NotebookLM PDF to PowerPoint

Single-file `uv run` script that converts PDF slides to PPTX using a **PDF → SVG → EMF → PPTX** pipeline. No rasterization — vector graphics are preserved at any zoom level.

## Usage

**Via direct script:**
```bash
uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/pdf2ppt.py input.pdf --remove-watermark
```

**Local:**
```bash
uv run scripts/pdf2ppt.py input.pdf
```

## System Dependencies

Two external tools are required on PATH. Check before converting:

```bash
uv run scripts/pdf2ppt.py --check-deps
# Returns JSON: {"ok": bool, "pdf2svg": bool, "inkscape": bool}
# Exit code 0 = ready, 2 = missing dependencies
```

Install missing dependencies:

| Platform | Command |
|----------|---------|
| macOS | `brew install pdf2svg inkscape` |
| Ubuntu/Debian | `sudo apt install pdf2svg inkscape` |
| Fedora/RHEL | `sudo dnf install pdf2svg inkscape` |
| Arch | `sudo pacman -S pdf2svg inkscape` |
| Alpine | `apk add pdf2svg inkscape` |
| Windows | `choco install pdf2svg inkscape` |

The AI harness should install these before invoking if the execution environment allows it.

## Conversion Workflow

### 1. Check dependencies

```bash
uv run scripts/pdf2ppt.py --check-deps
```

If `"ok": false`, install the missing tool(s), then re-check.

### 2. Convert

```bash
# Single file
uv run scripts/pdf2ppt.py input.pdf

# With watermark removal and parallel processing
uv run scripts/pdf2ppt.py input.pdf --remove-watermark --parallel 4 --force

# Specific pages, custom output
uv run scripts/pdf2ppt.py input.pdf output.pptx --pages 1-5,7
```

### 3. Batch convert

```bash
for f in /path/to/pdfs/*.pdf; do
  uv run scripts/pdf2ppt.py "$f" --remove-watermark --force --parallel 4
done
```

Output `.pptx` files are created next to each input PDF by default.

## Command Reference

| Flag | Description |
|------|-------------|
| `--check-deps` | Check system deps, print JSON, exit |
| `--remove-watermark`, `--rw` | Remove NotebookLM watermark |
| `--pages`, `-p` | Page range: `1-5,7,9-11` |
| `--parallel`, `-j` | Parallel SVG→EMF workers (default: 1) |
| `--force`, `-f` | Overwrite existing output |
| `--no-clean` | Keep temp files after conversion |
| `--no-check` | Skip SVG transparency warnings |
| `--verbose` | Verbose output |

Exit codes: 0=success, 1=generic error, 2=missing deps, 101=pdf2svg failure, 102=svg2emf failure.
