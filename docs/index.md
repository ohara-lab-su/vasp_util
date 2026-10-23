# vasp_util

[GitHub](https://github.com/ohara-lab-su/vasp_util/) / [ohara-lab-su](https://ohara-lab-su.github.io/)

VASP の入力ファイル操作、実行管理、および出力・構造解析を補助する Python パッケージ。

```{toctree}
:maxdepth: 2
:caption: Contents

usage
api/modules
```

## 構成

- `Vasp`: VASP 入力の確認、実行、前処理・後処理の統合。
- `VaspIncar`: INCAR の読み書きとタグ操作。
- `VaspKpoints`: KPOINTS の読み書きと設定変更。
- `VaspLog`: 計算結果の収集、バックアップ、ログファイル操作。
- `VaspOutcar`: OUTCAR のエネルギー、位置、力、磁気モーメントの解析。
- `VaspPoscar`: POSCAR の格子・原子座標の解析。
- `VaspPoscarAnalyzer`: 原子間距離、近接原子、MD 中のジャンプ解析。
- `VaspPotcarBuilder`: 元素に応じた POTCAR の選択と結合。
- `Config`: VASP 実行設定と YAML 設定の読み込み。

具体的な Python スクリプトは [使用マニュアル](usage) に、各クラスの詳細な引数・メソッドは [API リファレンス](api/modules) を参照してください。
