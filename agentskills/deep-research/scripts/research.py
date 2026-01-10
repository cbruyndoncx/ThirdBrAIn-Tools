# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
# ]
# ///
"""
Unified Deep Research Script - Single command for all providers

Usage:
    uv run research.py "What are the latest AI breakthroughs?" --provider openai --poll
    uv run research.py "Explain quantum computing" --provider deepseek

Providers:
    - openai: O1 models with background processing (auto-polls)
    - deepseek: Synchronous reasoning models (immediate results)
    - anthropic: Claude models with extended thinking (future)
    - google: Gemini with grounding (future)
"""

import sys
import argparse
import os
import httpx
import json
from typing import Tuple, Optional, List
from datetime import datetime
from abc import ABC, abstractmethod
import time


# ============================================================================
# HTTP Client
# ============================================================================

class HTTPClient:
    """Simple HTTP client wrapper with timeout and error handling."""

    def __init__(self, timeout: float = 120.0):
        self.timeout = timeout

    def post(self, url: str, headers: dict, json_data: dict) -> dict:
        """POST request with error handling."""
        try:
            response = httpx.post(
                url,
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")
        except httpx.HTTPStatusError as e:
            error_msg = str(e.response.text)
            raise Exception(f"HTTP {e.response.status_code}: {error_msg}")

    def get(self, url: str, headers: dict) -> dict:
        """GET request with error handling."""
        try:
            response = httpx.get(
                url,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")
        except httpx.HTTPStatusError as e:
            error_msg = str(e.response.text)
            raise Exception(f"HTTP {e.response.status_code}: {error_msg}")


# ============================================================================
# Utilities
# ============================================================================

def get_api_key(provider: str, key_name: str = None) -> str:
    """Get API key from environment."""
    if key_name is None:
        key_name = f"{provider.upper()}_API_KEY"

    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(
            f"API key not found: {key_name}\n"
            f"Please set: export {key_name}=\"your-key\""
        )
    return api_key


def format_markdown_report(
    title: str,
    content: str,
    citations: Optional[list] = None,
    source: Optional[str] = None,
) -> str:
    """Format research output as markdown."""
    md_parts = [f"# {title}\n"]

    if source:
        md_parts.append(f"> Research conducted with {source}\n")

    md_parts.append(content)

    if citations:
        md_parts.append("\n## References\n")
        for i, citation in enumerate(citations, 1):
            if isinstance(citation, dict):
                url = citation.get("url", "")
                title = citation.get("title", "")
                if url:
                    md_parts.append(f"[{i}] {title}: {url}\n")
                else:
                    md_parts.append(f"[{i}] {title}\n")
            else:
                md_parts.append(f"[{i}] {citation}\n")

    return "".join(md_parts)


def ensure_reports_dir() -> str:
    """Ensure research reports directory exists."""
    reports_dir = os.path.join(os.getcwd(), "99-TMP", "OUTPUT")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def print_error(msg: str, file=None) -> None:
    """Print error to stderr."""
    if file is None:
        file = sys.stderr
    print(f"❌ {msg}", file=file)


def print_success(msg: str, file=None) -> None:
    """Print success to stderr."""
    if file is None:
        file = sys.stderr
    print(f"✓ {msg}", file=file)


def print_info(msg: str, verbose: bool = False) -> None:
    """Print info message if verbose."""
    if verbose:
        print(f"ℹ {msg}", file=sys.stderr)


# ============================================================================
# Base Provider
# ============================================================================

class BaseProvider(ABC):
    """Abstract base class for research providers."""

    @abstractmethod
    def create_request(
        self,
        query: str,
        model: Optional[str] = None,
        verbose: bool = False,
    ) -> Tuple[str, str]:
        """
        Create a research request.

        Args:
            query: Research question
            model: Specific model to use (optional)
            verbose: Enable verbose output

        Returns:
            Tuple of (request_id, status)
            where status is "completed" or "in_progress"
        """
        pass

    @abstractmethod
    def get_results(self, request_id: str, output_path: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """
        Get research results.

        Args:
            request_id: Request ID from create_request
            output_path: Optional custom file path to save results

        Returns:
            Tuple of (markdown_report, report_file_path)
        """
        pass

    @abstractmethod
    def check_status(self, request_id: str) -> str:
        """
        Check request status.

        Args:
            request_id: Request ID from create_request

        Returns:
            Status string: "completed", "in_progress", or "failed"
        """
        pass

    def _get_adaptive_poll_interval(self, elapsed_seconds: int) -> int:
        """
        Get adaptive polling interval based on elapsed time.

        Strategy:
        - 0-10s: poll every 10s
        - 10-30s: poll every 30s
        - 30s-5min: poll every 1min
        - 5-30min: poll every 5min

        Args:
            elapsed_seconds: Total elapsed time in seconds

        Returns:
            Poll interval in seconds
        """
        if elapsed_seconds < 10:
            return 10
        elif elapsed_seconds < 30:
            return 30
        elif elapsed_seconds < 300:  # 5 minutes
            return 60
        else:  # 5+ minutes
            return 300

    def poll_until_complete(
        self,
        request_id: str,
        verbose: bool = False,
    ) -> str:
        """
        Poll request until completion with adaptive intervals.

        Polling intervals increase over time:
        - 0-10s: 10s intervals
        - 10-30s: 30s intervals
        - 30s-5min: 1min intervals
        - 5-30min: 5min intervals (max 30 minute timeout)

        Args:
            request_id: Request ID from create_request
            verbose: Enable verbose output

        Returns:
            Final status: "completed" or "failed"
        """
        start_time = time.time()
        poll_num = 0

        while True:
            elapsed = int(time.time() - start_time)
            poll_num += 1

            status = self.check_status(request_id)

            if status == "completed":
                return "completed"
            elif status == "failed":
                return "failed"

            # Calculate remaining time based on 30 min max
            max_timeout = 1800  # 30 minutes
            remaining = max(0, max_timeout - elapsed)

            if verbose:
                elapsed_mins = elapsed // 60
                remaining_mins = remaining // 60
                print(
                    f"  [Poll {poll_num}] Status: {status} "
                    f"(elapsed: {elapsed_mins}m{elapsed%60:02d}s, "
                    f"timeout: {remaining_mins}m{remaining%60:02d}s)",
                    file=sys.stderr,
                )

            # Check if we've exceeded the max timeout
            if elapsed >= max_timeout:
                print(f"  ⏱ Timeout after {elapsed}s", file=sys.stderr)
                return "in_progress"

            # Get adaptive interval and sleep
            interval = self._get_adaptive_poll_interval(elapsed)
            time.sleep(interval)

    def _get_default_model(self) -> str:
        """Get default model for this provider."""
        return "default"


# ============================================================================
# OpenAI Provider
# ============================================================================

class OpenAIProvider(BaseProvider):
    """OpenAI Deep Research provider."""

    def __init__(self):
        self.api_key = get_api_key("openai")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.client = HTTPClient(timeout=120.0)

    def _get_default_model(self) -> str:
        return "o1"

    def create_request(
        self,
        query: str,
        model: Optional[str] = None,
        verbose: bool = False,
    ) -> Tuple[str, str]:
        """Create a research request with OpenAI Deep Research."""
        if not model:
            model = os.getenv("OPENAI_DEFAULT_MODEL", self._get_default_model())

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "input": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
            "tools": [
                {"type": "web_search_preview"},
            ],
            "background": True,  # Enable background processing
        }

        response = self.client.post(
            f"{self.base_url}/responses",
            headers=headers,
            json_data=payload,
        )

        request_id = response.get("id")
        status = response.get("status")

        # Normalize status
        if status == "completed":
            status = "completed"
        else:
            status = "in_progress"

        return request_id, status

    def check_status(self, request_id: str) -> str:
        """Check the status of a research request."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        response = self.client.get(
            f"{self.base_url}/responses/{request_id}",
            headers=headers,
        )

        status = response.get("status", "unknown")

        # Normalize status
        if status in ["processing", "pending"]:
            return "in_progress"
        elif status == "completed":
            return "completed"
        elif status == "failed":
            return "failed"
        else:
            return "in_progress"

    def get_results(self, request_id: str, output_path: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """Retrieve completed research results."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        response = self.client.get(
            f"{self.base_url}/responses/{request_id}",
            headers=headers,
        )

        # Extract report from response
        report_content = self._extract_report(response)

        # Extract citations if available
        citations = self._extract_citations(response)

        # Format as markdown
        markdown = format_markdown_report(
            title="Research Report",
            content=report_content,
            citations=citations,
            source="OpenAI Deep Research",
        )

        # Save to file
        report_file = self._save_report(request_id, markdown, output_path=output_path)

        return markdown, report_file

    def _extract_report(self, response: dict) -> str:
        """Extract report content from response."""
        # OpenAI response structure: response.content[0].research
        try:
            # Handle different response structures
            if "content" in response:
                content = response.get("content")
                if isinstance(content, list) and len(content) > 0:
                    item = content[0]
                    if "research" in item:
                        return item["research"]
                    elif "text" in item:
                        return item["text"]

            # Fallback: try getting report directly
            if "report" in response:
                return response["report"]

            # Last resort: return full response as JSON for debugging
            return f"```json\n{json.dumps(response, indent=2)}\n```"
        except Exception as e:
            return f"Error extracting report: {str(e)}"

    def _extract_citations(self, response: dict) -> list:
        """Extract citations from response."""
        citations = []
        try:
            if "content" in response:
                content = response.get("content")
                if isinstance(content, list) and len(content) > 0:
                    item = content[0]
                    if "citations" in item:
                        citations = item["citations"]
        except Exception:
            pass
        return citations

    def _save_report(self, request_id: str, markdown: str, output_path: Optional[str] = None) -> Optional[str]:
        """Save report to file."""
        try:
            if output_path:
                filepath = output_path
                parent_dir = os.path.dirname(filepath)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)
                    print(f"📁 Created directory: {parent_dir}", file=sys.stderr)
            else:
                reports_dir = ensure_reports_dir()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"openai_{request_id[:8]}_{timestamp}.md"
                filepath = os.path.join(reports_dir, filename)

            with open(filepath, "w") as f:
                f.write(markdown)

            return filepath
        except Exception as e:
            print(f"Warning: Could not save report: {e}")
            return None


