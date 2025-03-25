from typing import Any
from oocana import Context


class Translator:
  def __init__(self, llm_model: dict[str, Any], context: Context) -> None:
    pass

  def translate(
      self,
      code_map: dict[str, str],
      source: str,
      target: str,
      queries: list[str],
    ) -> list[str]:
    return [f"{source} -> {target}" for _ in queries]