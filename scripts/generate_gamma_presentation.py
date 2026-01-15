#!/usr/bin/env python3
"""
Gamma Presentation Generator
Generate presentations, documents, social posts, and websites using the Gamma API.

Usage:
    python generate_presentation.py --input-text "Your content" --format presentation
    python generate_presentation.py --input-file ./content.md --format presentation
"""

import argparse
import json
import os
from dotenv import load_dotenv
import sys
import time
from typing import Any, Dict, Optional
import urllib.request
import urllib.error


# Configuration
GAMMA_API_BASE_URL = "https://public-api.gamma.app/v1.0/generations"
GAMMA_API_KEY_HEADER = "X-API-KEY"
TIMEOUT_MS = 10 * 60 * 1000  # 10 minutes
POLL_INTERVAL_MS = 30 * 1000  # 30 seconds


def get_api_key() -> str:
    """Get Gamma API key from environment."""
    # Explicit: load from current working directory
    # from dotenv import load_dotenv
    # from pathlib import Path
    # load_dotenv(Path.cwd() / ".env")

    # Loads .env from current working directory
    load_dotenv()

    # Access variables
    api_key = os.getenv("GAMMA_API_KEY")
    if not api_key:
        raise ValueError("GAMMA_API_KEY environment variable not set")
    return api_key


