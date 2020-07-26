import shutil
import pyperclip
import pygit2
from pythonutils.input_utils import *
from pythonutils.os_utils import *

verbose = True
names_to_ignore = {
    ".git",
    "Packages",
}

input_project_path = stripped_input("Enter/paste the project path: ")
# input_project_path = r"C:\Users\georg\Projects\UnityFramework"
package_name = os.path.basename(input_project_path)
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
        shutil.rmtree(folder_path, ignore_errors=True)
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

project_root_folders = get_all_in_dir(target_dir=input_project_path, full_path=True, recursive=False,
                                      include_dirs=True, include_files=False)
for project_root_folder in project_root_folders:
    project_root_folder_name = os.path.basename(project_root_folder)
    if project_root_folder_name not in names_to_ignore:
        delete_root_folder(project_root_folder_name)

# delete all empty folders
project_dirs = list(os.walk(input_project_path))[1:]
for project_dir in project_dirs:
    if not project_dir[2]:
        is_empty = len(project_dir[0]) == 0
        if is_empty:
            os.rmdir(project_dir[0])


package_folder_path = os.path.join(input_project_path, "Packages")
package_folder_path = os.path.join(package_folder_path, package_name)
assets = get_all_in_dir(target_dir=package_folder_path, full_path=True, recursive=False, include_dirs=True,
                        include_files=True)
for asset in assets:
    new_asset_path = asset.replace(package_folder_path, input_project_path)
    shutil.move(asset, new_asset_path)

delete_root_folder("Packages")
os.remove(os.path.join(input_project_path, ".gitignore"))


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

    # use this as temp
    print("")
    cd_command = "cd {}".format(input_project_path)
    git_add_command = "git add -A"
    git_commit_command = "git commit -m \"Package\""
    git_push_command = "git push --set-upstream --force origin upm"
    git_checkout_command = "git checkout master"
    git_status_command = "git status"
    print(cd_command)
    print(git_add_command)
    print(git_commit_command)
    print(git_push_command)
    print(git_checkout_command)
    print(git_status_command)
    print("")

    clipboard = "{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n".format(cd_command, git_add_command, git_commit_command,
                                                              git_push_command, git_checkout_command,
                                                              git_status_command)
    pyperclip.copy(clipboard)

    print("That has been copied to you clipboard. Paste it in terminal!")
    print("")

    # switch_branch("master")
