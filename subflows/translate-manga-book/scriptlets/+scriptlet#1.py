from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
  format: typing.Literal["cbz", "cbr", "epub", "pdf", "zip"]
class Outputs(typing.TypedDict):
  format: typing.NotRequired[typing.Literal["cbz", "epub", "pdf"] | None]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
  format = params["format"]
  # cbr and zip are not supported by archive, convert to cbz (default)
  if format in ("cbr", "zip"):
    format = None  # Will use default (cbz)
  return { "format": format }
