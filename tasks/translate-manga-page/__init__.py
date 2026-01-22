import io

from typing import cast, Literal
from oocana import Context
from PIL.Image import open, Image
from shared.translator import Translator
from shared.image import parse_format, save_image
from shared.manga_translator import create_config, create_manga_translator

#region generated meta
import typing
from oocana import LLMModelOptions
class Inputs(typing.TypedDict):
  input: bytes
  target_language: typing.Literal["CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  source_language: typing.Literal["auto", "CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  device: typing.Literal["cuda", "cpu"]
  llm: LLMModelOptions
class Outputs(typing.TypedDict):
  output: typing.NotRequired[bytes]
  ext: typing.NotRequired[typing.Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]]
#endregion


async def main(params: Inputs, context: Context) -> Outputs:
  source_language = params["source_language"]
  target_language = params["target_language"]

  with io.BytesIO(params["input"]) as input_file:
    image = open(input_file)
    image_format: str | None = image.format

    if image_format is None:
      raise ValueError("Image format is not supported")

    image_format, image_ext = parse_format(image_format)
    translator = Translator(
      llm_model=params["llm"],
      context=context,
      source_language=source_language,
      target_language=target_language,
      report_progress=lambda p: context.report_progress(p * 100.0),
    )
    config = create_config(target_language, translator.translate)
    manga = create_manga_translator(
      use_gpu=(params["device"]=="cuda"),
      model_dir=context.pkg_data_dir,
    )
    ctx = await manga.translate(image, config)
    output_image = cast(Image | None, ctx.result)

  if output_image is None:
    raise ValueError("Translation failed")

  with io.BytesIO() as output:
    save_image(output_image, output, image_format)
    output_bytes = output.getvalue()

  context.report_progress(100.0)

  return {
    "output": output_bytes,
    "ext": cast(Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"], image_ext),
   }
