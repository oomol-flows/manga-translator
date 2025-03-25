import re

from typing import cast, Any
from pydantic import BaseModel
from manga_translator.config import RenderConfig, UpscaleConfig, DetectorConfig, ColorizerConfig, InpainterConfig, OcrConfig
from manga_translator import MangaTranslator, Config as MangaConfig

from .types import TargetLanguage
from .translator import Translator, WrappedTranslatorConfig

# clone from manga_translator.config.Config
# replace translator type
class Config(BaseModel):
    filter_text: str | None = None
    """Filter regions by their text with a regex. Example usage: '.*badtext.*'"""
    render: RenderConfig = RenderConfig()
    """render configs"""
    upscale: UpscaleConfig = UpscaleConfig()
    """upscaler configs"""
    translator: WrappedTranslatorConfig = WrappedTranslatorConfig()
    """tanslator configs"""
    detector: DetectorConfig = DetectorConfig()
    """detector configs"""
    colorizer: ColorizerConfig = ColorizerConfig()
    """colorizer configs"""
    inpainter: InpainterConfig = InpainterConfig()
    """inpainter configs"""
    ocr: OcrConfig = OcrConfig()
    """Ocr configs"""
    # ?
    kernel_size: int = 3
    """Set the convolution kernel size of the text erasure area to completely clean up text residues"""
    mask_dilation_offset: int = 0
    """By how much to extend the text mask to remove left-over text pixels of the original image."""
    _filter_text: re.Pattern[str] | None = None

    @property
    def re_filter_text(self):
      if self._filter_text is None and self.filter_text is not None:
        self._filter_text = re.compile(self.filter_text)
      return self._filter_text

def create_manga_translator(use_gpu: bool, model_dir: str | None) -> MangaTranslator:
  return MangaTranslator({
    "use_gpu": use_gpu,
    "model_dir": model_dir,
    "verbose": False,
    "ignore_errors": False,
    "use_gpu_limited": False,
    "font_path": None,
    "pre_dict": None,
    "post_dict": None,
    "kernel_size": 3,
    "use_mtpe": False,
    "save_text": False,
    "load_text": False,
    "prep_manual": False,
  })

def create_config(target_language: TargetLanguage, translator: Translator) -> MangaConfig:
  base_json: dict[str, Any] = {
    "filter_text": None,
    "render": {
      "renderer": "default",
      "alignment": "auto",
      "disable_font_border": False,
      "font_size_offset": 0,
      "font_size_minimum": -1,
      "direction": "auto",
      "uppercase": False,
      "lowercase": False,
      "gimp_font": "Sans-serif",
      "no_hyphenation": False,
      "font_color": None,
      "line_spacing": None,
      "font_size": None,
    },
    "upscale": {
      "upscaler": "esrgan",
      "revert_upscaling": False,
      "upscale_ratio": None,
    },
    "translator": {
      "translator": "deepseek",
      "target_lang": target_language,
      "no_text_lang_skip": False,
      "skip_lang": None,
      "gpt_config": None,
      "translator_chain": None,
      "selective_translation": None,
      "func": None,
    },
    "detector": {
      "detector": "default",
      "detection_size": 1536,
      "text_threshold": 0.5,
      "det_rotate": False,
      "det_auto_rotate": False,
      "det_invert": False,
      "det_gamma_correct": False,
      "box_threshold": 0.7,
      "unclip_ratio": 2.3,
    },
    "colorizer": {
      "colorization_size": 576,
      "denoise_sigma": 30,
      "colorizer": "none",
    },
    "inpainter": {
      "inpainter": "none",
      "inpainting_size": 2048,
      "inpainting_precision": "fp32",
    },
    "ocr": {
      "use_mocr_merge": False,
      "ocr": "48px",
      "min_text_length": 0,
      "ignore_bubble": 0,
    },
    "kernel_size": 1,
    "mask_dilation_offset": 0,
  }
  config = Config(**base_json)
  config.translator.func = translator

  return cast(Any, config)