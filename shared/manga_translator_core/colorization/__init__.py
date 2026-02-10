"""Colorization module — routes inference to remote API server."""

from PIL import Image

from ..config import Colorizer
from ..api_client import colorize as api_colorize


async def prepare(key: Colorizer):
    pass  # models live on the API server


async def dispatch(key: Colorizer, device: str = "cpu", **kwargs) -> Image.Image:
    image = kwargs.get("image")
    colorization_size = kwargs.get("colorization_size", 576)
    denoise_sigma = kwargs.get("denoise_sigma", 30)
    return await api_colorize(image, colorization_size, denoise_sigma)


async def unload(key: Colorizer):
    pass  # models live on the API server
