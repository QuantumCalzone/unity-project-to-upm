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
input_project_path = "/Users/georgekatsaros/Projects/UnityPackageTest"
repository = pygit2.Repository(".git")


def switch_branch(branch_name):
    if verbose:
        print(f"switch_branch( branch_name: {branch_name} )")

    branch_lookup = repository.lookup_branch(branch_name)
    branch_lookup_reference = repository.lookup_reference(branch_lookup.name)
    repository.checkout(branch_lookup_reference)


upm_branch = repository.lookup_branch("upm")

if upm_branch is not None:
    repository.branches.delete("upm")

most_recent_commit = repository[repository.head.target]
repository.create_branch("upm", most_recent_commit)
switch_branch("upm")

switch_branch("master")
