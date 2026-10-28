# 変更履歴

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/CHANGELOG.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/CHANGELOG.ja.md)

## v0.0.7 - 2026-10-28

### 実行系の構成方針（主要変更）

- 従来の `examples/` から実行スクリプト一式をコピーする方式を整理し、**編集用の計算条件 (`*_init.py`) と、通常変更しない計算実行処理を分離する**方針を明記。
- 実行処理は `src/vasp_util/runners/` に配置し、既存のライブラリ `vasp.py` と実行用 `vasp.py` の名前空間を区別する設計とした。
- `scripts/` は利用者が編集する雛形の配布元とし、`install.py` で作業ディレクトリに配置する。`rmc_util` と役割分担を揃え、`rmc_dft` を統合層として単純化することを目指す。
- `runners/` への移行完了や具体的な雛形の同梱は、今回の提供資料からは確認できないため完了扱いにはしない。

### 編集用スクリプトの配置機能

- 編集用の計算スクリプトをカレントディレクトリへコピーする `src/vasp_util/install.py` を追加。
- `pyproject.toml` の `[project.scripts]` に `vasp_util = "vasp_util.install:main"` を登録。
- リポジトリ直下の `scripts/` にある `.py` と `.sh` を `share/vasp_util/scripts` に同梱する設定を追加。
- `vasp_util install` は既存ファイルを上書きせず、`vasp_util install --force` で明示的に上書きする仕様とした。
- READMEの日本語版・英語版に使い方を追記。コピー済みのファイルはパッケージ更新時に自動更新されない。

今回提供された資料には過去バージョンの変更履歴が含まれていないため、過去の履歴は記載していません。
