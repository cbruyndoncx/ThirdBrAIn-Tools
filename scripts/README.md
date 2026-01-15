# Deep Research Scripts

Helper scripts for conducting comprehensive AI-powered research with OpenAI and DeepSeek.

## Scripts Overview

**Tip:** add `--help` to any helper (`research.py`, `poll_research.py`, `generate_gamma_presentation.py`, `get_gamma_assets.py`) to see the full list of arguments and their explanations before running.

### 1. `research.py` - Main Research Script

Primary script for creating and managing deep research requests.

**Quick Start:**
```bash
# With polling (waits for completion)
python3 research.py --query-file query.md --provider openai --poll

# Without polling (returns request ID immediately)
python3 research.py --query-file query.md --provider openai
```

**Load credentials from elsewhere:** use `--env-file /path/to/.env` when running from a different directory so `OPENAI_API_KEY`/`DEEPSEEK_API_KEY` load regardless of your CWD.

**Key Features:**
- Supports OpenAI and DeepSeek providers
- Adaptive polling intervals (10s → 30s → 1m → 5m)
- Auto-saves both raw JSON and extracted markdown
- Displays prominent request ID for reconnection
- Handles background processing

### 2. `poll_research.py` - Polling & Reconnection Script

**NEW:** Reconnect to long-running research jobs and retrieve results.

**Quick Start:**
```bash
# Poll and retrieve results
python3 poll_research.py resp_abc123def456

# Just check status
python3 poll_research.py resp_abc123def456 --check-only

# Poll with custom timeout (1 hour)
python3 poll_research.py resp_abc123def456 --timeout 3600
```

**Load credentials from elsewhere:** add `--env-file /path/to/.env` so `OPENAI_API_KEY` is read even if the script is executed from outside the repo.

**Use Cases:**
- Reconnect after disconnection
- Check status of background research
- Retrieve results when convenient
- Custom timeout for very long research

**Key Features:**
- Adaptive polling like research.py
- Saves both raw JSON and markdown
- Shows character count and file locations
- Supports custom timeouts
- Status-only checking mode

### 3. `extract_json.py` - JSON Extraction Helper

Extract markdown content from OpenAI's nested JSON response structure.

**Quick Start:**
```bash
python3 extract_json.py input.json output.md
```

**Use Cases:**
- Extract markdown from saved raw JSON
- Re-process OpenAI responses
- Debugging response structure issues

**How It Works:**
```python
# Navigates nested structure:
response.output[]
  -> type="message"
    -> content[]
      -> type="output_text"
        -> text (markdown content)
```

## Common Workflows

### Workflow 1: Wait for Completion

**Best for:** Short research tasks or when you can wait

```bash
python3 research.py \
  --query-file 99-TMP/INPUT/query.md \
  --output 99-TMP/OUTPUT/result.md \
  --provider openai \
  --poll \
  --verbose
```

**Result:**
- Markdown saved to: `99-TMP/OUTPUT/result_260111_1430.md` (with frontmatter, timestamp appended)
- Raw JSON saved to: `99-TMP/OUTPUT/result_260111_1430-raw.json` (timestamp appended)

### Workflow 2: Submit and Reconnect

**Best for:** Long research, disconnection risk, background processing

**Step 1: Submit**
```bash
python3 research.py --query-file query.md --provider openai
```

**Output:**
```
======================================================================
✓ Request created successfully!
  Request ID: resp_060d0cafcee3c1b4006962dad3910c81a2adbb24abaa24a49b
======================================================================
```

**Step 2: Check Status (anytime)**
```bash
python3 poll_research.py resp_060d0cafcee3... --check-only
```

**Step 3: Retrieve (when ready)**
```bash
python3 poll_research.py resp_060d0cafcee3... --output result.md --verbose
```

### Workflow 3: Manual Status Check

Use curl for direct API access:

```bash
curl -X GET "https://api.openai.com/v1/responses/REQUEST_ID" \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq
```

## File Organization

**Typical output structure:**

```
99-TMP/
├── INPUT/
│   └── company-research-query.md                    # Your research query
└── OUTPUT/
    ├── openai_o4-mini-deep-research_260111_1430.md         # Extracted markdown with frontmatter
    └── openai_o4-mini-deep-research_260111_1430-raw.json   # Raw API response
```

**Filename format:**
- `{provider}_{model}_{timestamp}.md` - Markdown report with YAML frontmatter
- `{provider}_{model}_{timestamp}-raw.json` - Raw JSON response
- Timestamp format: `YYMMDD_HHMM` (e.g., `260111_1430` = Jan 11, 2026 at 2:30 PM)

