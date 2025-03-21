import re

from pydantic import BaseModel
from manga_translator.config import RenderConfig, UpscaleConfig, DetectorConfig, TranslatorConfig, ColorizerConfig, InpainterConfig, OcrConfig

class WrappedTranslatorConfig(TranslatorConfig):
  base_url: str = ""
  key: str = ""
  model: str = ""

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