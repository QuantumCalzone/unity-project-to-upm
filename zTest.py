import json
import os
import re

verbose = True
project_path = r"C:\Users\georg\Projects\UnityFramework"

package_json_path = os.path.join(project_path, "Packages", os.path.basename(project_path), "package.json")
print(f"package_json_path: {package_json_path}")


def get_new_version(project_path):
    if verbose:
        print(f"get_new_version( project_path: {project_path} )")

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

    new_version = get_new_version(project_path)
    package_json_data = {}

    with open(package_json_path) as package_json:
        package_json_data = json.load(package_json)
        package_json_data["version"] = new_version

    with open(package_json_path, 'w') as package_json:
        json.dump(package_json_data, package_json, indent=4, separators=(',', ': '))


increment_version(package_json_path)
