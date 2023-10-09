from glob import iglob
import os
import sys


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


src_directory = sys.argv[1]

if not src_directory:
    raise "No path to src directory"

build_directory = src_directory + "../"
result_file_name = "TelegramAnnouncer.py"
database_providers_directory = src_directory + "database_providers/*"
service_providers_directory = src_directory + "services/*"
clients_directory = src_directory + "clients/*"
enums_directory = src_directory + "core/enums/*"
types_directory = src_directory + "core/types/*"
menu_directory = src_directory + "core/menu/*"
runners_directory = src_directory + "core/runners/**/*"
main_path = src_directory + "main.py"

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

result = merge_file(src_directory + "main.py", result)
result = result.replace("..", ".")
safe_write_in_file(build_directory, result_file_name, result)

print("Build is finished successfully")
