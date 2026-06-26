"""
Image generation tool.

Strategy (in order):
  1. Gemini Imagen (imagen-3.0-generate-002) via google-genai SDK
  2. OpenAI gpt-image-1 (DALL-E 3 compatible)
  3. Local placeholder image (Pillow-generated grey card)

Generated images are saved to output/images/<id>.jpg.
The returned path is the URL path: /images/<id>.jpg
"""

import os
import base64
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ── Output paths ──────────────────────────────────────────────────────────────
OUTPUT_DIR      = Path(__file__).resolve().parent.parent / "output" / "images"
PLACEHOLDER_SRC = Path(__file__).resolve().parent.parent / "output" / "placeholder.jpg"
PLACEHOLDER_URL = "/images/placeholder.jpg"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Gemini Imagen
# ─────────────────────────────────────────────────────────────────────────────

def _generate_with_gemini(prompt: str, filename: str) -> str | None:
    """Try to generate an image using Gemini Imagen via the google-genai SDK."""
    try:
        from google import genai as google_genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[ImageTool] GEMINI_API_KEY not set - skipping Gemini Imagen")
            return None

        client = google_genai.Client(api_key=api_key)

        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=google_genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="BLOCK_SOME",
                person_generation="DONT_ALLOW",
            ),
        )

        if not response.generated_images:
            print("[ImageTool] Gemini returned no images")
            return None

        image_bytes = response.generated_images[0].image.image_bytes
        save_path = OUTPUT_DIR / filename
        with open(save_path, "wb") as f:
            f.write(image_bytes)

        print(f"[ImageTool] Gemini image saved: {save_path}")
        return f"/images/{filename}"

    except Exception as e:
        print(f"[ImageTool] Gemini Imagen failed: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 2. OpenAI gpt-image-1
# ─────────────────────────────────────────────────────────────────────────────

def _generate_with_openai(prompt: str, filename: str) -> str | None:
    """Try to generate an image using OpenAI gpt-image-1."""
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("[ImageTool] OPENAI_API_KEY not configured - skipping OpenAI")
            return None

        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1792x1024",
            quality="standard",
        )

        image_url = response.data[0].url

        if image_url:
            img_resp = requests.get(image_url, timeout=30)
            img_resp.raise_for_status()
            image_bytes = img_resp.content
        else:
            # b64_json fallback
            b64 = response.data[0].b64_json
            image_bytes = base64.b64decode(b64)

        save_path = OUTPUT_DIR / filename
        with open(save_path, "wb") as f:
            f.write(image_bytes)

        print(f"[ImageTool] OpenAI image saved: {save_path}")
        return f"/images/{filename}"

    except Exception as e:
        print(f"[ImageTool] OpenAI image generation failed: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 3. Placeholder fallback
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_placeholder() -> str:
    """Create a minimal placeholder image if it doesn't already exist."""
    if PLACEHOLDER_SRC.exists():
        return PLACEHOLDER_URL

    try:
        from PIL import Image, ImageDraw

        img  = Image.new("RGB", (1792, 1024), color=(18, 18, 28))
        draw = ImageDraw.Draw(img)

        # Subtle diagonal gradient lines
        for i in range(0, 1792, 8):
            shade = int(28 + (i / 1792) * 30)
            draw.line([(i, 0), (i, 1024)], fill=(shade, shade, shade + 12))

        # Centered text
        draw.rectangle([780, 490, 1010, 534], fill=(40, 40, 60))

        img.save(PLACEHOLDER_SRC, "JPEG", quality=85)
        print(f"[ImageTool] Created placeholder: {PLACEHOLDER_SRC}")

    except Exception as e:
        print(f"[ImageTool] Pillow placeholder failed: {e}")
        # Write a minimal valid 1×1 JPEG
        minimal = bytes([
            0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46,0x49,0x46,0x00,0x01,
            0x01,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0xFF,0xDB,0x00,0x43,
            0x00,0x08,0x06,0x06,0x07,0x06,0x05,0x08,0x07,0x07,0x07,0x09,
            0x09,0x08,0x0A,0x0C,0x14,0x0D,0x0C,0x0B,0x0B,0x0C,0x19,0x12,
            0x13,0x0F,0x14,0x1D,0x1A,0x1F,0x1E,0x1D,0x1A,0x1C,0x1C,0x20,
            0x24,0x2E,0x27,0x20,0x22,0x2C,0x23,0x1C,0x1C,0x28,0x37,0x29,
            0x2C,0x30,0x31,0x34,0x34,0x34,0x1F,0x27,0x39,0x3D,0x38,0x32,
            0x3C,0x2E,0x33,0x34,0x32,0xFF,0xC0,0x00,0x0B,0x08,0x00,0x01,
            0x00,0x01,0x01,0x01,0x11,0x00,0xFF,0xC4,0x00,0x1F,0x00,0x00,
            0x01,0x05,0x01,0x01,0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,
            0x09,0x0A,0x0B,0xFF,0xDA,0x00,0x08,0x01,0x01,0x00,0x00,0x3F,
            0x00,0xFB,0xD6,0xFF,0xD9,
        ])
        with open(PLACEHOLDER_SRC, "wb") as f:
            f.write(minimal)

    return PLACEHOLDER_URL


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def generate_ai_image(article_title: str, article_id: int) -> tuple[str, str]:
    """
    Generate an AI image for a news article.

    Returns:
        (image_path, image_source)
        image_path   — URL path /images/<id>.jpg or /images/placeholder.jpg
        image_source — "generated" | "placeholder"
    """
    filename = f"{article_id}.jpg"

    editorial_prompt = (
        f"Create a realistic editorial-style technology news illustration "
        f"representing this news article: '{article_title}'. "
        f"Photorealistic, high quality, landscape orientation, "
        f"professional magazine style, modern technology aesthetic, "
        f"clean composition, dramatic lighting, no text, no logos, "
        f"no watermark, no captions."
    )

    # 1. Gemini Imagen
    print("[ImageTool] Attempting Gemini Imagen...")
    path = _generate_with_gemini(editorial_prompt, filename)
    if path:
        return path, "generated"

    # 2. OpenAI gpt-image-1
    print("[ImageTool] Attempting OpenAI gpt-image-1...")
    path = _generate_with_openai(editorial_prompt, filename)
    if path:
        return path, "generated"

    # 3. Placeholder
    print("[ImageTool] All image generators unavailable - using placeholder")
    return _ensure_placeholder(), "placeholder"


def is_valid_image_url(url: str) -> bool:
    """
    Quick HTTP HEAD to verify an image URL is reachable and returns an image.
    Returns True on network errors (don't block on slow CDNs).
    """
    if not url or not url.startswith("http"):
        return False
    try:
        resp = requests.head(url, timeout=6, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "")
        return resp.status_code == 200 and "image" in content_type
    except Exception:
        return True  # Assume valid if we can't check
