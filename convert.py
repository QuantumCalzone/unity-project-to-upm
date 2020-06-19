import shutil
import pygit2
from pythonutils.os_utils import *

verbose = True
names_to_ignore = {
    ".git",
    ".gitattributes",
    ".DS_Store",
    "Assets",
    "package.json",
    "package.json.meta",
}

# input_project_path = stripped_input("Enter/paste the project path: ")
input_project_path = r"C:\Users\georg\Projects\UnityBookmarks"
input_project_git_path = os.path.join(input_project_path, ".git")
repository = pygit2.Repository(input_project_git_path)


def switch_branch(branch_name):
    if verbose:
        print(f"switch_branch( branch_name: {branch_name} )")

    branch_lookup = repository.lookup_branch(branch_name)
    branch_lookup_reference = repository.lookup_reference(branch_lookup.name)
    repository.checkout(branch_lookup_reference)


def delete_root_folder(folder_name):
    if verbose:
        print(f"delete_root_folder( folder_name: {folder_name} )")

    folder_path = os.path.join(input_project_path, folder_name)

    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        if verbose:
            print(f"delete_root_folder( folder_name: {folder_name} ) | deleted")
        else:
            if verbose:
                print(f"delete_root_folder( folder_name: {folder_name} ) | could not find")


upm_branch = repository.lookup_branch("upm")

if upm_branch is not None:
    repository.branches.delete("upm")

most_recent_commit = repository[repository.head.target]
repository.create_branch("upm", most_recent_commit)
switch_branch("upm")

delete_root_folder("Library")
delete_root_folder("Packages")
delete_root_folder("ProjectSettings")

assets_folder_path = os.path.join(input_project_path, "Assets")
assets = get_all_in_dir(assets_folder_path)
for asset in assets:
    new_asset_path = asset.replace(assets_folder_path, input_project_path)
    shutil.move(asset, new_asset_path)

os.rmdir(assets_folder_path)

# https://www.google.com/search?q=pygit2+commit+all+changes&rlz=1C1CHBF_enUS838US838&oq=pygit2+commit+all+changes&aqs=chrome..69i57.4807j0j4&sourceid=chrome&ie=UTF-8

# switch_branch("master")
