from dataclasses import dataclass
from pathlib import Path
from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
  books_folder_path: str
  translated_folder_path: str | None
  formats: list[typing.Literal[".pdf", ".cbz", ".cbr", ".epub"]]
class Outputs(typing.TypedDict):
  items: list[list[dict]]
  translated_folder_path: list[str]
#endregion


@dataclass
class _Item:
  input: str
  output: str

def main(params: Inputs, context: Context) -> Outputs:
  input_path = Path(params["books_folder_path"])
  output_path = params["translated_folder_path"]
  formats = params["formats"]
  if output_path is None:
    output_path = Path(context.session_dir)
    output_path = output_path / "manga-translator"
    output_path = output_path / f"{context.job_id}"
  else:
    output_path = Path(output_path)

  items: list[_Item] = []
  for file in input_path.rglob("*"):
    if not file.is_file():
      continue
    if file.suffix not in formats:
      continue
    relatived = file.relative_to(input_path)
    translated_file = output_path / relatived
    translated_file.parent.mkdir(parents=True, exist_ok=True)
    if file.suffix == ".cbr": # cannot gen *.cbr file
      translated_file.suffix = ".cbz"

    items.append(_Item(
      input=str(file),
      output=str(translated_file),
    ))
  return {
    "items": items,
    "translated_folder_path": output_path,
  }