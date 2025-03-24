#region generated meta
import typing
class Inputs(typing.TypedDict):
  input_dir: str
  output_dir: str
  lang: typing.Literal["CHS", "CHT", "ENG", "JPN", "KOR", "FRA", "DEU", "RUS"]
class Outputs(typing.TypedDict):
  output_files: list[str]
#endregion

import os

from typing import cast
from natsort import natsorted
from PIL import Image
from oocana import Context
from shared import create_config, create_manga_translator

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
