#region generated meta
import typing
class Inputs(typing.TypedDict):
  input_files: list[str]
  output_folder: typing.Optional[str]
  device: typing.Literal["cuda", "cpu"]
  models: typing.Optional[str]
  source_language: typing.Literal["auto", "CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
  target_language: typing.Literal["CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN", "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR", "SRP", "HRV", "ARA", "THA", "IND"]
class Outputs(typing.TypedDict):
  output_files: list[str]
  output_folder: str
#endregion

import os

from typing import cast
from natsort import natsorted
from PIL import Image
from oocana import Context
from shared.manga_translator import create_config, create_manga_translator

async def main(params: Inputs, context: Context) -> Outputs:
  inputDir = params["input_dir"]
  outputDir = params["output_dir"]
  lang = params["lang"]
  config = create_config(
    translator=lambda _, s_lan, t_lan, querys: [
      f"{s_lan} -> {t_lan}" for _ in querys
    ],
  )
  manga_translator = create_manga_translator(
    use_gpu=False,
    model_dir=None,
  )
  # config_data["translator"] = {
  #   **config_data["translator"],
  #   "base_url": context.oomol_llm_env["base_url_v1"],
  #   "key": context.oomol_llm_env["api_key"],
  #   "model": context.oomol_llm_env["models"][0],
  # }

  for file in natsorted(os.listdir(inputDir)):
    with Image.open(os.path.join(inputDir, file)) as image:
      image = Image.open(os.path.join(inputDir, file))
      ctx = await manga_translator.translate(image, config)
      result = cast(Image.Image | None, ctx.result)
      if result:
        result.save(os.path.join(outputDir, file))

  return {
    "output_files": natsorted(os.listdir(outputDir)),
  }
