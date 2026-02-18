# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai>=1.0.0",
#     "Pillow>=10.0.0",
# ]
# ///
"""
Nano Banana — Gemini image generation, style extraction, and style library.

Single-file module for Claude Code. Reads GEMINI_API_KEY from the environment.

Usage (imported by Claude Code):
    import nano_banana as nb
    nb.new_session()
    nb.generate("a banana on a beach chair")
    nb.extract_style("path/to/image.png")
    nb.get_style(3)
    nb.list_styles()

Usage (CLI):
    uv run nano_banana.py generate "a banana on a beach chair" [--model MODEL]
    uv run nano_banana.py extract path/to/image.png
    uv run nano_banana.py models
    uv run nano_banana.py styles --list
    uv run nano_banana.py styles 3
    uv run nano_banana.py session
    uv run nano_banana.py revert
"""

import base64
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SESSION_FILE = ".image_session.json"
OUTPUT_DIR = "outputs"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_RESOLUTION = "1K"
VISION_MODEL = "gemini-2.5-pro"

STYLE_EXTRACTION_PROMPT = """Analyze this image and deconstruct its complete visual style. I want to be able to recreate this exact aesthetic for completely different subjects.

Describe in detail:

**Color Palette:** What are the dominant colors? Secondary colors? Describe the color temperature (warm, cool, neutral), saturation levels, and any notable color relationships or contrasts. Are there specific hex codes or color names that define this look?

**Lighting:** What type of lighting is used? Describe the direction, quality (soft, hard, diffused), color temperature of the light, shadows, highlights, and any atmospheric lighting effects like rim light, backlighting, or volumetric rays.

**Composition & Framing:** How is the image composed? Describe the perspective, camera angle, focal length feel (wide, telephoto, macro), depth of field, rule of thirds usage, leading lines, symmetry, or any other compositional techniques.

**Textures & Materials:** What surface qualities are present? Describe any grain, noise, smoothness, glossiness, or material properties that define the look.

**Mood & Atmosphere:** What emotional tone does this convey? Describe the overall vibe, energy level, and feeling the viewer gets.

**Artistic Style:** Is this photorealistic, illustrated, painterly, graphic, retro, futuristic, minimal, maximalist? What art movement or design era does it reference, if any?

**Typography & Graphics:** If text or graphic elements are present, describe the font style, weight, treatment, and how it integrates with the image.

**Special Effects:** Any glows, blurs, distortions, overlays, duotone treatments, or post-processing effects?

Write this as a cohesive style guide I can reference when generating new images. Be specific enough that someone could recreate this aesthetic without seeing the original."""

# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


def _get_client():
    """Initialize Gemini client with GEMINI_API_KEY from the environment.

    Temporarily clears GOOGLE_API_KEY so the SDK doesn't override
    our explicit key with it.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")
    google_key_backup = os.environ.pop("GOOGLE_API_KEY", None)
    try:
        client = genai.Client(api_key=api_key)
    finally:
        if google_key_backup:
            os.environ["GOOGLE_API_KEY"] = google_key_backup
    return client


# ---------------------------------------------------------------------------
# Image generation — session helpers
# ---------------------------------------------------------------------------


def _ensure_output_dir():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)


def _load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"history": [], "outputs": [], "turn": 0}


def _save_session(session):
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f)


def _reconstruct_history(raw_history):
    """Convert raw history dicts back to types.Content objects.

    Preserves thought signatures needed for multi-turn continuity.
    """
    reconstructed = []
    for item in raw_history:
        parts = []
        for part_data in item.get("parts", []):
            if "text" in part_data:
                part_kwargs = {"text": part_data["text"]}
                if "thought_signature" in part_data:
                    part_kwargs["thought_signature"] = base64.b64decode(
                        part_data["thought_signature"]
                    )
                parts.append(types.Part(**part_kwargs))
            elif "inline_data" in part_data:
                blob = types.Blob(
                    mime_type=part_data["inline_data"]["mime_type"],
                    data=base64.b64decode(part_data["inline_data"]["data"]),
                )
                part_kwargs = {"inline_data": blob}
                if "thought_signature" in part_data:
                    part_kwargs["thought_signature"] = base64.b64decode(
                        part_data["thought_signature"]
                    )
                parts.append(types.Part(**part_kwargs))
        reconstructed.append(types.Content(role=item.get("role"), parts=parts))
    return reconstructed


def _get_next_output_path(session):
    _ensure_output_dir()
    turn = session.get("turn", 0) + 1
    timestamp = datetime.now().strftime("%H%M%S")
    return f"{OUTPUT_DIR}/output_{turn:03d}_{timestamp}.png"


# ---------------------------------------------------------------------------
# Image generation — public API
# ---------------------------------------------------------------------------


def new_session():
    """Clear the current session and start fresh."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    print("Session cleared. Ready for new image generation.")
    return {"history": [], "outputs": [], "turn": 0}


