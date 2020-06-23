import shutil
import pygit2
from pythonutils.input_utils import *
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
input_project_path = r"/Users/georgekatsaros/Projects/UnityFramework"
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


def read_git_info(file_name):
    if verbose:
        print(f"read_git_info( file_name: {file_name} )")

    active_script_path = os.path.realpath(__file__)
    project_path = get_parent_dir(active_script_path)

    git_info_path = os.path.join(project_path, f"{file_name}.txt")
    ensure_file_path_exists(git_info_path)

    git_info_file = open(git_info_path, "r")
    git_info = git_info_file.read()
    git_info_file.close()

    return git_info


upm_branch = repository.lookup_branch("upm")

if upm_branch is not None:
    repository.branches.delete("upm")

most_recent_commit = repository[repository.head.target]
repository.create_branch("upm", most_recent_commit)
switch_branch("upm")

delete_root_folder("Library")
delete_root_folder("Packages")
delete_root_folder("ProjectSettings")


project_dirs = get_all_in_dir(target_dir=input_project_path, full_path=True, recursive=True, include_dirs=True,
                              include_files=False)
for project_dir in project_dirs:
    project_dir_contents = os.listdir(project_dir)
    print(project_dir_contents)
    is_empty = len(project_dir_contents) == 0
    print(f"project_dir: {is_empty}")


assets_folder_path = os.path.join(input_project_path, "Assets")
assets = get_all_in_dir(assets_folder_path)
for asset in assets:
    new_asset_path = asset.replace(assets_folder_path, input_project_path)
    shutil.move(asset, new_asset_path)

os.rmdir(assets_folder_path)

user_name = read_git_info("user_name")
user_mail = read_git_info("user_mail")

if user_name == "" or user_mail == "":
    print("You need to fill out info!")
else:
    index = repository.index
    index.add_all()
    index.write()
    author = pygit2.Signature(user_name, user_mail)
    commiter = pygit2.Signature(user_name, user_mail)
    tree = repository.TreeBuilder().write()
    commit = repository.create_commit("refs/heads/upm", author, commiter, "Package", tree, [repository.head.target])

    # sshcred = repository.credentials.Keypair("git", "/path/to/id_rsa.pub", "/path/to/id_rsa", "")
    # repository.crendentals = sshcred
    #
    # repository.remotes["origin"].push(["refs/heads/upm:refs/heads/upm"])

    # switch_branch("master")
