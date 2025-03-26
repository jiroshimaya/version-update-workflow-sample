# version-update-workflow-sample
This project is a sample workflow for updating Python package versions using GitHub Actions. It assumes the use of uv. The main features are as follows:
- Execution of lint, format, and test
- Version updates using Git tags
- Publishing to PyPI and TestPyPI

#### [English](https://github.com/jiroshimaya/version-update-workflow-sample/blob/main/README.md) | [日本語](https://github.com/jiroshimaya/version-update-workflow-sample/blob/main/README.ja.md)

# Motivation

The motivation for this project is to centralize version management and naturally synchronize the states of GitHub and PyPI.

Typically, when creating a Python package using uv, the version upgrade procedure is as follows:
- Manually update `project.version` in `pyproject.toml`
- Execute `uv build && uv publish` (the version is determined based on `pyproject.toml`)

When managing source code on GitHub, the following additional tasks are required:
- Reflect the updates on GitHub
- Add a Git tag corresponding to the latest version

These procedures have the following challenges:
- Versions are managed in both Git tags and `pyproject.toml`
- There is a possibility of forgetting to update `pyproject.toml` during a pull request. If forgotten, a commit or pull request solely for version updates becomes necessary
- Since pushing to GitHub and publishing to PyPI are done separately, care is needed to keep GitHub and PyPI in the same state

To solve these challenges, we aimed for the following:
- Centralize version information management with Git tags
- Simultaneously execute version updates, builds, and publishing with GitHub Actions

This approach avoids the dual management of versions in `pyproject.toml` and Git tags. Additionally, by updating PyPI through GitHub Actions, it is possible to keep GitHub and PyPI in sync without conscious effort, leading to improved development efficiency.

# Tools Used

- **Package Management**: uv
- **Lint Tools**: ruff, mypy
- **Format Tools**: ruff
- **Test Tools**: pytest, bats, act
- **Task Management**: taskipy
- **Build Tools**: hatchling, hatch-vcs

# Usage

## Execution with GitHub Actions

### Preparation
1. Upload the `.github` directory and its contents to the repository.
2. Register `TEST_PYPI_TOKEN` and `PYPI_TOKEN` in GitHub Secrets.
3. Select `read and write permissions` in GitHub > Settings > Actions > General > Workflow Permissions

### `python-check.yaml`
- Perform Lint and Format on `.py` files.
- Trigger on pull requests to the `main` branch.

### `publish-to-testpypi.yaml`
- Performs version updates and publishes to TestPyPI.
- Manually executed from GitHub Actions.
- The following options can be specified at execution (all optional):
  - **Version Number**: A semantic versioning format number starting with `v`. If left blank, the latest tag starting with `v` is used.
  - **Recreate Tag**: If checked, the tag is recreated if the specified version number already exists.
  - **Dry Run**: If checked, operations that affect outside the Workflow, such as pushing tags to remote and publishing to TestPyPI, are not performed.

### publish-to-pypi.yaml
This file is for updating the version and publishing the package to PyPI.  
The execution method and options that can be specified are the same as `publish-to-testpypi.yaml`.

### update-version.yaml
- This is a workflow for updating versions. It pushes the specified tag to GitHub. It is the same as publish-to-testpypi.yaml but without the publish process.

## Local Execution
### Environment Setup
The following is the procedure for M1 macOS. If you are using another OS, please adjust accordingly.

#### [uv](https://github.com/astral-sh/uv)
```sh
# Installation of uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### docker or [docker desktop](https://www.docker.com/ja-jp/products/docker-desktop/)
It is necessary to run act. Please be aware of the terms of use when using it commercially.

#### [act](https://github.com/nektos/act)
This tool is used to execute GitHub Actions in a local environment.  
Actions are executed within a Docker container, and you can choose from three container sizes. Here, the Medium size is selected.

``` 
brew install act
act --container-architecture linux/amd64
# When asked for the container size, select Medium
```

#### [bats](https://github.com/bats-core/bats-core)
It is a testing tool for bash.

```
# Installation of bats. Only necessary if you want to test shell scripts locally.
brew install bats
```

### Standalone Execution

#### Test

You can run pytest via uv.

```sh
uv run task test
```

#### update_version.sh
This is a shell script used for version updates in the workflow.

```sh
sh .github/scripts/update_version.sh [-v version] [-i increment_type] [-n] [-d]
```

Please see the details below.
https://gist.github.com/jiroshimaya/5f4524ca296357e1c5347f1674217529

### workflow

You can run workflow tests with act.

```sh
act [trigger] -j [jobname] -W [workflow yaml filepath] -e [event file path]
```

#### テスト

Specify a trigger or job to execute.
```sh
# Specify pull_request as the trigger
act pull_request -W .github/workflows/python-check.yaml
# Specify the job
act -j test -W .github/workflows/python-check.yaml
```

#### publish
It is recommended to execute in dry-run mode. If it is actually published during testing, management becomes complicated. If the job is triggered by workflow_dispatch, specify the necessary inputs in the event file.

```json:tests/workflow/event.json
{"inputs": {"version": "", "recreate": "true", "dry_run": "true"}}
```

```sh
act -j publish -W .github/workflows/publish-to-testpypi.yaml -e tests/workflow/event.json
```

If you want to test against multiple events, please use a script.

```sh
uv run task test-workflow # Execute with bats
uv run task test-workflow-py # Execute with pytest
```
