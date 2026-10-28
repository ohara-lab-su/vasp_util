# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fvasp_util-181717?logo=github)](https://github.com/ohara-lab-su/vasp_util/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/vasp_util/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/)

VASP の入力・出力、原子構造の解析、計算実行と結果整理を、研究プログラムから扱うための Python
ライブラリです。[RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/) の VASP 関連ツール基盤として開発したものを、RMC と VASP の機能分離方針に基づき、RMC-DFT 0.7.10 から独立させました。

構造操作や VASP 入出力には [ASE](https://ase-lib.org/) と [pymatgen](https://pymatgen.org/) という充実したライブラリがあります。
`vasp_util` はそれらを置き換えるためのものではありません。既存の機能は利用しながら、計算前後のファイル操作、サイト番号による構造参照、近接原子・原子移動の調査、計算結果の整理、RMCProfile
とのデータ交換など、実際の作業で繰り返し必要になった処理をまとめています。単独の操作は既存ライブラリで実現できても、研究で使う入出力・判断・実行手順を一つの
API にまとめる意味があります。

## 開発の経緯

2010年頃から2015年頃にかけて、VASP を含む結晶構造関連のツール [sae](https://github.com/ohara-lab-su/sae) を開発していました。機能の追加とともに巨大化し、設計にも問題を抱えたため、その後は利用を休止しました。一方で、ASE や pymatgen は大きく発展し、sae をそのまま作り直す必要性も薄れました。

その後、別の解析で使用していた `x_poscar` を基礎として、VASP 関連のツールを再編しました。`x_poscar` は、LAMMPS を用いた解析との連携、Bader 電荷・電荷密度の解析、振動解析などで必要となった POSCAR 関連の処理を含むツールです。`vasp_util` は、過去に作成した VASP ツールのすべてを統合したものではなく、主としてこの `x_poscar` をベースに、VASP の入出力や構造解析に必要な機能をクラス・関数として編纂し直したものです。

その後、`x_poscar` を中心とするこれらのツールを **RMC-DFT の開発の中で再編**し、RMC-DFT 内から VASP を利用するためのツール・クラス基盤として整備しました。現在の `vasp_util` の直接の前身は、この RMC-DFT 内の VASP 関連コードです。

さらに開発方針を変更し、RMC と VASP に関する機能を分離して、それぞれ独立に開発・発展させることにしました。その方針に従って VASP 関連のツール基盤を `vasp_util` として独立させました。RMC と VASP の連携・計算フローに固有の処理は、両ライブラリとは別の `rmc_dft` パッケージで扱う構成です。

現時点では、既存ツールの統廃合や機能整理が十分に完了しているわけではありません。久しぶりに開発を再開してみると、ASE や pymatgen の機能は以前の想定以上に充実していました。そのため、既存ライブラリと重複する実装も残っています。今後は、必要な入出力仕様や研究上の操作を維持しつつ、ASE・pymatgen で代替できる部分を見極めながら整理していく位置づけです。

## 主な機能

- **POSCAR とサイトの参照** — `VaspPoscar` は POSCAR を読み込み、格子、Direct/Cartesian
  座標、元素ごとのサイト番号と全原子の番号を扱います。外部向けの原子番号は原則 1 始まりです。POSCAR
  の単一倍率、負の体積指定、3成分倍率、Selective dynamics 行を考慮して座標を読み込みます。
- **構造・MD の解析** — `VaspPoscarAnalyzer` は原子間距離、元素を指定した近接原子、距離順の近傍、二つの構造間の同一番号サイトの変位、しきい値によるジャンプ判定、MD
  ステップ列でのジャンプ探索・サイト追跡を扱います。原子の対応付けは基本的に同じサイト番号を前提とします。
- **周期セルの幾何演算** — `cell_geometry` は体積、座標変換、折り返し、周期画像探索、原子対ごとの下限距離検査を提供します。
  `minimum_image_vector` は直交座標の距離を評価して有限範囲の格子シフトを探索します。
- **INCAR・KPOINTS** — `VaspIncar` は pymatgen の `Incar` と元ファイルのテキスト行を併用し、コメントや行構成をなるべく保ちながらタグを編集します。
  `VaspKpoints` は pymatgen の `Kpoints` を使い、Gamma/Monkhorst-Pack の格子、シフト、コメントを管理します。どちらも自動保存の設定を持ちます。
- **POTCAR** — `VaspPotcarBuilder` はローカルに用意した PAW データセットから、元素ごとに定義された候補の優先順位と実在ファイルに基づいて
  POTCAR を組み立てます。ポテンシャルの科学的な最適性を自動判定するものではありません。
- **OUTCAR** — `VaspOutcar` は電子反復とイオンステップごとのエネルギー（TOTEN、entropy
  を除いたエネルギー、sigma→0）、位置、力、原子別・全体の磁気モーメントを抽出します。終了判定に通らない OUTCAR は読み込み時に例外になります。
- **実行・結果管理** — `Vasp` は入力の準備、INCAR/KPOINTS の設定、ローカル・MPI・ジョブコマンドによる実行、計算結果の収集とバックアップ、CONTCAR
  の引き継ぎ、CFG 変換をまとめます。`VaspLog` は通常ファイルと `.gz` を考慮したログのコピー・整理などを担当します。
- **RMCProfile との受け渡し** — `poscar2cfg` 系は POSCAR/CONTCAR 相当のファイルを RMCProfile の CFG に変換します。CFG
  のセルベクトルには元の半分、原子座標には `2f−1` の変換を適用する、形式固有の処理です。XDATCAR
  からの構造取り出し、VASP4形式からVASP5形式への補助変換も含まれます。

## ASE・pymatgen との関係

`vasp_util` の機能をすべて独自のアルゴリズムと位置付けるものではありません。POSCAR/XDATCAR
の入出力、座標変換、周期距離、近傍探索、INCAR/KPOINTS/POTCAR/OUTCAR の処理、VASP の実行には ASE や pymatgen に対応する機能があります。実際に
`Vasp` の一部は `ase.io`、`VaspIncar` と `VaspKpoints` は pymatgen を利用しています。

違いは主に **処理のまとまりと入出力の約束**です。例えば `VaspPoscarAnalyzer`
は元素別サイト番号とグローバル番号を結び付け、近傍の元素・サイト番号・距離・変位を返し、同じ番号の原子について MD
ステップ間の変位を調べます。これらの計算要素は ASE/pymatgen でも構成できますが、ここでは研究用の操作としてまとめています。
`VaspIncar` は辞書としてのタグ操作に加え、既存ファイルのコメントを残す編集を行います。`Vasp` は Calculator
だけでなく、入力準備から結果整理・RMC 用変換までを扱います。

内部の計算を ASE/pymatgen
に置き換えられる箇所があれば、置き換えることに支障はありません。ただし、同等性はメソッド名ではなく、座標系、原子番号、周期境界条件、ファイル保持、例外・戻り値まで比較して判断する必要があります。特に
`VaspPoscar.apply_pbc_shortest_direct_vector` は分率座標で候補の長さを比較しており、`cell_geometry.minimum_image_vector`
の直交座標距離による探索とは、非直交セルで必ずしも同じ結果になりません。この違いは現在の実装上の注意点です。

## v0.0.8 における実行スクリプトの構成

計算実行処理と、作業ディレクトリで編集する計算条件・起動処理を分離しました。

- **ライブラリ (`src/vasp_util/`)**：既存の `vasp.py` を含むVASP入出力・構造解析API。
- **runner (`src/vasp_util/runners/run_vasp.py`)**：`run_vasp(...)` による実行処理。元の単独実行用 `__main__` を保持。
- **編集可能な起動スクリプト (`scripts/vasp.py`)**：`Config`、`XLogger`、`VaspLog`、`VaspIncar` を生成し、`run_vasp_init(...)` を実行後、全引数を明示して `run_vasp(...)` を呼び出します。
- **編集可能な条件設定 (`scripts/vasp_init.py`)**：提供された `rmc_vasp_init.py` を基に、KPOINTS・POTCAR・INCARの設定を保持。単独実行用 `__main__` を保持。
- **配置コマンド (`src/vasp_util/install.py`)**：インストール済みの雛形を作業ディレクトリへコピーします。VASPは実行しません。

従来の単独実行コードにあった富岳向けの `sleep 5` と `ls -la ./` は起動スクリプト側に維持しています。不要な環境では作業ディレクトリ側で変更できます。`log_dir_vasp=None`、`run_mode=None`、`postprocess_mode=True` など、デフォルト引数も明示します。

### 編集用ファイルの配置

パッケージをインストールした後、計算用の作業ディレクトリで実行します。

```bash
vasp_util install
```

リポジトリ直下の `scripts/` にある `.py` / `.sh` を配布物に同梱し、**カレントディレクトリにコピー**します。同名ファイルは上書きせずスキップします。明示的に上書きする場合のみ、次を実行します。

```bash
vasp_util install --force
```

`vasp_init.py` で計算条件を編集し、`python vasp.py` で計算を実行します。


コピーした `*_init.py` 等は作業ディレクトリ側で編集します。パッケージの更新だけではコピー済みのファイルは変わりません。`--force` は利用者の編集内容を失わせるため注意してください。実行処理をモジュール側に置くことは、編集用ファイルまで自動更新することを意味しません。

## 利用上の注意

POSCAR/CFG 変換の一部には入力行の配置や Direct 座標を前提とする処理があります。また、MD
ステップ間の変位は同じサイト番号が同じ原子に対応することを前提とし、複数ステップにわたる非折り返し軌跡を自動復元するものではありません。解析結果を利用する際は、対象ファイルとセル条件に適した処理であることを確認してください。

API と使用例は [ドキュメント](https://ohara-lab-su.github.io/vasp_util/) を参照してください。
