"""Detection module — routes inference to remote API server.

NoneDetector stays local (no model needed). All other detectors
are handled by the API's CRAFT-based detection endpoint.
"""

import cv2
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

    # Apply image preprocessing locally (these are pure numpy ops)
    img = image
    img_h, img_w = img.shape[:2]
    original = img.copy()

    if rotate:
        img = np.rot90(img, k=-1)
    if min(img_w, img_h) < 400:
        new_side = max(img_w, img_h, 400)
        padded = np.zeros((new_side, new_side, 3), dtype=np.uint8)
        padded[:img_h, :img_w] = img
        img = padded
    if invert:
        img = cv2.bitwise_not(img)
    if gamma_correct:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean = np.mean(gray)
        if mean > 0:
            gamma = np.log(0.5 * 255) / np.log(mean)
            img = np.power(img, gamma).clip(0, 255).astype(np.uint8)

    # Call remote API
    return await api_detect(img, detect_size, text_threshold, box_threshold, unclip_ratio)


async def unload(detector_key: Detector):
    pass  # models live on the API server
