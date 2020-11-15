import converter.converter as converter
from pythonutils.input_utils import *

input_project_path = stripped_input("Enter/paste the project path: ")
# input_project_path = r"C:\Users\georg\Projects\UnityFramework"
# input_project_path = r"/Users/georgekatsaros/Projects/UnityFrameworkPlugins"

converter.convert(input_project_path)
