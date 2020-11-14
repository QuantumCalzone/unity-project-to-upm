import os
import sys
import subprocess
import importlib.util
from importlib.machinery import SourceFileLoader
import importlib

active_script = os.path.realpath(__file__)
active_script_dir = os.path.dirname(active_script)
print("")

upm_dir = os.path.join(active_script_dir, "unity-project-to-upm")
upm_dir = upm_dir if not os.path.islink(upm_dir) else os.readlink(upm_dir)
print(f"upm_dir: {upm_dir}")
auto_convert_path = os.path.join(upm_dir, "auto_convert.py")
print(f"auto_convert_path: {auto_convert_path}")
# subprocess.call(auto_convert_path, shell=True)

# module = importlib.load_source("auto_convert", auto_convert_path)

# sys.path.append(auto_convert_path)
# sys.path.append(os.path.dirname(os.path.expanduser(auto_convert_path)))
# print(os.path.dirname(os.path.expanduser(auto_convert_path)))
# import auto_convert

loader = importlib.machinery.SourceFileLoader("auto_convert", auto_convert_path)
# loader.create_module()
# auto_convert = loader.exec_module("auto_convert")
print(f"loader.path : f{loader.path}")
print(f"loader.contents : f{loader.contents()}")
print(f"loader.is_package : f{loader.is_package()}")
print(f"loader.is_resource : f{loader.is_resource()}")

# auto_convert_spec = importlib.util.spec_from_file_location("auto_convert", auto_convert)
# auto_convert_spec_module = importlib.util.module_from_spec(auto_convert_spec)
# sys.modules[auto_convert_spec_module.name] = auto_convert_spec_module
# auto_convert_spec.loader.exec_module(auto_convert_spec_module)
# auto_convert_spec_module.convert("idk")

print("")
os.system("pause")
