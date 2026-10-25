# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fvasp_util-181717?logo=github)](https://github.com/ohara-lab-su/vasp_util/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/vasp_util/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/)

VASP の入力・出力、原子構造の解析、計算実行と結果整理を、研究プログラムから扱うための Python
ライブラリです。[RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/) で使っていた処理を 0.7.10 から分離しました。

構造操作や VASP 入出力には [ASE](https://ase-lib.org/) と [pymatgen](https://pymatgen.org/) という充実したライブラリがあります。
`vasp_util` はそれらを置き換えるためのものではありません。既存の機能は利用しながら、計算前後のファイル操作、サイト番号による構造参照、近接原子・原子移動の調査、計算結果の整理、RMCProfile
とのデータ交換など、実際の作業で繰り返し必要になった処理をまとめています。単独の操作は既存ライブラリで実現できても、研究で使う入出力・判断・実行手順を一つの
API にまとめる意味があります。

## 開発の経緯

2010年頃から2015年頃にかけて、VASP を含む結晶構造関連のツール [sae](https://github.com/ohara-lab-su/sae)
を開発していました。機能の追加とともに巨大化し、設計にも問題を抱えたため、その後は利用を休止しました。一方で ASE と pymatgen
は発展し、sae をそのまま作り直す理由も薄れました。

それでも VASP の構造や計算結果を扱うプログラムを書くたび、特定の解析やファイル処理が必要になり、似たコードが複数のプロジェクトに増えていきました。そこで
RMC-DFT 内で実際に使っている処理を小さなクラスと関数に整理し、独立して利用できるようにしたものが `vasp_util` です。

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

## 利用上の注意

POSCAR/CFG 変換の一部には入力行の配置や Direct 座標を前提とする処理があります。また、MD
ステップ間の変位は同じサイト番号が同じ原子に対応することを前提とし、複数ステップにわたる非折り返し軌跡を自動復元するものではありません。解析結果を利用する際は、対象ファイルとセル条件に適した処理であることを確認してください。

API と使用例は [ドキュメント](https://ohara-lab-su.github.io/vasp_util/) を参照してください。
