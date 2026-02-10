"""Detection module — routes inference to remote API server.

NoneDetector stays local (no model needed). All other detectors
are handled by the API's CRAFT-based detection endpoint.
"""

import numpy as np

from .none import NoneDetector
from ..config import Detector
from ..api_client import detect as api_detect


async def prepare(detector_key: Detector):
    pass  # models live on the API server


async def dispatch(
    detector_key: Detector,
    image: np.ndarray,
    detect_size: int,
    text_threshold: float,
    box_threshold: float,
    unclip_ratio: float,
    invert: bool,
    gamma_correct: bool,
    rotate: bool,
    auto_rotate: bool = False,
    device: str = "cpu",
    verbose: bool = False,
):
    if detector_key == Detector.none:
        detector = NoneDetector()
        return await detector.detect(
            image, detect_size, text_threshold, box_threshold,
            unclip_ratio, invert, gamma_correct, rotate, auto_rotate, verbose,
        )

    # Call remote API and let server-side detector apply preprocessing,
    # so behavior stays aligned with detector implementation.
    return await api_detect(
        image,
        detect_size,
        text_threshold,
        box_threshold,
        unclip_ratio,
        det_rotate=rotate,
        det_auto_rotate=auto_rotate,
        det_invert=invert,
        det_gamma_correct=gamma_correct,
    )


async def unload(detector_key: Detector):
    pass  # models live on the API server
