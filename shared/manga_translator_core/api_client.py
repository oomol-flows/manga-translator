"""HTTP client for manga-translator API server.

Routes all model inference to a remote FastAPI server instead of
loading models locally. Configured via MANGA_API_URL env var.
"""

import base64
import io
import json
import os
from typing import List, Tuple

import numpy as np
from PIL import Image

API_URL = os.environ.get("MANGA_API_URL", "http://localhost:8000")
_client = None


async def get_client():
    global _client
    if _client is None:
        import httpx
        _client = httpx.AsyncClient(base_url=API_URL, timeout=300.0)
    return _client


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def ndarray_to_png_bytes(arr: np.ndarray) -> bytes:
    img = Image.fromarray(arr.astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def pil_to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def png_bytes_to_ndarray(data: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(data))
    return np.array(img.convert("RGB"))


def png_bytes_to_pil(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))


def base64_png_to_ndarray(s: str) -> np.ndarray:
    data = base64.b64decode(s)
    img = Image.open(io.BytesIO(data))
    return np.array(img.convert("L"))


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

async def detect(
    image: np.ndarray,
    detect_size: int = 2048,
    text_threshold: float = 0.5,
    box_threshold: float = 0.7,
    unclip_ratio: float = 2.3,
    det_rotate: bool = False,
    det_auto_rotate: bool = False,
    det_invert: bool = False,
    det_gamma_correct: bool = False,
) -> Tuple[list, np.ndarray, np.ndarray]:
    """Call /api/detect. Returns (List[Quadrilateral], raw_mask, mask)."""
    from .utils import Quadrilateral

    client = await get_client()
    resp = await client.post(
        "/api/detect",
        files={"image": ("image.png", ndarray_to_png_bytes(image), "image/png")},
        data={
            "detect_size": str(detect_size),
            "text_threshold": str(text_threshold),
            "box_threshold": str(box_threshold),
            "unclip_ratio": str(unclip_ratio),
            "det_rotate": str(det_rotate).lower(),
            "det_auto_rotate": str(det_auto_rotate).lower(),
            "det_invert": str(det_invert).lower(),
            "det_gamma_correct": str(det_gamma_correct).lower(),
        },
    )
    resp.raise_for_status()
    result = resp.json()

    textlines = []
    for item in result["textlines"]:
        q = Quadrilateral(
            pts=np.array(item["pts"], dtype=np.float64),
            text="",
            prob=item.get("prob", 1.0),
        )
        textlines.append(q)

    mask = base64_png_to_ndarray(result["mask"])
    return textlines, mask, mask


async def ocr(
    image: np.ndarray,
    textlines_json: List[dict],
    ocr_min_prob: float | None = None,
) -> list:
    """Call /api/ocr. Returns List[Quadrilateral] with text and colors."""
    from .utils import Quadrilateral

    client = await get_client()
    resp = await client.post(
        "/api/ocr",
        files={"image": ("image.png", ndarray_to_png_bytes(image), "image/png")},
        data={
            "textlines": json.dumps(textlines_json),
            **({"ocr_min_prob": str(ocr_min_prob)} if ocr_min_prob is not None else {}),
        },
    )
    resp.raise_for_status()
    result = resp.json()

    quads = []
    for item in result["textlines"]:
        fg = item.get("fg_color", [0, 0, 0])
        bg = item.get("bg_color", [0, 0, 0])
        q = Quadrilateral(
            pts=np.array(item["pts"], dtype=np.float64),
            text=item.get("text", ""),
            prob=item.get("prob", 1.0),
            fg_r=fg[0], fg_g=fg[1], fg_b=fg[2],
            bg_r=bg[0], bg_g=bg[1], bg_b=bg[2],
        )
        quads.append(q)
    return quads


async def inpaint(
    image: np.ndarray,
    mask: np.ndarray,
    inpainting_size: int = 1024,
) -> np.ndarray:
    """Call /api/inpaint. Returns RGB ndarray."""
    client = await get_client()
    resp = await client.post(
        "/api/inpaint",
        files={
            "image": ("image.png", ndarray_to_png_bytes(image), "image/png"),
            "mask": ("mask.png", ndarray_to_png_bytes(mask), "image/png"),
        },
        data={"inpainting_size": str(inpainting_size)},
    )
    resp.raise_for_status()
    return png_bytes_to_ndarray(resp.content)


async def upscale(
    image: Image.Image,
    upscale_ratio: int = 4,
) -> Image.Image:
    """Call /api/upscale. Returns PIL.Image."""
    client = await get_client()
    resp = await client.post(
        "/api/upscale",
        files={"image": ("image.png", pil_to_png_bytes(image), "image/png")},
        data={"upscale_ratio": str(upscale_ratio)},
    )
    resp.raise_for_status()
    return png_bytes_to_pil(resp.content)


async def colorize(
    image: Image.Image,
    colorization_size: int = 576,
    denoise_sigma: int = 30,
) -> Image.Image:
    """Call /api/colorize. Returns PIL.Image."""
    client = await get_client()
    resp = await client.post(
        "/api/colorize",
        files={"image": ("image.png", pil_to_png_bytes(image), "image/png")},
        data={
            "colorization_size": str(colorization_size),
            "denoise_sigma": str(denoise_sigma),
        },
    )
    resp.raise_for_status()
    return png_bytes_to_pil(resp.content)


TRANSLATOR_ENDPOINT_MAP = {
    "nllb": "/api/translate/nllb",
    "nllb_big": "/api/translate/nllb-big",
    "mbart50": "/api/translate/mbart50",
}


async def translate(
    texts: List[str],
    from_lang: str,
    to_lang: str,
    translator_key: str,
) -> List[str]:
    """Call /api/translate/<model>. Returns list of translated strings."""
    endpoint = TRANSLATOR_ENDPOINT_MAP.get(translator_key)
    if endpoint is None:
        raise ValueError(f"Unsupported API translator: {translator_key}")

    client = await get_client()
    resp = await client.post(
        endpoint,
        json={"texts": texts, "from_lang": from_lang, "to_lang": to_lang},
    )
    resp.raise_for_status()
    return resp.json()["translations"]
