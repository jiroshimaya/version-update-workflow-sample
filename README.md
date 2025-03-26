# version-update-workflow-sample
このプロジェクトは、Pythonパッケージのバージョンを更新するためのGitHub Actionsのサンプルワークフローです。uvを使用することを前提としています。主な機能は以下の通りです。
- lint、format、testの実行
- Gitタグを用いたバージョン更新
- PyPIおよびTestPyPIへの公開
- sphinxによるdocsの作成とgithub pagesでの公開

#### [English](https://github.com/jiroshimaya/version-update-workflow-sample/blob/main/README.en.md) | [日本語](https://github.com/jiroshimaya/version-update-workflow-sample/blob/main/README.md)

# モチベーション

このプロジェクトのモチベーションは、バージョン管理を一元化し、GitHubとPyPIの状態を自然に同期させることです。

通常、uvを使ってPythonパッケージを作成する際のバージョンアップ手順は以下の通りです：
- `pyproject.toml` の `project.version` を手動で更新
- `uv build && uv publish` を実行（バージョンは `pyproject.toml` に基づいて決定）

GitHubでソースコードを管理する場合、さらに以下の作業が必要です：
- 更新内容をGitHubに反映
- 最新バージョンに対応するGitタグを追加

これらの手順には以下の課題があります：
- バージョンがGitのタグと `pyproject.toml` で二重管理される
- プルリクエスト時に `pyproject.toml` の更新を忘れることがある。忘れると、バージョン更新のためだけのコミットやプルリクエストが必要になる
- GitHubへのプッシュとPyPIへの公開が別々に行われるため、GitHubとPyPIを同じ状態に保つには注意が必要

これらの課題を解決するために、以下を目指しました：
- バージョン情報をGitタグで一元管理
- GitHub Actionsでバージョン更新、ビルド、公開を同時に実行

これにより、`pyproject.toml` とGitタグのバージョンの二重管理を避けることができます。また、GitHub Actionsを通じてPyPIを更新することで、GitHubとPyPIの状態を意識せずに一致させることができ、開発の効率化につながると考えました。

# 利用ツール

- **パッケージ管理**: uv
- **Lintツール**: ruff, mypy
- **フォーマットツール**: ruff
- **テストツール**: pytest, bats, act
- **タスク管理**: taskipy
- **ビルドツール**: hatchling, hatch-vcs
- **ドキュメント作成**: sphinx

# 使い方

## GitHub Actionsでの実行

### 準備
「共通」は原則実施してください。
その他は対応する機能を使用する場合は実施してください。
#### 共通
- `.github`ディレクトリとその中身をリポジトリにアップロード
- GitHub > Setting > Actions > General > Workflow Permissionでread and write permissionsを選択

#### PyPI
- GitHubのSecretsに`TEST_PYPI_TOKEN`と`PYPI_TOKEN`を登録します。

#### docs
- GitHub > Settings > Pages で、Source を "GitHub Actions" に設定
- pyproject.toml > tool.taskipy.tasks > docs-generateの行のsrc/MYPKGをを適切なフォルダ名に書き換え
- docs/source/index.rstのプロジェクト説明部分を記載
- `uv run task docs-generate && uv run task docs-open`でドキュメントファイルの生成ができるか確認

### python-check.yaml
- `.py`ファイルに対して、LintとFormatを実施します。
- `main`ブランチへのプルリクエストをトリガーとします。

### publish-to-testpypi.yaml
- バージョン更新とTestPyPIへの公開を行います。
- GitHub Actionsから手動で実行します。
- 実行時に以下のオプションを指定できます（すべて任意）:
  - **バージョン番号**: `v`で始まるセマンティックバージョニング形式の番号。空欄の場合、`v`で始まる最新のタグが使用されます。
  - **Recreate Tag**: チェックすると、指定されたバージョン番号が既に存在する場合、タグを作り直します。
  - **Dry Run**: チェックすると、リモートへのタグのプッシュやTestPyPIへの公開など、Workflow外に影響を残す処理を行いません。

### publish-to-pypi.yaml
このファイルは、バージョンを更新し、PyPIにパッケージを公開するためのものです。  
実行方法や指定可能なオプションは、`publish-to-testpypi.yaml`と同じです。

### update-version.yaml
- このワークフローは、バージョンを更新するためのものです。GitHubに指定したタグをプッシュします。これは、publish-to-testpypi.yamlからTestPYPIへの公開処理を除いたものです。
- update-version-simple.yamlはシンプルバージョンです。インクリメントの種類（patch, minor, major）を選ぶだけで自動でインクリメントします。
- auto-update-version.yamlはpushによって.pyが変更されたら自動でpatchバージョンのインクリメントを実施するワークフローです。pushがPRのマージのみによって行われるのであれば、autoでもいいかと思います。

### docs.yaml
- sphinxによりドキュメントページを自動生成し、github pagesにデプロイします。
- デフォルトではセマンティックバージョン形式（v*.*.*）のタグがpushされたときに実行されます。

## ローカルでの実行
### 環境構築
以下はM1 macOSでの手順です。他のOSを使用している場合は、適宜読み替えてください。

#### [uv](https://github.com/astral-sh/uv)
```sh
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### dockerまたは[docker desktop](https://www.docker.com/ja-jp/products/docker-desktop/)
actを実行するために必要です。商用利用する際は、利用規約に注意してください。

#### [act](https://github.com/nektos/act)
このツールは、ローカル環境でGitHub Actionsを実行するために使用します。  
Dockerコンテナ内でアクションを実行し、コンテナのサイズは3種類から選べます。ここではMediumサイズを選択します。

``` 
brew install act
act --container-architecture linux/amd64
# コンテナのサイズを聞かれたらMediumを選択
```

#### [bats](https://github.com/bats-core/bats-core)
bashのテストツールです。

```
# batsのインストール。ローカルでシェルのテストをしたい場合のみ必要
brew install bats
```

### 単体実行

#### テスト

uv経由でpytestを実行できます。

```sh
uv run task test
```

#### update_version.sh
workflowでのバージョン更新に用いるシェルスクリプトです。

```sh
sh .github/scripts/update_version.sh [-v version] [-i increment_type] [-n] [-d]
```

詳細は以下を御覧ください。
https://gist.github.com/jiroshimaya/5f4524ca296357e1c5347f1674217529

### workflow

actでworkflowのテストを実行できます。

```sh
act [trigger] -j [jobname] -W [workflow yaml filepath] -e [event file path]
```

#### テスト

トリガーまたはjobを指定して実行します。
```sh
# triggerとしてpull_requestを指定
act pull_request -W .github/workflows/python-check.yaml
# jobを指定
act -j test -W .github/workflows/python-check.yaml
```

#### publish
原則として、dry-runで実行してください。テスト中に実際にpublishされると、管理が複雑になるためです。
workflow_dispatchがトリガーとなるジョブの場合は、eventファイルで必要な入力を指定します。

```json:tests/workflow/event.json
{"inputs": {"version": "", "recreate": "true", "dry_run": "true"}}
```

```sh
act -j publish -W .github/workflows/publish-to-testpypi.yaml -e tests/workflow/event.json
```

複数のeventに対してテストしたい場合はスクリプトを使用してください。

```sh
uv run task test-workflow # batsで実行
uv run task test-workflow-py # pytestで実行
```