# ============================================================================
# DeepSeek Provider
# ============================================================================

class DeepSeekProvider(BaseProvider):
    """DeepSeek reasoning provider."""

    def __init__(self):
        self.api_key = get_api_key("deepseek")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.client = HTTPClient(timeout=300.0)  # Longer timeout for reasoning
        self._results_cache = {}  # Cache results from create_request

    def _get_default_model(self) -> str:
        return "deepseek-reasoner"

    def create_request(
        self,
        query: str,
        model: Optional[str] = None,
        verbose: bool = False,
    ) -> Tuple[str, str]:
        """Create a research request (synchronous, returns immediately)."""
        if not model:
            model = os.getenv("DEEPSEEK_DEFAULT_MODEL", self._get_default_model())

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
            "temperature": 1.0,  # Required for reasoning
            "stream": False,
        }

        response = self.client.post(
            f"{self.base_url}/v1/chat/completions",
            headers=headers,
            json_data=payload,
        )

        # Generate synthetic request ID for consistency
        request_id = f"deepseek_{id(response)}"

        # Cache the result since DeepSeek returns immediately
        self._results_cache[request_id] = {
            "response": response,
            "model": model,
            "query": query,
        }

        # DeepSeek returns immediately
        return request_id, "completed"

    def check_status(self, request_id: str) -> str:
        """Check status (DeepSeek is always completed immediately)."""
        if request_id in self._results_cache:
            return "completed"
        return "in_progress"

    def get_results(self, request_id: str, output_path: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """Retrieve results."""
        if request_id not in self._results_cache:
            return "Error: Request not found (already retrieved?)", None

        cached = self._results_cache.pop(request_id)
        response = cached["response"]

        # Extract reasoning and response
        content = self._extract_content(response)

        # Format as markdown
        markdown = format_markdown_report(
            title="Research Report",
            content=content,
            source="DeepSeek Reasoning",
        )

        # Save to file
        report_file = self._save_report(request_id, markdown, output_path=output_path)

        return markdown, report_file

    def _extract_content(self, response: dict) -> str:
        """Extract content from DeepSeek response."""
        try:
            # Standard OpenAI-compatible response structure
            if "choices" in response:
                choices = response.get("choices", [])
                if len(choices) > 0:
                    message = choices[0].get("message", {})
                    content = message.get("content", "")

                    # If there's reasoning_content, include it
                    reasoning = message.get("reasoning_content", "")
                    if reasoning:
                        return f"## Reasoning\n\n{reasoning}\n\n## Response\n\n{content}"
                    else:
                        return content

            return "Error: Unable to extract response content"
        except Exception as e:
            return f"Error extracting content: {str(e)}"

    def _save_report(self, request_id: str, markdown: str, output_path: Optional[str] = None) -> Optional[str]:
        """Save report to file."""
        try:
            if output_path:
                filepath = output_path
                parent_dir = os.path.dirname(filepath)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)
                    print(f"📁 Created directory: {parent_dir}", file=sys.stderr)
            else:
                reports_dir = ensure_reports_dir()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"deepseek_{request_id[:8]}_{timestamp}.md"
                filepath = os.path.join(reports_dir, filename)

            with open(filepath, "w") as f:
                f.write(markdown)

            return filepath
        except Exception as e:
            print(f"Warning: Could not save report: {e}")
            return None


