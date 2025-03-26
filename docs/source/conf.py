import os
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../../src"))


def get_version():
    try:
        # 最新のgit tagを取得
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], universal_newlines=True
        ).strip()
        return tag
    except subprocess.CalledProcessError:
        # git tagが存在しない場合はデフォルトのバージョンを返す
        return "0.1.0"


def get_project_name():
    try:
        # pyproject.tomlからproject.nameを取得
        import tomli

        with open("../../pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
            return pyproject["project"]["name"]
    except (FileNotFoundError, KeyError):
        # pyproject.tomlが存在しない、またはproject.nameが設定されていない場合はデフォルト値を返す
        return "mypkg"


def get_author():
    try:
        # pyproject.tomlからauthorを取得
        import tomli

        with open("../../pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
            return pyproject["project"]["authors"][0]["name"]
    except (FileNotFoundError, KeyError):
        # pyproject.tomlが存在しない、またはauthorが設定されていない場合はデフォルト値を返す
        return "shimajiroxyz"


PROJECT_NAME = get_project_name()
AUTHOR = get_author()
YEAR = datetime.now().year

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = PROJECT_NAME
copyright = f"{YEAR}, {AUTHOR}"
author = AUTHOR
version = get_version()
release = version
language = "ja"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # ソースコード読み込み用
    "sphinx.ext.napoleon",  # docstring パース用
    "sphinxcontrib.autodoc_pydantic",  # pydanticのドキュメント生成用
]


templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# -- Options for sphinx-multiversion -----------------------------------------
# -- Options for sphinx-multiversion -----------------------------------------
