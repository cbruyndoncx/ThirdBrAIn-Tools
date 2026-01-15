#!/usr/bin/env python3
"""
Gamma Presentation Assets Getter
Retrieve and optionally download presentation exports (PDF, PPTX).

Usage:
    python get_presentation_assets.py --generation-id abc123
    python get_presentation_assets.py --generation-id abc123 --download --output-dir ./exports
"""

import argparse
import json
import os
from dotenv import load_dotenv
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, Optional


_ENV_FILE_PATH: Optional[Path] = None
_ENV_LOADED = False


def ensure_env_loaded(env_file: Optional[str] = None) -> None:
    """Load dotenv configuration once (optionally from a custom path)."""
    global _ENV_FILE_PATH, _ENV_LOADED
    if env_file:
        env_path = Path(env_file).expanduser()
        if not env_path.is_file():
            raise FileNotFoundError(f".env file not found: {env_path}")
        _ENV_FILE_PATH = env_path

    if _ENV_LOADED:
        return

    if _ENV_FILE_PATH:
        load_dotenv(dotenv_path=str(_ENV_FILE_PATH))
    else:
        load_dotenv()

    _ENV_LOADED = True


# Configuration
GAMMA_API_BASE_URL = "https://public-api.gamma.app/v1.0/generations"
GAMMA_API_KEY_HEADER = "X-API-KEY"


def get_api_key() -> str:
    """Get Gamma API key from environment."""
    ensure_env_loaded()

    # Access variables
    api_key = os.getenv("GAMMA_API_KEY")
    if not api_key:
        raise ValueError("GAMMA_API_KEY environment variable not set")
    return api_key


def make_request(url: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Make HTTP GET request to Gamma API."""
    if api_key is None:
        api_key = get_api_key()

    headers = {
        "Accept": "application/json",
        GAMMA_API_KEY_HEADER: api_key,
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {error_body}")


def extract_url(data: Dict[str, Any], export_type: str) -> Optional[str]:
    """Extract specific export URL from API response."""
    # Direct URL properties
    if export_type == "pdf":
        return (
            data.get("pdfUrl")
            or data.get("pdf_url")
            or (isinstance(data.get("exports"), list) and len(data["exports"]) > 0 and data["exports"][0].get("url"))
        )
    elif export_type == "pptx":
        return (
            data.get("pptxUrl")
            or data.get("pptx_url")
            or (isinstance(data.get("exports"), list) and len(data["exports"]) > 1 and data["exports"][1].get("url"))
        )

    return None


def download_file(url: str, output_path: str) -> bool:
    """Download a file from URL to local path."""
    try:
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}", file=sys.stderr)
        return False


def get_presentation_assets(
    generation_id: str, download: bool = False, output_dir: Optional[str] = None, api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Get presentation assets (PDF and PPTX URLs)."""
    if api_key is None:
        api_key = get_api_key()

    try:
        # Fetch generation status and assets
        status_url = f"{GAMMA_API_BASE_URL}/{generation_id}"
        data = make_request(status_url, api_key=api_key)

        result: Dict[str, Any] = {
            "generation_id": generation_id,
        }

        # Extract URLs
        # Try multiple possible locations for export URLs
        exports = None
        pdf_url = None
        pptx_url = None

        # Direct URL fields
        pdf_url = data.get("pdfUrl") or data.get("pdf_url")
        pptx_url = data.get("pptxUrl") or data.get("pptx_url")

        # Try exports array
        if not exports and data.get("exports"):
            exports = data.get("exports")
            if isinstance(exports, list) and len(exports) > 0:
                # Typically PDF is first, PPTX is second
                for i, export in enumerate(exports):
                    if isinstance(export, dict):
                        if export.get("url") and not pdf_url:
                            pdf_url = export.get("url")
                        elif export.get("url") and not pptx_url:
                            pptx_url = export.get("url")
                    elif isinstance(export, str):
                        if not pdf_url:
                            pdf_url = export
                        elif not pptx_url:
                            pptx_url = export

        if pdf_url:
            result["pdf"] = pdf_url

        if pptx_url:
            result["pptx"] = pptx_url

        # Download if requested
        if download and output_dir:
            output_dir_path = Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)

            downloads: Dict[str, Any] = {}

            if pdf_url:
                pdf_path = output_dir_path / f"{generation_id}.pdf"
                if download_file(pdf_url, str(pdf_path)):
                    downloads["pdf"] = str(pdf_path)
                else:
                    downloads["pdf_error"] = f"Failed to download PDF from {pdf_url}"

            if pptx_url:
                pptx_path = output_dir_path / f"{generation_id}.pptx"
                if download_file(pptx_url, str(pptx_path)):
                    downloads["pptx"] = str(pptx_path)
                else:
                    downloads["pptx_error"] = f"Failed to download PPTX from {pptx_url}"

            if downloads:
                result["downloads"] = downloads

        return result

    except Exception as e:
        return {
            "generation_id": generation_id,
            "error": str(e),
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Get presentation assets (PDF/PPTX URLs and optionally download them)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "--generation-id",
        required=True,
        help="The generation ID returned by the generate API",
    )

    # Optional arguments
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the assets to local files",
    )
    parser.add_argument(
        "--output-dir",
        default="99-TMP/OUTPUT",
        help="Directory to download assets to (default: 99-TMP/OUTPUT)",
    )
    parser.add_argument(
        "--env-file",
        help="Path to a .env file so API keys can be loaded from any directory",
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        default=True,
        help="Output as JSON (default: true)",
    )

    args = parser.parse_args()

    ensure_env_loaded(args.env_file)

    # Get assets
    result = get_presentation_assets(
        generation_id=args.generation_id,
        download=args.download,
        output_dir=args.output_dir if args.download else None,
    )

    # Output result
    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            if result.get("pdf"):
                print(f"PDF: {result['pdf']}")
            if result.get("pptx"):
                print(f"PPTX: {result['pptx']}")
            if result.get("downloads"):
                print("\nDownloads:")
                for key, value in result["downloads"].items():
                    if not key.endswith("_error"):
                        print(f"  {key.upper()}: {value}")


if __name__ == "__main__":
    main()
