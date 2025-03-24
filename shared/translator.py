from oocana import Context


class Translator:
  def __init__(self, context: Context) -> None:
    pass

  def translate(
      self,
      code_map: dict[str, str],
      source: str,
      target: str,
      queries: list[str],
    ) -> list[str]:
    return [f"{source} -> {target}" for _ in queries]