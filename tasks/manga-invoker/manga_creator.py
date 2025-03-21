import os
import sys

sys.path.append(
  os.path.abspath(os.path.join(__file__, "..", "..", "..", "manga")),
)

from typing import cast
from manga.manga_translator.mode.local import MangaTranslatorLocal

def create(params: dict | None) -> MangaTranslatorLocal:
  return MangaTranslatorLocal(cast(dict, params))