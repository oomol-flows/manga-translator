import io

from typing import cast, Any, Literal, TypedDict
from oocana import Context
from PIL.Image import open, Image
from shared.translator import Translator
from shared.manga_translator import (
  create_config,
  create_manga_translator,
  SourceLanguage,
  TargetLanguage,
)


ImageExt = Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]

class Inputs(TypedDict):
  input: bytes
  device: Literal["cuda", "cpu"]
  models: str | None
  llm: dict[str, Any]
  source_language: SourceLanguage
  target_language: TargetLanguage

class Outputs(TypedDict):
  output: bytes
  ext: ImageExt

async def main(params: Inputs, context: Context) -> Outputs:
  models = params["models"]
  if models is None:
    models = "/tmp/models"

  with io.BytesIO(params["input"]) as input_file:
    image = open(input_file)
    image_format: str | None = image.format

    if image_format is None:
      raise ValueError("Image format is not supported")

    translator = Translator(
      llm_model=params["llm"],
      context=context,
      source_language=params["source_language"],
      target_language=params["target_language"],
    )
    config = create_config(translator.translate)
    manga = create_manga_translator(
      use_gpu=(params["device"]=="cuda"),
      model_dir=models,
    )
    ctx = await manga.translate(image, config)
    output_image = cast(Image | None, ctx.result)

  if output_image is None:
    raise ValueError("Translation failed")

  with io.BytesIO() as output:
    output_image.save(output, format=image_format)
    output_bytes = output.getvalue()

  return {
    "output": output_bytes,
    "ext": cast(ImageExt, "." + image_format.lower()),
   }
