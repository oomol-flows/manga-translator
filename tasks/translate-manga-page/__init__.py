from io import BytesIO
from typing import Literal, TypedDict
from oocana import Context
from PIL.Image import open
from shared.manga_translator import (
  create_config,
  create_manga_translator,
  SourceLanguage,
  TargetLanguage,
)


class Inputs(TypedDict):
  input: bytes
  device: Literal["cuda", "cpu"]
  models: str | None
  source_language: SourceLanguage
  target_language: TargetLanguage

class Outputs(TypedDict):
  output: bytes
  ext: Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]

def main(params: Inputs, context: Context) -> Outputs:
  models = params["models"]
  if models is None:
    models = "/tmp/models"

  with BytesIO(params["input"]) as input_file:
    image = open(input_file)

  if image.format is None:
    raise ValueError("Image format is not supported")

  manga = create_manga_translator(
    use_gpu=(params["device"]=="cuda"),
    model_dir=models,
  )

  return { "output": "output_value" }
