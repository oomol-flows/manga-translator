from typing import cast, final, Any
from typing_extensions import override

from manga_translator import Translator
from manga_translator.config import TranslatorConfig
from manga_translator.translators import TRANSLATORS
from manga_translator.translators.common import CommonTranslator


def replace_offline_translator():
  cast(Any, TRANSLATORS)[Translator.deepseek] = WrappedTranslator
  print("replace", TRANSLATORS[Translator.deepseek])

@final
class WrappedTranslator(CommonTranslator):
  _MAX_REQUESTS_PER_MINUTE = 9999
  _INVALID_REPEAT_COUNT = 0 # this's useless
  _LANGUAGE_CODE_MAP = {
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

  def __init__(self, **kargs):
    super().__init__()
    print("init", kargs)

  @override
  def parse_args(self, args: TranslatorConfig):
    print(args)

  @override
  async def _translate(self, from_lang: str, to_lang: str, queries: list[str]) -> list[str]:
    return [f"{from_lang} -> {to_lang}" for _ in queries]