import os
import shutil


def safe_create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


shutil.rmtree(".github/")
shutil.rmtree(".git/")
shutil.rmtree(".idea/")
os.remove(".gitignore")
os.remove(".gitkeep")

os.system("python3 -m pip install --upgrade pip")
os.system("pip install -r dev/requirements.txt")
os.system('python3 dev/utils/build.py "$(pwd)/src/"')

shutil.rmtree("src/")
shutil.rmtree("dev/")

safe_create_dir("env/")
safe_create_dir("messages/")
os.remove("install.py")
