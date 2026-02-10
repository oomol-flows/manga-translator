"""Inpainting module — routes inference to remote API server.

NoneInpainter and OriginalInpainter stay local (no model needed).
All other inpainters are handled by the API's SD inpainting endpoint.
"""

import numpy as np
from typing import Optional

from .none import NoneInpainter
from .original import OriginalInpainter
from ..config import Inpainter, InpainterConfig
from ..api_client import inpaint as api_inpaint


async def prepare(inpainter_key: Inpainter, device: str = "cpu"):
    pass  # models live on the API server


async def dispatch(
    inpainter_key: Inpainter,
    image: np.ndarray,
    mask: np.ndarray,
    config: Optional[InpainterConfig] = None,
    inpainting_size: int = 1024,
    device: str = "cpu",
    verbose: bool = False,
) -> np.ndarray:
    config = config or InpainterConfig()

    if inpainter_key == Inpainter.none:
        inpainter = NoneInpainter()
        return await inpainter.inpaint(image, mask, config, inpainting_size, verbose)

    if inpainter_key == Inpainter.original:
        inpainter = OriginalInpainter()
        return await inpainter.inpaint(image, mask, config, inpainting_size, verbose)

    # All model-based inpainters → API
    return await api_inpaint(image, mask, inpainting_size)


async def unload(inpainter_key: Inpainter):
    pass  # models live on the API server
