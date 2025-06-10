import datetime
import shutil
import os
import subprocess
import json
from pathlib import Path


def log(msg):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"[{now}] {msg}")


def clone_repo(repo_url, temp_dir):
    log(f"Клонирование репозитория: {repo_url}")
    subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
    log("Клонирование завершено")


def del_dirs(temp_dir, repo_path):
    log("Удаление всех директорий в корне, кроме директории исходного кода")
    for smth in os.listdir(temp_dir):
        smth_path = os.path.join(temp_dir, smth)
        if not os.path.samefile(
            os.path.join(temp_dir, repo_path.split(os.sep)[0]), smth_path
        ):
            if os.path.isdir(smth_path):
                shutil.rmtree(smth_path)
            else:
                os.remove(smth_path)
    log("Удаление завершено")


def create_json(source_path, version):
    log("Создание служебного файла «version.json»")
    files = [
        f
        for f in os.listdir(source_path)
        if f.endswith((".py", ".js", ".sh"))
        and os.path.isfile(os.path.join(source_path, f))
    ]
    version_data = {"name": "hello world ", "version": version, "files": files}
    with open(os.path.join(source_path, "version.json"), "w") as f:
        json.dump(version_data, f, indent=1)
    log("Файл «version.json» создан")


def create_archive(source_path):
    log("Создание архива")
    archive_date = datetime.datetime.now().strftime("%d%m%Y")
    archive_name = Path(source_path).name + archive_date
    shutil.make_archive(archive_name, "zip", source_path)
    log(f"Архив создан: {archive_name}.zip")


def build(repo_url, repo_path, version):
    temp_dir = "temp_dir"
    shutil.rmtree(temp_dir, ignore_errors=True)
    clone_repo(repo_url, temp_dir)

    source_path = os.path.join(temp_dir, repo_path)

    del_dirs(temp_dir, repo_path)
    create_json(source_path, version)
    create_archive(source_path)

    log("Удаление временных файлов")
    shutil.rmtree(temp_dir, ignore_errors=True)


repo_url = "https://github.com/paulbouwer/hello-kubernetes"
repo_path = "src/app"
version = "25.3000"

# repo_url, repo_path, version = input().split() # если через консоль ввод, (вход(?))

build(repo_url, repo_path, version)
