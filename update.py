import os
import shutil
from glob import iglob
from urllib.request import urlopen
import requests


def find_greater_version(version1: str, version2: str):
    if version1 == version2:
        return version1

    version1_symbols = version1.split('.')
    version2_symbols = version2.split('.')

    try:
        if int(version1_symbols[0]) > int(version2_symbols[0]):
            return version1

        if int(version1_symbols[0]) < int(version2_symbols[0]):
            return version2

        if int(version1_symbols[1]) > int(version2_symbols[1]):
            return version1

        if int(version1_symbols[1]) < int(version2_symbols[1]):
            return version2

        if int(version1_symbols[2]) > int(version2_symbols[2]):
            return version1

        if int(version1_symbols[2]) < int(version2_symbols[2]):
            return version2

        return version1
    except IndexError or ValueError:
        print("Bad version")
        return version2


def update(version, current_directory_path):
    temp_path = current_directory_path + "temp/"
    downloaded_path = "{0}TelegramAnnouncer-{1}/".format(temp_path, version)
    archive_format = "zip"
    archive_name = "v{0}.{1}".format(version, archive_format)
    archive_link = "https://github.com/d1mak3/TelegramAnnouncer/archive/refs/tags/" + archive_name
    os.mkdir(temp_path)
    request_stream = requests.get(archive_link, allow_redirects=True)
    open(temp_path + archive_name, "wb").write(request_stream.content)
    shutil.unpack_archive(temp_path + archive_name, temp_path, archive_format)

    for path in iglob(current_directory_path + "**"):
        if "temp" in path:
            continue

        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

    for path in iglob(downloaded_path + "**"):
        shutil.move(path, current_directory_path)

    shutil.rmtree(temp_path)
    os.system("python3 install.py")


current_dir = os.path.abspath(os.curdir) + '/'

try:
    with open("version", "r") as version_file:
        local_version = version_file.read()
except FileNotFoundError:
    local_version = ""

need_to_update = local_version == ""

version_url = "https://raw.githubusercontent.com/d1mak3/TelegramAnnouncer/develop/version"
latest_version = urlopen(version_url).read().decode("utf-8").replace('\n', '')

if need_to_update:
    update(latest_version, current_dir)
    print("Обновление успешно установлено")

if find_greater_version(local_version, latest_version) == latest_version:
    need_to_update = input("Вышла новая версия! Обновить TelegramAnnouncer?(Д/н): ").lower() in ["д", "y"]

if need_to_update:
    update(latest_version, current_dir)
    print("Обновление успешно установлено")

