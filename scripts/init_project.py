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
    update_pyproject_toml()
