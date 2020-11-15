import converter.converter as converter
import os
from pathlib import Path

active_script = os.path.realpath(__file__)
active_script_path = Path(active_script)

converter.convert(active_script_path.parent.parent)

print("")
os.system("pause")