def session_info():
    """Display current session status."""
    session = _load_session()
    turn_count = session.get("turn", 0)
    outputs = session.get("outputs", [])

    if turn_count == 0:
        print("No active session. Start generating to create one.")
        return None

    print(f"Current session: {turn_count} turn(s)")
    print("Outputs generated:")
    for i, output in enumerate(outputs, 1):
        print(f"  {i}. {output}")
    return session


def revert(turns: int = 1):
    """Undo the last N turns from the current session."""
    session = _load_session()
    turn_count = session.get("turn", 0)

    if turn_count == 0:
        print("No active session to revert.")
        return None

    if turns > turn_count:
        print(f"Can only revert {turn_count} turn(s). Reverting all.")
        turns = turn_count

    session["history"] = session["history"][: -(turns * 2)]
    session["outputs"] = session["outputs"][:-turns]
    session["turn"] = turn_count - turns
    _save_session(session)

    if session["turn"] == 0:
        print(f"Reverted {turns} turn(s). Session is now empty.")
    else:
        print(f"Reverted {turns} turn(s). Now at turn {session['turn']}.")
        print(f"Last output: {session['outputs'][-1] if session['outputs'] else 'None'}")
    return session


def _is_imagen_model(model: str) -> bool:
    """Check if a model ID refers to an Imagen model."""
    return "imagen" in model.lower()


def _generate_imagen(
    prompt: str,
    aspect_ratio: str,
    model: str,
    output: str = None,
    number_of_images: int = 1,
) -> str:
    """Generate an image using the Imagen API (no session/chat support).

    Returns:
        Path to the generated image.
    """
    client = _get_client()
    session = _load_session()

    print(f"Generating with Imagen model: {model}")
    result = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=number_of_images,
            aspect_ratio=aspect_ratio,
        ),
    )

    output_path = None
    for img in result.generated_images:
        if output:
            output_path = output
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = _get_next_output_path(session)
        img.image.save(output_path)
        print(f"Saved: {output_path}")
        session["turn"] = session.get("turn", 0) + 1
        session["outputs"].append(output_path)

    session["history"].append({"role": "user", "parts": [{"text": prompt}]})
    session["history"].append({"role": "model", "parts": [{"text": f"[Imagen: {output_path}]"}]})
    _save_session(session)
    return output_path