**Frontmatter structure:**
```yaml
---
provider: openai
model: o4-mini-deep-research
request_id: resp_abc123...
timestamp: 260111_1430
---
```

## Prerequisites

**Python Packages:**
```bash
pip3 install httpx openai python-dotenv --break-system-packages
```

**Environment Variables:**
```bash
export OPENAI_API_KEY="your-key-here"
export DEEPSEEK_API_KEY="your-key-here"  # If using DeepSeek
```

## Tips & Best Practices

### When to Use Each Script

| Scenario | Use |
|----------|-----|
| Quick research (< 5 min) | `research.py --poll` |
| Long research (10-30 min) | `research.py` then `poll_research.py` |
| Unstable connection | `research.py` then `poll_research.py` |
| Need to disconnect | `research.py` then `poll_research.py` later |
| Check job status | `poll_research.py --check-only` |
| Re-extract from JSON | `extract_json.py` |

### Timeout Strategies

**Default (30 min):**
```bash
python3 poll_research.py REQUEST_ID
```

**Extended (1 hour):**
```bash
python3 poll_research.py REQUEST_ID --timeout 3600
```

**Very long (2 hours):**
```bash
python3 poll_research.py REQUEST_ID --timeout 7200
```

### Error Recovery

**If polling times out:**
```bash
# Just run poll_research.py again - it picks up where it left off
python3 poll_research.py REQUEST_ID --timeout 3600
```

**If you lose the request ID:**
- Check stderr output (if you saved it)
- Look for recent `-raw.json` files in `99-TMP/OUTPUT/`
- Open any raw JSON file and find the `"id"` field at the top level
- Or check the markdown frontmatter for the `request_id` field

**If JSON extraction fails:**
```bash
# Manually extract with the helper script
python3 extract_json.py OUTPUT/file-raw.json OUTPUT/file.md
```

## Output Files

### Raw JSON (`-raw.json`)

Contains the complete OpenAI API response:
- Full output array with reasoning, web searches, and final message
- Metadata (model, status, timing, etc.)
- Useful for debugging or re-processing

### Markdown (`.md`)

Extracted final report with YAML frontmatter:
- YAML frontmatter includes provider, model, request_id, and timestamp
- Clean markdown content from `output_text` field
- Ready for delivery or further processing
- Frontmatter is compatible with Obsidian and other markdown tools

## Advanced Usage

### Custom Output Locations

```bash
python3 research.py \
  --query-file query.md \
  --output /custom/path/report.md \
  --poll
```

**Creates:**
- `/custom/path/report_260111_1430.md` (markdown with timestamp appended)
- `/custom/path/report_260111_1430-raw.json` (JSON with timestamp appended)

**Note:** When using `--output`, the timestamp is automatically appended to your specified filename, and provider/model metadata is added to the frontmatter.

### Verbose Polling

See every poll attempt:

```bash
python3 poll_research.py REQUEST_ID --verbose
```

**Output:**
```
[Poll 1] Status: in_progress (elapsed: 0m10s, timeout: 29m50s)
[Poll 2] Status: in_progress (elapsed: 0m40s, timeout: 29m20s)
[Poll 3] Status: in_progress (elapsed: 1m40s, timeout: 28m20s)
...
```

### Background Processing

Run research in background, check later:

```bash
# Submit and go do something else
python3 research.py --query-file query.md --provider openai > request_id.txt 2>&1

# Come back later and poll
REQUEST_ID=$(grep "Request ID:" request_id.txt | cut -d: -f2 | tr -d ' ')
python3 poll_research.py $REQUEST_ID --output final-report.md
```

## Gamma helpers

`generate_gamma_presentation.py` and `get_gamma_assets.py` now accept `--env-file /path/to/.env` so they can pick up `GAMMA_API_KEY` even when you execute the helpers outside the repository root.

## Troubleshooting

See the main [SKILL.md](../SKILL.md) for detailed troubleshooting section.

**Common issues:**
- cmd.exe errors in WSL → Use full paths (`/usr/bin/python3`)
- Missing modules → `pip3 install httpx openai python-dotenv --break-system-packages`
- Timeout → Increase with `--timeout` or run `poll_research.py` again
- Empty extraction → Check JSON structure with `extract_json.py`

## See Also

- [Main Skill Documentation](../SKILL.md) - Complete deep-research skill guide
- [GitHub Repository](https://github.com/cbruyndoncx/ThirdBrAIn-Tools/tree/main/agentskills/deep-research) - Latest versions
