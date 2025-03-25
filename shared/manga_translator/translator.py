from typing import cast, final, Any, Callable
from typing_extensions import override

from manga_translator import Translator as MangaTranslator
from manga_translator.config import TranslatorConfig
from manga_translator.translators import TRANSLATORS
from manga_translator.translators.common import CommonTranslator



Translator = Callable[[dict[str, str], list[str]], list[str]]

class WrappedTranslatorConfig(TranslatorConfig):
  func: Translator | None = None

@final
class WrappedTranslator(CommonTranslator):
  _MAX_REQUESTS_PER_MINUTE = 9999
  _INVALID_REPEAT_COUNT = 0 # this's useless
  _LANGUAGE_CODE_MAP: dict[str, str] = {
    "CHS": "Simplified Chinese",
    "CHT": "Traditional Chinese",
    "CSY": "Czech",
    "NLD": "Dutch",
    "ENG": "English",
    "FRA": "French",
    "DEU": "German",
    "HUN": "Hungarian",
    "ITA": "Italian",
    "JPN": "Japanese",
    "KOR": "Korean",
    "PLK": "Polish",
    "PTB": "Portuguese",
    "ROM": "Romanian",
    "RUS": "Russian",
    "ESP": "Spanish",
    "TRK": "Turkish",
    "UKR": "Ukrainian",
    "VIN": "Vietnamese",
    "CNR": "Montenegrin",
    "SRP": "Serbian",
    "HRV": "Croatian",
    "ARA": "Arabic",
    "THA": "Thai",
    "IND": "Indonesian"
  }

  def __init__(self, **_):
    super().__init__()
    self._transalte: Translator | None = None

  @override
  def parse_args(self, args: TranslatorConfig):
    self._transalte = cast(WrappedTranslatorConfig, args).func

  @override
  async def _translate(self, from_lang: str, to_lang: str, queries: list[str]) -> list[str]:
    if self._transalte is None:
      return [q for q in queries]
    else:
      return self._transalte(self._LANGUAGE_CODE_MAP, queries)

cast(Any, TRANSLATORS)[MangaTranslator.deepseek] = WrappedTranslator