def generate(
    prompt: str,
    reference_images: list = None,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    model: str = DEFAULT_MODEL,
    output: str = None,
) -> str:
    """Generate or refine an image. Automatically continues existing session.

    Routes to the Imagen API for imagen-* models, or the Gemini chat API
    for gemini-* models.

    Args:
        prompt: Text description of what to generate/change.
        reference_images: Optional list of image paths to use as references.
        aspect_ratio: "1:1", "3:4", "16:9", etc.
        resolution: "1K", "2K", or "4K".
        model: Model ID (default gemini-3-pro-image-preview).
        output: Custom output path. If None, auto-generates in outputs/.

    Returns:
        Path to the generated image.
    """
    # Imagen models use a separate API
    if _is_imagen_model(model):
        return _generate_imagen(prompt, aspect_ratio=aspect_ratio, model=model, output=output)

    client = _get_client()
    session = _load_session()

    content_parts = [prompt]

    if reference_images:
        from PIL import Image

        for img_path in reference_images:
            if os.path.exists(img_path):
                content_parts.append(Image.open(img_path))
            else:
                print(f"Warning: Reference image not found: {img_path}")

    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspectRatio=aspect_ratio),
    )

    if session["history"]:
        print(f"Continuing session (turn {session['turn'] + 1})...")
        reconstructed_history = _reconstruct_history(session["history"])
        chat = client.chats.create(
            model=model, config=config, history=reconstructed_history
        )
        response = chat.send_message(content_parts)
        session["history"].append({"role": "user", "parts": [{"text": prompt}]})
    else:
        print("Starting new session...")
        chat = client.chats.create(model=model, config=config)
        response = chat.send_message(content_parts)
        session["history"].append({"role": "user", "parts": [{"text": prompt}]})

    output_path = None
    response_parts = []

    for part in response.parts:
        if part.text is not None:
            print(f"Model: {part.text}")
            part_data = {"text": part.text}
            if hasattr(part, "thought_signature") and part.thought_signature:
                part_data["thought_signature"] = base64.b64encode(
                    part.thought_signature
                ).decode("utf-8")
            response_parts.append(part_data)
        elif part.inline_data is not None:
            if output:
                output_path = output
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = _get_next_output_path(session)
            image = part.as_image()
            image.save(output_path)
            print(f"Saved: {output_path}")

            part_data = {
                "inline_data": {
                    "mime_type": part.inline_data.mime_type,
                    "data": base64.b64encode(part.inline_data.data).decode("utf-8"),
                }
            }
            if hasattr(part, "thought_signature") and part.thought_signature:
                part_data["thought_signature"] = base64.b64encode(
                    part.thought_signature
                ).decode("utf-8")
            response_parts.append(part_data)

    session["history"].append({"role": "model", "parts": response_parts})
    session["turn"] = session.get("turn", 0) + 1
    if output_path:
        session["outputs"].append(output_path)
    _save_session(session)

    return output_path


gen = generate  # convenience alias


# ---------------------------------------------------------------------------
# Style extraction
# ---------------------------------------------------------------------------


def extract_style(image_path: str, custom_prompt: str = None) -> str:
    """Extract detailed style information from an image.

    Args:
        image_path: Path to the image to analyze.
        custom_prompt: Optional custom extraction prompt.

    Returns:
        Detailed style description as text.
    """
    from PIL import Image

    client = _get_client()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path)
    prompt = custom_prompt or STYLE_EXTRACTION_PROMPT

    print(f"Analyzing style of: {image_path}")
    print("This may take a moment...")

    response = client.models.generate_content(
        model=VISION_MODEL, contents=[prompt, image]
    )

    style_description = response.text

    print("\n" + "=" * 60)
    print("STYLE EXTRACTION COMPLETE")
    print("=" * 60 + "\n")
    print(style_description)

    return style_description


