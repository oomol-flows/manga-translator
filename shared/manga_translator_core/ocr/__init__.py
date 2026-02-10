"""OCR module — routes inference to remote API server."""

import numpy as np
from typing import List, Optional

from ..config import Ocr, OcrConfig
from ..utils import Quadrilateral
from ..api_client import ocr as api_ocr


async def prepare(ocr_key: Ocr, device: str = "cpu"):
    pass  # models live on the API server


async def dispatch(
    ocr_key: Ocr,
    image: np.ndarray,
    regions: List[Quadrilateral],
    config: Optional[OcrConfig] = None,
    device: str = "cpu",
    verbose: bool = False,
) -> List[Quadrilateral]:
    # Serialize Quadrilateral → JSON for the API
    textlines_json = [
        {"pts": r.pts.tolist(), "prob": float(r.prob)}
        for r in regions
    ]

    ocr_min_prob = None
    if config is not None:
        ocr_min_prob = getattr(config, "ocr_min_prob", None)

    return await api_ocr(image, textlines_json, ocr_min_prob=ocr_min_prob)


async def unload(ocr_key: Ocr):
    pass  # models live on the API server
