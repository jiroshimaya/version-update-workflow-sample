import os
import re
import subprocess
import tomllib

import tomlkit


def get_project_name():
    return os.path.basename(os.getcwd())


def get_git_url():
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        url = result.stdout.strip()
        # .gitを除いたURLを返す
        return re.sub(r"\.git$", "", url)
    except subprocess.CalledProcessError:
        return "https://github.com/example/example"


def rename_src_directory():
    """src/version_update_workflow_sampleをsrc/{PROJECTNAME}にリネームする"""
    project_name = get_project_name()
    old_dir = "src/version_update_workflow_sample"
    new_dir = f"src/{project_name.replace('-', '_')}"

    if not os.path.exists(old_dir):
        print(f"Warning: {old_dir} does not exist")
        return

    if os.path.exists(new_dir):
        print(f"Warning: {new_dir} already exists")
        return

    # ディレクトリをリネーム
    os.rename(old_dir, new_dir)
    print(f"Renamed {old_dir} to {new_dir}")

    # __init__.pyの内容を更新
    init_file = os.path.join(new_dir, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write('def hello() -> str:\n    return "Hello"\n')
        print(f"Updated {init_file}")


def update_pyproject_toml():
    # pyproject.tomlを読み込む
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    # プロジェクト名を更新
    project_name = get_project_name()
    data["project"]["name"] = project_name

    # Homepage URLを更新
    git_url = get_git_url()
    data["project"]["urls"]["Homepage"] = git_url

    # docs-generateコマンドを更新
    docs_cmd = data["tool"]["taskipy"]["tasks"]["docs-generate"]
    new_cmd = docs_cmd.replace(
        "src/version_update_workflow_sample", f"src/{project_name.replace('-', '_')}"
    )
    data["tool"]["taskipy"]["tasks"]["docs-generate"] = new_cmd

    # 変更を保存
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(data))

    print(f"Updated project name to: {project_name}")
    print(f"Updated homepage URL to: {git_url}")
    print("Updated docs-generate command")


if __name__ == "__main__":
    rename_src_directory()
    update_pyproject_toml()
