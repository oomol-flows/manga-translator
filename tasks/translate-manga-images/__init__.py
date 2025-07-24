import os

from typing import cast
from PIL.Image import open as open_image, Image
from oocana import Context
from shared.translator import Translator
from shared.image import parse_format, save_image
from shared.manga_translator import create_config, create_manga_translator

#region generated meta
import typing
from oocana import LLMModelOptions
class Inputs(typing.TypedDict):
  input_files: list[str]
  output_folder: str | None
  source_language: typing.Literal["auto", "CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  target_language: typing.Literal["CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  device: typing.Literal["cuda", "cpu"]
  llm: LLMModelOptions
class Outputs(typing.TypedDict):
  output_files: list[str]
  output_folder: str
#endregion


async def main(params: Inputs, context: Context) -> Outputs:
  input_files = params["input_files"]
  output_folder = params["output_folder"]
  source_language = params["source_language"]
  target_language = params["target_language"]

  if len(input_files) == 0:
    raise ValueError("No input_files provided")

  completed_files: int = 0
  translator = Translator(
    llm_model=params["llm"],
    context=context,
    source_language=source_language,
    target_language=target_language,
    report_progress=lambda p: context.report_progress(
      progress=100.0 * ((completed_files + p) / len(input_files))
    ),
  )
  config = create_config(target_language, translator.translate)
  manga = create_manga_translator(
    use_gpu=(params["device"]=="cuda"),
    model_dir=context.pkg_data_dir,
  )
  if output_folder is None:
    output_folder = os.path.join(
      context.session_dir,
      context.job_id,
    )
  output_files: list[str] = []
  os.makedirs(output_folder, exist_ok=True)

  for i, input_file_path in enumerate(input_files):
    completed_files = i
    origin_ext_name = os.path.splitext(input_file_path)[1]

    with open(input_file_path, mode="rb") as input:
      image = open_image(input)
      image_format: str | None = image.format
      if image_format is None:
        print(f"Image {input_file_path} format is not supported")
        continue

      image_format, ext_name = parse_format(image_format, origin_ext_name)
      ctx = await manga.translate(image, config)
      output_image = cast(Image | None, ctx.result)
      if output_image is None:
        continue

      output_file_name = f"{i + 1}{ext_name}"
      output_file = os.path.join(output_folder, output_file_name)
      output_files.append(output_file)

      with open(output_file, "wb") as output:
        save_image(output_image, output, image_format)

  context.report_progress(100.0)

  return {
    "output_files": output_files,
    "output_folder": output_folder,
  }