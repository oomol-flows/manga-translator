import re
import io

from typing import final, cast, Any
from collections.abc import Generator
from oocana import Context

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessageChunk


@final
class Translator:
  def __init__(self, llm_model: dict[str, Any], context: Context) -> None:
    env = context.oomol_llm_env
    model: str = llm_model["model"]
    temperature: float = float(llm_model["temperature"])
    self._model = ChatOpenAI(
      api_key=cast(Any, env["api_key"]),
      base_url=env["base_url_v1"],
      model=model,
      temperature=temperature,
    )

  def translate(
      self,
      code_map: dict[str, str],
      source: str,
      target: str,
      queries: list[str],
    ) -> list[str]:

    if source == "auto":
      source = ""

    system = self._gen_admin_prompt(target, source)
    translated_list: list[str] = []

    for translated in self._translate_text_by_text(system, queries):
      translated_list.append(translated)

    return translated_list

  def _translate_text_by_text(self, system: str, texts: list[str]) -> Generator[str, Any, None]:
    human="\n".join([f"{i+1}: {t}" for i, t in enumerate(texts)])
    for line in self._invoke_response_lines(system, human):
      match = re.search(r"^\d+\:", line)
      if match:
        yield re.sub(r"^\d+\:\s*", "", line)

  def _invoke_response_lines(self, system: str, human: str) -> Generator[str, None, None]:
    stream = self._model.stream(
      input=[
        SystemMessage(content=system),
        HumanMessage(content=human),
      ],
    )
    line_buffer = io.StringIO()
    aggregate: BaseMessageChunk | None = None

    for chunk in stream:
      fragment = str(chunk.content)
      aggregate = chunk if aggregate is None else aggregate + chunk
      lines = fragment.split("\n")
      if len(lines) > 0:
        line_buffer.write(lines[0])
        for line in lines[1:]:
          yield line_buffer.getvalue()
          line_buffer = io.StringIO()
          line_buffer.write(line)

    yield line_buffer.getvalue()

  def _gen_admin_prompt(self, target_lan: str, source_lan: str) -> str:
    return f"""
      You are a translator and need to translate the user's {source_lan} text into {target_lan}.
      I want you to replace simplified A0-level words and sentences with more beautiful and elegant, upper level {target_lan} words and sentences. Keep the meaning same, but make them more literary.
      I want you to only reply the translation and nothing else, do not write explanations.
      A number and colon are added to the top of each line of text entered by the user. This number is only used to align the translation text for you and has no meaning in itself. You should delete the number in your mind to understand the user's original text.
      Your translation results should be split into a number of lines, the number of lines is equal to the number of lines in the user's original text. The content of each line should correspond to the corresponding line of the user's original text.
      All user submitted text must be translated. The translated lines must not be missing, added, misplaced, or have their order changed. They must correspond exactly to the original text of the user.

      Here is an example. First, the user submits the original text in English (this is just an example):
      1: IV
      2: This true without lying, certain & most true:
      3: That which is below is like that which is above and that which is above is like that which is below to do ye miracles of one only thing.
      4: .+
      5: And as all things have been and arose from one by ye mediation of one: so all things have their birth from this one thing by adaptation.

      If you are asked to translate into Chinese, you need to submit the translated content in the following format:
      1: 四
      2: 这是真的，没有任何虚妄，是确定的，最真实的：
      3: 上如其下，下如其上，以此来展现“一”的奇迹。
      4: .+
      5: 万物皆来自“一”的沉思，万物在“一”的安排下诞生。
      """