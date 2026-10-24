# Output Files and Analysis

RMC_POT outputs fitting results, calculation histories, atomic configurations, partial pair distribution functions, and other data. The files produced depend on the settings.

| File | Main contents | Corresponding module |
| --- | --- | --- |
| `.fit` | Comparison between experimental and calculated values | `rmc_pot_fit` |
| `.hst` | History of attempted and accepted moves, evolution of goodness of fit, etc. | `rmc_pot_hst` |
| `.ppcf` | Partial Pair Correlation Function | `rmc_pot_ppcf` |
| `.cfg` | Atomic configuration | `rmc_pot` / `util` related modules |
| Log files | Records of the calculation process | `rmc_pot_log` |

When interpreting a `.fit` file, check whether the dataset represents $S(Q)$, $F(Q)$, $I(Q)$, or another quantity. When comparing `.hst` values, also consider the combination of fitted datasets and constraints.

For file columns, headers, and interpretation, see the [detailed output-file reference](../reference/rmcpot_output_explained.md).

*Reference: RMC_POT user guide 2023.1, II.B.*