# ============================================================================
# Main Script
# ============================================================================

def get_provider(provider_name: str):
    """Get provider instance by name."""
    providers = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        # Future providers
        # "anthropic": AnthropicProvider,
        # "google": GoogleProvider,
    }

    if provider_name not in providers:
        available = ", ".join(providers.keys())
        print_error(f"Unknown provider: {provider_name}")
        print_error(f"Available: {available}")
        sys.exit(1)

    return providers[provider_name]()


def main():
    parser = argparse.ArgumentParser(
        description="Deep research across multiple AI providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run research.py "What is quantum computing?" --provider openai --poll
  uv run research.py "Latest AI breakthroughs" --provider deepseek
  uv run research.py "Explain transformers" --provider openai --model o1-mini
        """,
    )

    parser.add_argument(
        "query", nargs="?", help="Research query (or use --query-file)"
    )
    parser.add_argument(
        "--query-file",
        help="Read query from file instead of command line",
    )
    parser.add_argument(
        "--provider",
        default=os.getenv("REASONING_DEFAULT_PROVIDER", "openai"),
        help="AI provider: openai, deepseek (default: $REASONING_DEFAULT_PROVIDER or openai)",
    )
    parser.add_argument(
        "--model",
        help="Specific model (optional, uses provider default if not specified)",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        help="For async providers (OpenAI), auto-poll until complete",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )
    parser.add_argument(
        "--output",
        help="Save results to specified file path",
    )

    args = parser.parse_args()

    # Handle query from file or command line
    if args.query_file:
        try:
            with open(args.query_file, "r") as f:
                query = f.read().strip()
        except FileNotFoundError:
            print_error(f"Query file not found: {args.query_file}")
            sys.exit(1)
        except IOError as e:
            print_error(f"Error reading query file: {e}")
            sys.exit(1)
    elif args.query:
        query = args.query
    else:
        print_error("Must provide either a query or --query-file")
        parser.print_help()
        sys.exit(1)

    try:
        # Get provider
        provider = get_provider(args.provider)

        if args.verbose:
            print(f"Provider: {args.provider}")
            print(f"Query: {query}")
            print()

        # Step 1: Create research request
        print("📋 Creating research request...", file=sys.stderr)
        request_id, status = provider.create_request(
            query=query,
            model=args.model,
            verbose=args.verbose,
        )
        print(f"✓ Request created: {request_id}", file=sys.stderr)

        # Step 2: Check status and poll if needed
        if status == "in_progress" and args.poll:
            print("⏳ Polling for results (adaptive intervals: 10s→30s→1m→5m)...", file=sys.stderr)
            status = provider.poll_until_complete(
                request_id=request_id,
                verbose=args.verbose,
            )

        if status == "completed":
            print("✓ Research complete", file=sys.stderr)
        elif status == "in_progress":
            print_error("Research still in progress. Use --poll to wait for completion.")
            print_error(f"Request ID: {request_id}")
            sys.exit(1)
        elif status == "failed":
            print_error("Research failed")
            sys.exit(1)

        # Step 3: Get results
        print("📥 Retrieving results...", file=sys.stderr)
        report_md, report_file = provider.get_results(request_id=request_id, output_path=args.output)

        # Output the report
        print(report_md)

        if report_file:
            print(f"\n💾 Report saved to: {report_file}", file=sys.stderr)

        print_success("Research complete", file=sys.stderr)

    except KeyboardInterrupt:
        print_error("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