def extract_and_save(image_path: str, output_path: str = None) -> str:
    """Extract style and save to a markdown file.

    Args:
        image_path: Path to the image to analyze.
        output_path: Where to save (auto-generated if not provided).

    Returns:
        Path to the saved style guide.
    """
    style_description = extract_style(image_path)

    if not output_path:
        image_name = Path(image_path).stem
        output_path = f"styles/{image_name}_style.md"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(f"# Style Guide: {Path(image_path).name}\n\n")
        f.write(f"*Extracted from: `{image_path}`*\n\n")
        f.write("---\n\n")
        f.write(style_description)

    print(f"\nStyle guide saved to: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Style library
# ---------------------------------------------------------------------------


def _find_style_library() -> Path:
    """Locate style-library.html relative to this script."""
    html_path = Path(__file__).parent.parent / "style-library" / "style-library.html"
    if not html_path.exists():
        # Fall back to sibling directory (if script is at repo root)
        html_path = Path(__file__).parent / "style-library" / "style-library.html"
    if not html_path.exists():
        raise FileNotFoundError(f"style-library.html not found at {html_path}")
    return html_path


def get_style(style_id: int) -> dict:
    """Get a style by ID from the style library.

    Args:
        style_id: The style number to retrieve.

    Returns:
        Dictionary with style info (id, name, prompt, category, etc.)
    """
    content = _find_style_library().read_text()

    match = re.search(r"const styles = \[(.*?)\];", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find styles array in style-library.html")

    style_pattern = re.compile(r"\{[^{}]*\}", re.DOTALL)
    for style_str in style_pattern.findall(match.group(1)):
        id_match = re.search(r"id:\s*(\d+)", style_str)
        if id_match and int(id_match.group(1)) == style_id:
            style = {"id": style_id}

            name_match = re.search(r'name:\s*"([^"]*)"', style_str)
            if name_match:
                style["name"] = name_match.group(1)

            cat_match = re.search(r'category:\s*"([^"]*)"', style_str)
            if cat_match:
                style["category"] = cat_match.group(1)

            prompt_match = re.search(
                r'prompt:\s*"((?:[^"\\]|\\.)*)"', style_str, re.DOTALL
            )
            if prompt_match:
                prompt = prompt_match.group(1)
                prompt = prompt.replace("\\n", "\n").replace('\\"', '"')
                style["prompt"] = prompt

            use_match = re.search(r'exampleUse:\s*"([^"]*)"', style_str)
            if use_match:
                style["exampleUse"] = use_match.group(1)

            return style

    raise ValueError(f"Style #{style_id} not found in library")


def list_styles() -> list:
    """List all available styles with their IDs and names."""
    content = _find_style_library().read_text()

    styles = []
    pattern = re.compile(r'id:\s*(\d+),\s*name:\s*"([^"]*)"')
    for match in pattern.finditer(content):
        styles.append({"id": int(match.group(1)), "name": match.group(2)})
    return styles


# ---------------------------------------------------------------------------
# Model listing
# ---------------------------------------------------------------------------

IMAGE_KEYWORDS = {"image", "imagen", "gemini-3"}


def list_models() -> list[dict]:
    """List available image-capable models.

    Returns:
        List of dicts with 'id' and 'display_name' keys.
    """
    client = _get_client()
    results = []
    for m in client.models.list():
        name = m.name.removeprefix("models/")
        if any(kw in name.lower() for kw in IMAGE_KEYWORDS):
            results.append({
                "id": name,
                "display_name": getattr(m, "display_name", ""),
            })
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _cli():
    """Minimal CLI for direct invocation with uv run."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  uv run nano_banana.py generate <prompt> [--ar 1:1] [--res 1K] [--model MODEL] [--output PATH]")
        print("  uv run nano_banana.py extract <image_path>")
        print("  uv run nano_banana.py styles --list")
        print("  uv run nano_banana.py styles <id>")
        print("  uv run nano_banana.py models")
        print("  uv run nano_banana.py session")
        print("  uv run nano_banana.py new")
        print("  uv run nano_banana.py revert [turns]")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "generate":
        if len(sys.argv) < 3:
            print("Error: provide a prompt")
            sys.exit(1)
        prompt = sys.argv[2]
        ar = DEFAULT_ASPECT_RATIO
        res = DEFAULT_RESOLUTION
        mdl = DEFAULT_MODEL
        out = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] in ("--ar", "--aspect-ratio") and i + 1 < len(sys.argv):
                ar = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] in ("--res", "--resolution") and i + 1 < len(sys.argv):
                res = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
                mdl = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] in ("--output", "-o") and i + 1 < len(sys.argv):
                out = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        result = generate(prompt, aspect_ratio=ar, resolution=res, model=mdl, output=out)
        print(f"\nResult: {result}")

    elif cmd == "extract":
        if len(sys.argv) < 3:
            print("Error: provide an image path")
            sys.exit(1)
        extract_style(sys.argv[2])

    elif cmd == "styles":
        if len(sys.argv) < 3 or sys.argv[2] == "--list":
            styles = list_styles()
            print(f"Available styles ({len(styles)} total):\n")
            for s in styles:
                print(f"  #{s['id']:2d}: {s['name']}")
        else:
            style = get_style(int(sys.argv[2]))
            print(f"Style #{style['id']}: {style['name']}")
            print(f"Category: {style.get('category', 'N/A')}")
            print(f"Example use: {style.get('exampleUse', 'N/A')}")
            print(f"\nPrompt:\n{style['prompt']}")

    elif cmd == "models":
        models = list_models()
        default = DEFAULT_MODEL
        print(f"Image-capable models ({len(models)} found):\n")
        for m in models:
            marker = " (default)" if m["id"] == default else ""
            print(f"  {m['id']:50s} {m['display_name']}{marker}")

    elif cmd == "session":
        session_info()

    elif cmd == "new":
        new_session()

    elif cmd == "revert":
        turns = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        revert(turns)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
