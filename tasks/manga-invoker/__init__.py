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
import json

from typing import cast, Any
from natsort import natsorted
from PIL import Image
from oocana import Context
from shared import Config

# wait shared update os.sys.path
from manga_translator import MangaTranslator, Config as MangaConfig

def to_dict(**kwargs) -> dict[str, Any]:
  return kwargs

async def main(params: Inputs, context: Context) -> Outputs:
  inputDir = params["input_dir"]
  outputDir = params["output_dir"]
  lang = params["lang"]
  config_path = os.path.join(__file__, "..", "..", "..", "config.json")
  config_path = os.path.abspath(config_path)
  args = to_dict(
    verbose=True,
    attempts=0,
    ignore_errors=False,
    model_dir=None,
    use_gpu=False,
    use_gpu_limited=False,
    font_path="",
    pre_dict=None,
    post_dict=None,
    kernel_size=3,
    mode="local",
    input=[inputDir],
    dest=outputDir,
    format=None,
    overwrite=False,
    skip_no_text=False,
    use_mtpe=False,
    save_text=False,
    load_text=False,
    save_text_file="",
    prep_manual=False,
    save_quality=100,
    config_file=config_path,
    output_lang=lang,
  )
  translator = MangaTranslator(args)

  with open(config_path, "r", encoding="utf-8") as file:
    config_data = json.load(file)
    config_data["translator"] = {
      **config_data["translator"],
      "base_url": context.oomol_llm_env["base_url_v1"],
      "key": context.oomol_llm_env["api_key"],
      "model": context.oomol_llm_env["models"][0],
    }
    config: MangaConfig = cast(Any, Config(**config_data))

  for file in natsorted(os.listdir(inputDir)):
    with Image.open(os.path.join(inputDir, file)) as image:
      image = Image.open(os.path.join(inputDir, file))
      ctx = await translator.translate(image, config)
      result: Image.Image | None = ctx.result
      if result:
        result.save(os.path.join(outputDir, file))

  return {
    "output_files": natsorted(os.listdir(outputDir)),
  }
