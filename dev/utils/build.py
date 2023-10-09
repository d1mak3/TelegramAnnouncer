from glob import iglob
import os
import shutil


def merge_file(file_path, result_string):
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if "src" not in line:
            result_string += line

    result_string += "\n\n"

    return result_string


def safe_write_in_file(file_path, file_name, data):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(file_path + file_name, "w") as file:
        file.write(data)


build_directory = "../../build/"
result_file_name = "TelegramAnnouncer.py"
database_providers_directory = "../../src/database_providers/*"
service_providers_directory = "../../src/services/*"
clients_directory = "../../src/clients/*"
enums_directory = "../../src/core/enums/*"
types_directory = "../../src/core/types/*"
menu_directory = "../../src/core/menu/*"
runners_directory = "../../src/core/runners/**/*"
main_path = "../../src/main.py"
requirements_path = "../requirements.txt"
license_path = "../../LICENSE"

result = ""

for path in iglob(database_providers_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)

for path in iglob(service_providers_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)

for path in iglob(clients_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)


for path in iglob(enums_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)


for path in iglob(types_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)

for path in iglob(menu_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)

for path in iglob(runners_directory, recursive=True):
    if not os.path.isfile(path) or "__pycache__" in path:
        continue

    result = merge_file(path, result)

result = merge_file(main_path, result)
safe_write_in_file(build_directory, result_file_name, result)
shutil.copy(requirements_path, build_directory + "requirements.txt")
shutil.copy(license_path, build_directory + "LICENSE")

print("Build is finished successfully")
