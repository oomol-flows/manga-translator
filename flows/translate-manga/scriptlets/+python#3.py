from typing import TypedDict
from collections.abc import Iterable

class Inputs(TypedDict):
  name: str
  meta: dict[str, str]

class Outputs(TypedDict):
  title: str | None
  author: str | None

def main(params: Inputs) -> Outputs:
  name = params["name"]
  meta = params["meta"]
  return {
    "title": extract(meta, ("Title", "Subject", "DocumentTitle")) or name,
    "author": extract(meta, ("Author", "Creator", "Producer", "Publisher")),
  }

def extract(meta: dict[str, str], keys: Iterable[str]) -> str | None:
  for key in keys:
    value = meta.get(key, None)
    if value is not None:
      return value
  return None