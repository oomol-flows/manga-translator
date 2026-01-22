import os
from typing import cast, Literal
from oocana import Context, LLMModelOptions
from PIL.Image import open as open_image, Image
from shared.translator import Translator
from shared.image import parse_format
from shared.manga_translator import create_config, create_manga_translator

#region generated meta
import typing
class Inputs(typing.TypedDict):
  input: str
  target_language: typing.Literal["CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  source_language: typing.Literal["auto", "CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  device: typing.Literal["cuda", "cpu"]
  llm: LLMModelOptions
class Outputs(typing.TypedDict):
  output: typing.NotRequired[str]
  ext: typing.NotRequired[typing.Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]]
#endregion


async def main(params: Inputs, context: Context) -> Outputs:
  source_language = params["source_language"]
  target_language = params["target_language"]

  image = open_image(params["input"])
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

  # Save translated image to file
  output_filename = f"translated{image_ext}"
  output_path = os.path.join(context.session_dir, output_filename)

  # Convert RGB if necessary for certain formats
  if image_format not in ["PNG", "WEBP"] and output_image.mode != "RGB":
    output_image = output_image.convert("RGB")

  output_image.save(output_path, format=image_format)

  context.report_progress(100.0)

  return {
    "output": output_path,
    "ext": cast(Literal[".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"], image_ext),
   }
