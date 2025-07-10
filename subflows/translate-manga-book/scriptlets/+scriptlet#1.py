from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
  format: typing.Literal["cbz", "cbr", "epub", "pdf"]
class Outputs(typing.TypedDict):
  format: typing.Literal["cbz", "epub", "pdf"] | None
#endregion

def main(params: Inputs, context: Context) -> Outputs:
  format = params["format"]
  if format == "cbr":
    format = None
  return { "format": format }
