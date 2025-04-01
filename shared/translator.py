import re
import io

from typing import final, cast, Any, Callable
from collections.abc import Generator
from oocana import Context

from shared.manga_translator import SourceLanguage, TargetLanguage
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessageChunk


ProgressReporter = Callable[[float], None]

@final
class Translator:
  def __init__(
      self,
      llm_model: dict[str, Any],
      context: Context,
      source_language: SourceLanguage,
      target_language: TargetLanguage,
      report_progress: ProgressReporter,
    ) -> None:

    env = context.oomol_llm_env
    model: str = llm_model["model"]
    temperature: float = float(llm_model["temperature"])
    top_p: float = float(llm_model["top_p"])
    self._model = ChatOpenAI(
      api_key=cast(Any, env["api_key"]),
      base_url=env["base_url_v1"],
      model=model,
      temperature=temperature,
      top_p=top_p,
    )
    self._source_language: SourceLanguage = source_language
    self._target_language: TargetLanguage = target_language
    self._report_progress: ProgressReporter = report_progress

  def translate(self, code_map: dict[str, str], queries: list[str]) -> list[str]:
    source: str = self._source_language
    target: str = self._target_language

    target = code_map[target]
    if source == "auto":
      source = ""
    else:
      source = code_map[source]

    system = self._gen_admin_prompt(source, target)
    translated_list: list[str] = []

    for i, translated in enumerate(self._translate_text_by_text(system, queries)):
      translated_list.append(translated)
      self._report_progress((i + 1) / len(queries))

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

  def _gen_admin_prompt(self, source: str, target: str) -> str:
    users_what: str = ""
    first_line_suffix: str = ""

    if source == "":
      users_what = "in an unknown language "
      first_line_suffix = " (please judge the language of user-submitted text by yourself)"
    else:
      users_what = source + " "

    return f"""
      You are a translator who needs to translate user-submitted {users_what}text into {target}{first_line_suffix}.
      Your translation should keep the original meaning intact, and maintain the style and tone of the original text.
      For example, if the original text is serious, the translation should be serious; if the original text is colloquial,
      the translation should also be colloquial. Pay attention to distinguishing the tone and speaking style of different characters,
      and retain the character's quirks in the translation. It is necessary to ensure that the translation does not lose the style of the original text.
      I hope you only reply to the translation, not to anything else, and do not write explanations.
      A number and colon will be added to the top of each line of text entered by the user. This number is only used to align the translated text for you and has no meaning by itself. You should delete this number in your mind to understand the user's original text.
      Your translation results should be divided into a number of lines, the number of lines is equal to the number of lines in the user's original text. The content of each line should correspond to the corresponding line of the user's original text.
      All user-submitted texts must be translated. The translated lines must not be lost, added, misplaced, or changed in order. They must correspond exactly to the user's original text.
      The content must be translated into the correct language, and direct replies to the original text are prohibited.

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