def make_request(
    url: str, method: str = "POST", body: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Make HTTP request to Gamma API."""
    if api_key is None:
        api_key = get_api_key()

    headers = {
        "Content-Type": "application/json",
        GAMMA_API_KEY_HEADER: api_key,
    }

    body_data = None
    if body:
        body_data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=body_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {error_body}")


def extract_generation_id(data: Dict[str, Any]) -> Optional[str]:
    """Extract generation ID from API response."""
    return data.get("generationId") or data.get("generation_id") or data.get("id")


def extract_url(data: Dict[str, Any]) -> Optional[str]:
    """Extract URL from API response."""
    # Direct URL properties
    direct_url = (
        data.get("gammaUrl")
        or data.get("gamma_url")
        or data.get("url")
        or data.get("exportUrl")
        or data.get("export_url")
        or data.get("outputUrl")
        or data.get("output_url")
    )

    if direct_url:
        return direct_url

    # Check arrays for URLs
    outputs = data.get("outputs", [])
    if outputs and isinstance(outputs, list) and outputs[0]:
        if isinstance(outputs[0], dict) and outputs[0].get("url"):
            return outputs[0]["url"]

    exports = data.get("exports", [])
    if exports and isinstance(exports, list) and exports[0]:
        if isinstance(exports[0], dict) and exports[0].get("url"):
            return exports[0]["url"]
        if isinstance(exports[0], str):
            return exports[0]

    artifacts = data.get("artifacts", [])
    if artifacts and isinstance(artifacts, list) and artifacts[0]:
        if isinstance(artifacts[0], dict) and artifacts[0].get("url"):
            return artifacts[0]["url"]

    return None


def is_completed(status: str) -> bool:
    """Check if generation status is completed."""
    status_lower = status.lower()
    return status_lower in ["completed", "succeeded"]


def is_failed(status: str) -> bool:
    """Check if generation status is failed."""
    status_lower = status.lower()
    return status_lower in ["failed", "error"]


def poll_generation_status(generation_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Poll generation status until completion or timeout."""
    if api_key is None:
        api_key = get_api_key()

    start = time.time() * 1000  # Convert to milliseconds
    poll_interval_sec = POLL_INTERVAL_MS / 1000
    timeout_sec = TIMEOUT_MS / 1000

    while (time.time() * 1000) - start < TIMEOUT_MS:
        try:
            status_url = f"{GAMMA_API_BASE_URL}/{generation_id}"
            data = make_request(status_url, method="GET", api_key=api_key)

            status = (data.get("status") or data.get("state") or "").lower()

            if is_completed(status):
                url = extract_url(data)
                if url:
                    return {
                        "url": url,
                        "generation_id": generation_id,
                        "error": None,
                    }
                return {
                    "url": None,
                    "generation_id": generation_id,
                    "error": f"Generation completed but no export URL found: {json.dumps(data)}",
                }

            if is_failed(status):
                return {
                    "url": None,
                    "generation_id": generation_id,
                    "error": f"Generation failed: {json.dumps(data)}",
                }

            time.sleep(poll_interval_sec)

        except Exception as e:
            # Continue polling on errors
            time.sleep(poll_interval_sec)

    return {
        "url": None,
        "generation_id": generation_id,
        "error": f"Timed out waiting for generation {generation_id}",
    }


def generate_presentation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a presentation using the Gamma API."""

    api_key  = get_api_key()

    # Build request body
    body: Dict[str, Any] = {
        "inputText": params["input_text"],
        "textMode": params.get("text_mode", "generate"),
    }

    # Optional fields
    if params.get("format"):
        body["format"] = params["format"]
    if params.get("num_cards"):
        body["numCards"] = params["num_cards"]
    if params.get("export_as"):
        body["exportAs"] = params["export_as"]
    if params.get("card_split"):
        body["cardSplit"] = params["card_split"]
    if params.get("theme_id"):
        body["themeId"] = params["theme_id"]
    if params.get("folder_ids"):
        body["folderIds"] = params["folder_ids"]
    if params.get("additional_instructions"):
        body["additionalInstructions"] = params["additional_instructions"]

    # Nested options
    text_options: Dict[str, Any] = {}
    if params.get("text_amount"):
        text_options["amount"] = params["text_amount"]
    if params.get("text_tone"):
        text_options["tone"] = params["text_tone"]
    if params.get("text_audience"):
        text_options["audience"] = params["text_audience"]
    if params.get("text_language"):
        text_options["language"] = params["text_language"]
    if text_options:
        body["textOptions"] = text_options

    image_options: Dict[str, Any] = {}
    if params.get("image_source"):
        image_options["source"] = params["image_source"]
    if params.get("image_model"):
        image_options["model"] = params["image_model"]
    if params.get("image_style"):
        image_options["style"] = params["image_style"]
    if image_options:
        body["imageOptions"] = image_options

    card_options: Dict[str, Any] = {}
    if params.get("card_dimensions"):
        card_options["dimensions"] = params["card_dimensions"]
    if params.get("card_header_footer"):
        card_options["headerFooter"] = params["card_header_footer"]
    if card_options:
        body["cardOptions"] = card_options

    sharing_options: Dict[str, Any] = {}
    if params.get("sharing_workspace_access"):
        sharing_options["workspaceAccess"] = params["sharing_workspace_access"]
    if params.get("sharing_external_access"):
        sharing_options["externalAccess"] = params["sharing_external_access"]
    if params.get("sharing_email_options"):
        sharing_options["emailOptions"] = params["sharing_email_options"]
    if sharing_options:
        body["sharingOptions"] = sharing_options

    try:
        # Submit generation request
        response = make_request(GAMMA_API_BASE_URL, method="POST", body=body, api_key=api_key)

        generation_id = extract_generation_id(response)
        if not generation_id:
            return {
                "url": None,
                "generation_id": None,
                "error": f"Failed to extract generation ID from response: {json.dumps(response)}",
            }

        # Poll for completion
        result = poll_generation_status(generation_id, api_key=api_key)
        return result

    except Exception as e:
        return {
            "url": None,
            "generation_id": None,
            "error": str(e),
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a presentation using the Gamma API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input arguments (one required)
    parser.add_argument(
        "--input-text",
        help="The content for the presentation (text and image URLs)",
    )
    parser.add_argument(
        "--input-file",
        help="Path to a file containing the presentation content. If provided, file content will be used instead of --input-text.",
    )

    # Optional arguments
    parser.add_argument(
        "--text-mode",
        default="generate",
        choices=["generate", "condense", "preserve"],
        help="Text mode (default: generate)",
    )
    parser.add_argument(
        "--format",
        default="presentation",
        choices=["presentation", "document", "social", "webpage"],
        help="Format to create (default: presentation)",
    )
    parser.add_argument(
        "--num-cards",
        type=int,
        help="Number of cards/slides to generate",
    )
    parser.add_argument(
        "--export-as",
        choices=["pdf", "pptx"],
        help="Export format",
    )
    parser.add_argument(
        "--card-split",
        choices=["auto", "inputTextBreaks"],
        help="Card split mode",
    )
    parser.add_argument(
        "--theme-id",
        help="Theme ID to apply",
    )
    parser.add_argument(
        "--additional-instructions",
        help="Custom instructions for generation (text)",
    )
    parser.add_argument(
        "--additional-instructions-file",
        help="Path to a file containing custom instructions. If provided, file content will be used instead of --additional-instructions.",
    )
    parser.add_argument(
        "--text-amount",
        choices=["brief", "medium", "detailed", "extensive"],
        help="Content detail level",
    )
    parser.add_argument(
        "--text-tone",
        help="Voice/style (e.g., 'professional and confident')",
    )
    parser.add_argument(
        "--text-audience",
        help="Target audience (e.g., 'executives')",
    )
    parser.add_argument(
        "--text-language",
        help="Output language code (e.g., 'en', 'es', 'fr')",
    )
    parser.add_argument(
        "--image-source",
        choices=[
            "aiGenerated",
            "pictographic",
            "unsplash",
            "giphy",
            "webAllImages",
            "webFreeToUse",
            "webFreeToUseCommercially",
            "placeholder",
            "noImages",
        ],
        help="Image source",
    )
    parser.add_argument(
        "--image-model",
        help="AI model for image generation",
    )
    parser.add_argument(
        "--image-style",
        help="Visual style for images",
    )
    parser.add_argument(
        "--card-dimensions",
        help="Card dimensions (format-specific)",
    )
    parser.add_argument(
        "--card-header-footer",
        type=json.loads,
        help="Header/footer configuration as JSON",
    )
    parser.add_argument(
        "--folder-ids",
        type=json.loads,
        help="Folder IDs as JSON array",
    )
    parser.add_argument(
        "--sharing-workspace-access",
        choices=["noAccess", "view", "comment", "edit", "fullAccess"],
        help="Workspace access level",
    )
    parser.add_argument(
        "--sharing-external-access",
        choices=["noAccess", "view", "comment", "edit"],
        help="External access level",
    )
    parser.add_argument(
        "--sharing-email-options",
        type=json.loads,
        help="Email sharing options as JSON",
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        default=True,
        help="Output as JSON (default: true)",
    )

    args = parser.parse_args()

    # Validate and read input
    input_text = None
    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception as e:
            print(f"Error reading file {args.input_file}: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.input_text:
        input_text = args.input_text
    else:
        parser.error("Either --input-text or --input-file is required")

    # Read additional instructions if provided
    additional_instructions = None
    if args.additional_instructions_file:
        try:
            with open(args.additional_instructions_file, "r", encoding="utf-8") as f:
                additional_instructions = f.read()
        except Exception as e:
            print(f"Error reading file {args.additional_instructions_file}: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.additional_instructions:
        additional_instructions = args.additional_instructions

    # Convert args to params dict
    params = {
        "input_text": input_text,
        "text_mode": args.text_mode,
        "format": args.format,
        "num_cards": args.num_cards,
        "export_as": args.export_as,
        "card_split": args.card_split,
        "theme_id": args.theme_id,
        "additional_instructions": additional_instructions,
        "text_amount": args.text_amount,
        "text_tone": args.text_tone,
        "text_audience": args.text_audience,
        "text_language": args.text_language,
        "image_source": args.image_source,
        "image_model": args.image_model,
        "image_style": args.image_style,
        "card_dimensions": args.card_dimensions,
        "card_header_footer": args.card_header_footer,
        "folder_ids": args.folder_ids,
        "sharing_workspace_access": args.sharing_workspace_access,
        "sharing_external_access": args.sharing_external_access,
        "sharing_email_options": args.sharing_email_options,
    }

    # Generate presentation
    result = generate_presentation(params)

    # Output result
    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        if result["error"]:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"URL: {result['url']}")
            print(f"Generation ID: {result['generation_id']}")


if __name__ == "__main__":
    main()
