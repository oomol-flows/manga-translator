import os
import sys
from oocana import Context
from argparse import Namespace

async def main(params: dict, context: Context):
  os.environ["DEEPSEEK_API_KEY"] = context.oomol_llm_env.get("api_key")
  os.environ["DEEPSEEK_API_BASE"]= context.oomol_llm_env.get("base_url") + "/v1"
  from run import run

  inputDir = params['sourceDir']
  outputDir = params['outputDir']

  args = Namespace(
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
    config_file=os.path.join(sys.path[0], 'config.json'),
    output_lang=params["outputLanguage"]
  ) # type: ignore

  await run(args)          

  return { "outputDir": params["outputDir"] }