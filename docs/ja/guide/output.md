# 出力ファイルと解析

RMC_POT はフィッティング状況、計算履歴、原子配置、部分二体分布関数などを出力します。出力ファイルの種類は設定によって変わります。

| ファイル | 主な内容 | 対応するモジュール |
| --- | --- | --- |
| `.fit` | 実験値と計算値の比較 | `rmc_pot_fit` |
| `.hst` | 試行・受理の履歴、適合度の推移など | `rmc_pot_hst` |
| `.ppcf` | Partial Pair Correlation Function | `rmc_pot_ppcf` |
| `.cfg` | 原子配置 | `rmc_pot` / `util` 関連 |
| ログ | 計算過程の記録 | `rmc_pot_log` |

`.fit` を解釈する際は、対象データが $S(Q)$、$F(Q)$、$I(Q)$ などのどれかを確認してください。`.hst` の値を比較する際は、フィッティング対象と制約の組み合わせにも注意が必要です。

各ファイルの列・ヘッダ・読み方は [出力ファイル詳説](../reference/rmcpot_output_explained.md) を参照してください。

*参照：RMC_POT user guide 2023.1, II.B.*
