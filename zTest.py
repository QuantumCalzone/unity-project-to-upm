from pythonutils.os_utils import *

names_to_ignore = {
    ".git",
    ".gitattributes",
    ".DS_Store",
    "Assets",
    "package.json",
    "package.json.meta",
}

input_project_path = r"C:\Users\georg\Projects\UnityFramework"

project_folders = get_all_in_dir(target_dir=input_project_path, full_path=True, recursive=False,
                                 include_dirs=True, include_files=False)

for project_folder in project_folders:
    project_folder_name = os.path.basename(project_folder)
    if project_folder_name not in names_to_ignore:
        print(project_folder_name)
