#!/usr/bin/env python3
"""
Poll OpenAI Deep Research Request

Polls an OpenAI deep research request until completion, then saves results.
Useful for reconnecting to long-running research jobs.

Usage:
    python3 poll_research.py REQUEST_ID [--output OUTPUT_FILE] [--verbose]

Examples:
    # Poll and auto-save
    python3 poll_research.py resp_abc123

    # Poll and save to specific file
    python3 poll_research.py resp_abc123 --output research-report.md

    # Poll with verbose output
    python3 poll_research.py resp_abc123 --verbose

Environment:
    OPENAI_API_KEY - Required API key
"""

import sys
import argparse
import os
import httpx
import json
import time
from datetime import datetime


def get_api_key():
    """Get OpenAI API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set", file=sys.stderr)
        print("   Please set: export OPENAI_API_KEY=\"your-key\"", file=sys.stderr)
        sys.exit(1)
    return api_key


def check_status(request_id: str, api_key: str, base_url: str = "https://api.openai.com/v1") -> dict:
    """Check the status of a research request."""
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = httpx.get(
            f"{base_url}/responses/{request_id}",
            headers=headers,
            timeout=120.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking status: {e}", file=sys.stderr)
        sys.exit(1)


def get_adaptive_poll_interval(elapsed_seconds: int) -> int:
    """
    Get adaptive polling interval based on elapsed time.

    Strategy:
    - 0-10s: poll every 10s
    - 10-30s: poll every 30s
    - 30s-5min: poll every 1min
    - 5-30min: poll every 5min
    """
    if elapsed_seconds < 10:
        return 10
    elif elapsed_seconds < 30:
        return 30
    elif elapsed_seconds < 300:  # 5 minutes
        return 60
    else:  # 5+ minutes
        return 300


def poll_until_complete(request_id: str, api_key: str, verbose: bool = False, max_timeout: int = 1800) -> dict:
    """
    Poll request until completion with adaptive intervals.

    Args:
        request_id: OpenAI request ID
        api_key: OpenAI API key
        verbose: Show detailed polling progress
        max_timeout: Maximum timeout in seconds (default: 1800 = 30 min)

    Returns:
        Final response dict when completed
    """
    start_time = time.time()
    poll_num = 0
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    print(f"⏳ Polling request: {request_id}", file=sys.stderr)
    print(f"   Max timeout: {max_timeout // 60} minutes", file=sys.stderr)
    print(f"   Adaptive intervals: 10s → 30s → 1m → 5m", file=sys.stderr)
    print("", file=sys.stderr)

    while True:
        elapsed = int(time.time() - start_time)
        poll_num += 1

        # Check status
        response = check_status(request_id, api_key, base_url)
        status = response.get("status", "unknown")

        # Normalize status
        if status in ["processing", "pending"]:
            normalized_status = "in_progress"
        elif status == "completed":
            normalized_status = "completed"
        elif status == "failed":
            normalized_status = "failed"
        else:
            normalized_status = "in_progress"

        # Calculate remaining time
        remaining = max(0, max_timeout - elapsed)

        if verbose or poll_num % 5 == 0:  # Show every 5th poll if not verbose
            elapsed_mins = elapsed // 60
            remaining_mins = remaining // 60
            print(
                f"  [Poll {poll_num}] Status: {status} "
                f"(elapsed: {elapsed_mins}m{elapsed%60:02d}s, "
                f"timeout: {remaining_mins}m{remaining%60:02d}s)",
                file=sys.stderr,
            )

        # Check completion
        if normalized_status == "completed":
            print(f"✓ Research completed after {elapsed}s ({poll_num} polls)", file=sys.stderr)
            return response
        elif normalized_status == "failed":
            print(f"❌ Research failed", file=sys.stderr)
            sys.exit(1)

        # Check timeout
        if elapsed >= max_timeout:
            print(f"⏱ Timeout after {elapsed}s", file=sys.stderr)
            print(f"   Request still in progress. You can poll again later with:", file=sys.stderr)
            print(f"   python3 poll_research.py {request_id}", file=sys.stderr)
            sys.exit(1)

        # Adaptive sleep
        interval = get_adaptive_poll_interval(elapsed)
        time.sleep(interval)


def extract_markdown_from_response(response: dict) -> str:
    """
    Extract markdown content from OpenAI response.

    Handles the nested structure:
    response.output[] -> type="message" -> content[] -> type="output_text" -> text
    """
    try:
        # Check for output array (new structure)
        if "output" in response:
            for item in response.get("output", []):
                if item.get("type") == "message":
                    for content_item in item.get("content", []):
                        if content_item.get("type") == "output_text":
                            return content_item.get("text", "")

        # Fallback: check old structure (content array)
        if "content" in response:
            content = response.get("content")
            if isinstance(content, list) and len(content) > 0:
                item = content[0]
                if "research" in item:
                    return item["research"]
                elif "text" in item:
                    return item["text"]

        # Last resort: return error
        return f"❌ Could not extract markdown from response\n\nFull response:\n```json\n{json.dumps(response, indent=2)}\n```"

    except Exception as e:
        return f"❌ Error extracting markdown: {e}\n\nFull response:\n```json\n{json.dumps(response, indent=2)}\n```"


def save_raw_json(response: dict, request_id: str, model: str = "unknown", output_file: str = None) -> str:
    """Save raw JSON response to file."""
    timestamp = datetime.now().strftime("%y%m%d_%H%M")

    if output_file:
        # If output file specified, append timestamp and add -raw.json suffix
        base = output_file.rsplit(".", 1)[0]
        filepath = f"{base}_{timestamp}-raw.json"
    else:
        # Auto-generate filename
        reports_dir = os.path.join(os.getcwd(), "99-TMP", "OUTPUT")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"openai_{model}_{timestamp}-raw.json"
        filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w") as f:
        json.dump(response, f, indent=2)

    return filepath


def save_markdown(markdown: str, request_id: str, model: str = "unknown", output_file: str = None) -> str:
    """Save markdown report to file."""
    timestamp = datetime.now().strftime("%y%m%d_%H%M")

    if output_file:
        # If output file specified, append timestamp before extension
        base = output_file.rsplit(".", 1)[0]
        ext = output_file.rsplit(".", 1)[1] if "." in output_file else "md"
        filepath = f"{base}_{timestamp}.{ext}"
        parent_dir = os.path.dirname(filepath)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    else:
        # Auto-generate filename
        reports_dir = os.path.join(os.getcwd(), "99-TMP", "OUTPUT")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"openai_{model}_{timestamp}.md"
        filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w") as f:
        f.write(markdown)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Poll OpenAI Deep Research request until completion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 poll_research.py resp_abc123
  python3 poll_research.py resp_abc123 --output report.md --verbose
  python3 poll_research.py resp_abc123 --timeout 3600  # 1 hour timeout
        """,
    )

    parser.add_argument("request_id", help="OpenAI request ID (e.g., resp_abc123)")
    parser.add_argument("--output", "-o", help="Output file path for markdown report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed polling progress")
    parser.add_argument("--timeout", type=int, default=1800, help="Maximum timeout in seconds (default: 1800 = 30 min)")
    parser.add_argument("--check-only", action="store_true", help="Only check status, don't poll")

    args = parser.parse_args()

    try:
        api_key = get_api_key()

        if args.check_only:
            # Just check status once
            print(f"📋 Checking status of: {args.request_id}", file=sys.stderr)
            response = check_status(args.request_id, api_key)
            status = response.get("status", "unknown")
            print(f"   Status: {status}", file=sys.stderr)
            print("", file=sys.stderr)
            print(json.dumps(response, indent=2))
            sys.exit(0)

        # Poll until complete
        response = poll_until_complete(
            request_id=args.request_id,
            api_key=api_key,
            verbose=args.verbose,
            max_timeout=args.timeout,
        )

        # Extract model from response
        model = response.get("model", "unknown")
        timestamp = datetime.now().strftime("%y%m%d_%H%M")

        # Save raw JSON
        print("", file=sys.stderr)
        print("💾 Saving results...", file=sys.stderr)
        raw_json_file = save_raw_json(response, args.request_id, model=model, output_file=args.output)
        print(f"   Raw JSON: {raw_json_file}", file=sys.stderr)

        # Extract markdown and add frontmatter
        markdown_content = extract_markdown_from_response(response)
        frontmatter = f"""---
provider: openai
model: {model}
request_id: {args.request_id}
timestamp: {timestamp}
---

"""
        markdown = frontmatter + markdown_content
        markdown_file = save_markdown(markdown, args.request_id, model=model, output_file=args.output)
        print(f"   Markdown: {markdown_file}", file=sys.stderr)

        # Print summary
        print("", file=sys.stderr)
        print(f"✓ Research completed successfully", file=sys.stderr)
        print(f"  Characters: {len(markdown):,}", file=sys.stderr)
        print(f"  Files saved:", file=sys.stderr)
        print(f"    - {markdown_file}", file=sys.stderr)
        print(f"    - {raw_json_file}", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
