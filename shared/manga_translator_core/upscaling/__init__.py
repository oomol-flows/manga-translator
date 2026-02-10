"""Upscaling module — routes inference to remote API server."""

from typing import List
from PIL import Image

from ..config import Upscaler
from ..api_client import upscale as api_upscale


async def prepare(upscaler_key: Upscaler):
    pass  # models live on the API server


async def dispatch(
    upscaler_key: Upscaler,
    image_batch: List[Image.Image],
    upscale_ratio: int,
    device: str = "cpu",
) -> List[Image.Image]:
    if upscale_ratio == 1:
        return image_batch

    results = []
    for img in image_batch:
        result = await api_upscale(img, upscale_ratio)
        results.append(result)
    return results


async def unload(upscaler_key: Upscaler):
    pass  # models live on the API server
