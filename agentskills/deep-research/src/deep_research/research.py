#!/usr/bin/env python3
"""
Unified Deep Research Script - Single command for all providers

Usage:
    uvx research "What are the latest AI breakthroughs?" --provider openai --poll
    uvx research "Explain quantum computing" --provider deepseek

Providers:
    - openai: O1 models with background processing (auto-polls)
    - deepseek: Synchronous reasoning models (immediate results)
    - anthropic: Claude models with extended thinking (future)
    - google: Gemini with grounding (future)
"""

import sys
import argparse
import os

from .providers.openai import OpenAIProvider
from .providers.deepseek import DeepSeekProvider
from .shared.utils import print_error, print_success


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
  research "What is quantum computing?" --provider openai --poll
  research "Latest AI breakthroughs" --provider deepseek
  research "Explain transformers" --provider openai --model o1-mini
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
        report_md, report_file = provider.get_results(request_id=request_id)

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
