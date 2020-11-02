import convert
from pythonutils.input_utils import *

input_project_path = stripped_input("Enter/paste the project path: ")
# input_project_path = r"C:\Users\georg\Projects\UnityFramework"

convert.convert(input_project_path)
