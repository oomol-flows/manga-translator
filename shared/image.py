from typing import IO
from PIL.Image import registered_extensions, SAVE, Image


def parse_format(format: str, origin_ext_name: str | None = None) -> tuple[str, str]:
  if format not in SAVE:
    format = "PNG" # unsupported format, default to PNG
  ext_names = _FORMAT2EXT.get(format, None)
  ext_name: str
  if ext_names is None:
    format = "PNG"
    ext_name = ".png"
  elif origin_ext_name is not None and \
       origin_ext_name in ext_names:
    ext_name = origin_ext_name
  else:
    ext_name = ext_names[0]
  return format, ext_name

def save_image(image: Image, output: IO[bytes], format: str):
  if format not in _FORMATS_SUPPORTS_RGBA and image.format != "RGB":
    image = image.convert("RGB")
  image.save(output, format)

def _reverse(origin: dict[str, str]) -> dict[str, list[str]]:
  target: dict[str, list[str]] = {}
  for key, value in origin.items():
    if value in target:
      target[value].append(key)
    else:
      target[value] = [key]
  for keys in target.values():
    keys.sort()
    keys.reverse()
  return target

_FORMAT2EXT: dict[str, list[str]] = _reverse(registered_extensions())
_FORMATS_SUPPORTS_RGBA = (
  "DDS", "GIF", "PNG", "JPEG2000", "ICNS", "ICO",
  "TIFF", "PSD", "QOI", "SGI", "TGA", "WEBP",
)