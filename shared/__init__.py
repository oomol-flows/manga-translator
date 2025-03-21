import os
import sys

sys.path.append(
  os.path.abspath(os.path.join(__file__, "..", "..", "manga")),
)

from .translator import *