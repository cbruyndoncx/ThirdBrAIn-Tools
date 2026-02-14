#!/usr/bin/env -S uv run --quiet --script

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "google-generativeai",
#   "pillow",
#   "python-dotenv",
# ]
# ///

"""
NanoBanana: Gemini image generation/editing for ThirdBrAIn-Tools.

Usage:
    uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "isometric cyberpunk office" --size 1024x1024
    uvx --from "git+https://github.com/cbruyndoncx/ThirdBrAIn-Tools[nanobanana]" nanobanana --prompt "edit this photo" --input photo.jpg

Alternative (direct script):
    uv run https://raw.githubusercontent.com/cbruyndoncx/ThirdBrAIn-Tools/main/scripts/nanobanana.py --prompt "your prompt"
"""

import argparse
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

ENV_PATHS = [
    Path.home() / ".nanobanana.env",
    Path(".env"),
]

for p in ENV_PATHS:
    if p.exists():
        load_dotenv(p)
        break

API_KEY = os.getenv("GEMINI_API_KEY")

MODELS = {
    "gemini-3-pro-image-preview": "gemini-3.0-pro-preview-image",
    "gemini-2.5-flash-image": "gemini-2.5-flash-exp-image-generation",
}

SIZES = {
    "1024x1024": (1024, 1024),
    "832x1248": (832, 1248),
    "1248x832": (1248, 832),
    "864x1184": (864, 1184),
    "1184x864": (1184, 864),
    "896x1152": (896, 1152),
    "1152x896": (1152, 896),
    "768x1344": (768, 1344),
    "1344x768": (1344, 768),
    "1536x672": (1536, 672),
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="NanoBanana: Gemini image generation/editing"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Text description of the desired image/edit",
    )
    parser.add_argument(
        "--input",
        nargs="*",
        help="Optional input image(s) for editing",
    )
    parser.add_argument(
        "--output",
        help="Output PNG path (default: nanobanana-<id>.png)",
    )
    parser.add_argument(
        "--model",
        default="gemini-3-pro-image-preview",
        choices=list(MODELS),
        help="Gemini image model",
    )
    parser.add_argument(
        "--size",
        default="768x1344",
        choices=list(SIZES),
        help="Base resolution preset",
    )
    parser.add_argument(
        "--resolution",
        default="1K",
        choices=["1K", "2K", "4K"],
        help="Scale factor for base resolution",
    )
    return parser.parse_args()

def ensure_api_key() -> str:
    if not API_KEY:
        raise SystemExit(
            "GEMINI_API_KEY not set. Add it to ~/.nanobanana.env or .env"
        )
    return API_KEY

def compute_size(size_key: str, resolution: str) -> tuple[int, int]:
    w, h = SIZES[size_key]
    mult = {"1K": 1, "2K": 2, "4K": 4}[resolution]
    return w * mult, h * mult

def main() -> None:
    args = parse_args()
    ensure_api_key()

    genai.configure(api_key=API_KEY)

    model_name = MODELS[args.model]
    width, height = compute_size(args.size, args.resolution)

    model = genai.GenerativeModel(model_name)

    if args.input:
        images = [Image.open(Path(p).expanduser()) for p in args.input]
        response = model.generate_images(
            prompt=args.prompt,
            image_count=1,
            width=width,
            height=height,
            input_images=images,
        )
    else:
        response = model.generate_images(
            prompt=args.prompt,
            image_count=1,
            width=width,
            height=height,
        )

    img = response.images[0]._pil_image
    out_path = Path(args.output or f"nanobanana-{uuid.uuid4().hex[:8]}.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)

    print(f"Saved: {out_path.resolve()} ({img.size[0]}x{img.size[1]})")

if __name__ == "__main__":
    main()
