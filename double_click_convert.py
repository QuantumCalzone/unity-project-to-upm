import convert
import os
from pathlib import Path

active_script = os.path.realpath(__file__)
active_script_path = Path(active_script)

convert.convert(active_script_path.parent.parent)

print("")
os.system("pause")
