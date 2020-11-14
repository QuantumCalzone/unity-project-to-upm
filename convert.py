from datetime import datetime
import json
import pygit2
import pyperclip
from pythonutils.os_utils import *
import re
import shutil

verbose = True
names_to_ignore = {
    ".git",
    "Packages",
}


def switch_branch(branch_name, repository):
    if verbose:
        print(f"switch_branch( branch_name: {branch_name} , repository: {repository.path} )")

    branch_lookup = repository.lookup_branch(branch_name)
    branch_lookup_reference = repository.lookup_reference(branch_lookup.name)
    repository.checkout(branch_lookup_reference)


def delete_root_folder(folder_name, project_path):
    if verbose:
        print(f"delete_root_folder( folder_name: {folder_name} , project_path: {project_path} )")

    folder_path = os.path.join(project_path, folder_name)

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


def get_new_version(project_path):
    if verbose:
        print(f"get_new_version( project_path: {project_path} )")

    package_json_path = os.path.join(project_path, "Packages", os.path.basename(project_path), "package.json")
    new_version = ""

    with open(package_json_path) as package_json:
        package_json_data = json.load(package_json)
        version = package_json_data["version"]
        print(f"version: {version}")
        numbers = re.findall(r"\d+(?!\d+)", version)
        print(f"numbers: {numbers}")
        last_number = numbers[len(numbers) - 1]
        print(f"last_number: {last_number}")
        new_version = version[:-len(last_number)]
        new_version = new_version + str(int(last_number) + 1)
        print(f"new_version: {new_version}")

    return new_version


def increment_version(project_path):
    if verbose:
        print(f"increment_version( project_path: {project_path} )")

    package_json_path = os.path.join(project_path, "Packages", os.path.basename(project_path), "package.json")
    new_version = get_new_version(project_path)
    package_json_data = {}

    with open(package_json_path) as package_json:
        package_json_data = json.load(package_json)
        package_json_data["version"] = new_version

    with open(package_json_path, 'w') as package_json:
        json.dump(package_json_data, package_json, indent=4, separators=(',', ': '))


def commit_changes(repository, author, commiter, message):
    if verbose:
        print(f"commit_changes( repository: {repository.path} , f{author} , f{commiter} , {message} )")

    repository.index.add_all()
    repository.index.write()

    repository.create_commit(
        "refs/heads/master",
        author,
        commiter,
        message,
        repository.index.write_tree(),
        [repository.head.target]
    )


def convert(project_path):
    if verbose:
        print(f"convert( file_name: {project_path} )")

    user_name = read_git_info("user_name")
    user_mail = read_git_info("user_mail")

    if user_name == "" or user_mail == "":
        print("You need to fill out info!")
    else:
        package_name = os.path.basename(project_path)
        input_project_git_path = os.path.join(project_path, ".git")
        repository = pygit2.Repository(input_project_git_path)

        author = pygit2.Signature(user_name, user_mail)
        commiter = pygit2.Signature(user_name, user_mail)

        increment_version(project_path)

        commit_changes(repository, author, commiter, "incremented version")

        upm_branch = repository.lookup_branch("upm")

        if upm_branch is not None:
            repository.branches.delete("upm")

        most_recent_commit = repository[repository.head.target]
        repository.create_branch("upm", most_recent_commit)
        switch_branch("upm", repository)

        # delete all folders at root (except the ones we need to keep)
        project_root_folders = get_all_in_dir(target_dir=project_path, full_path=True, recursive=False,
                                              include_dirs=True, include_files=False)
        for project_root_folder in project_root_folders:
            project_root_folder_name = os.path.basename(project_root_folder)
            if project_root_folder_name != "Packages" and project_root_folder_name != ".git":
                print(f"deleting {project_root_folder_name}")
                delete_root_folder(project_root_folder_name, project_path)

        # delete all files at root
        project_root_files = get_all_in_dir(target_dir=project_path, full_path=True, recursive=False,
                                            include_dirs=False, include_files=True)
        for root_file in project_root_files:
            os.remove(root_file)

        # delete all empty folders
        project_dirs = list(os.walk(project_path))[1:]
        for project_dir in project_dirs:
            if not project_dir[2]:
                is_empty = len(project_dir[0]) == 0
                if is_empty:
                    os.rmdir(project_dir[0])

        temp_id = f"{datetime.utcnow()}"
        temp_id = temp_id.replace(":", "-")
        temp_id = temp_id.replace(".", "-")
        temp_id = f"{temp_id}-temp"
        temp_dir = os.path.join(project_path, temp_id)
        os.makedirs(temp_dir)

        package_folder_path = os.path.join(project_path, "Packages", package_name)
        assets = get_all_in_dir(target_dir=package_folder_path, full_path=True, recursive=False, include_dirs=True,
                                include_files=True)
        for asset in assets:
            new_asset_path = asset.replace(package_folder_path, temp_dir)
            shutil.move(asset, new_asset_path)

        delete_root_folder("Packages", project_path)

        temp_files = get_all_in_dir(target_dir=temp_dir, full_path=True, recursive=False,
                                    include_dirs=True, include_files=True)
        for temp_file in temp_files:
            new_asset_path = temp_file.replace(temp_dir, project_path)
            shutil.move(temp_file, new_asset_path)

        delete_root_folder(temp_id, project_path)

        index = repository.index
        index.add_all()
        index.write()
        tree = repository.TreeBuilder().write()
        commit = repository.create_commit("refs/heads/upm", author, commiter, "Package", tree, [repository.head.target])
        # commit_changes(repository, author, commiter, "Package")

        # sshcred = repository.credentials.Keypair("git", "/path/to/id_rsa.pub", "/path/to/id_rsa", "")
        # repository.crendentals = sshcred
        #
        # repository.remotes["origin"].push(["refs/heads/upm:refs/heads/upm"])

        # use this as temp
        print("")
        cd_command = "cd {}".format(project_path)
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
        # clipboard = "{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}\r\n".format(cd_command,
        #                                                           git_push_command, git_checkout_command,
        #                                                           git_status_command)
        pyperclip.copy(clipboard)

        print("That has been copied to you clipboard. Paste it in terminal!")
        print("")

        # switch_branch("master")
