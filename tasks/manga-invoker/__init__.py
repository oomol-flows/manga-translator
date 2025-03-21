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
from oocana import Context
from shared import replace_offline_translator

replace_offline_translator()

from manga.manga_translator.mode.local import MangaTranslatorLocal

def to_dict(**kwargs) -> dict:
  return kwargs

async def main(params: Inputs, context: Context) -> Outputs:
  # os.environ["DEEPSEEK_API_KEY"] = context.oomol_llm_env.get("api_key")
  # oomol_base_url = context.oomol_llm_env.get("base_url")
  # if not oomol_base_url.endswith("/v1"):
  #   oomol_base_url= oomol_base_url + "/v1"
  # os.environ["DEEPSEEK_API_BASE"]= oomol_base_url


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
  translator = MangaTranslatorLocal(cast(dict, args))
  await translator.translate_path(inputDir, outputDir, args)

  return {
    "output_files": natsorted(os.listdir(outputDir)),
  }
