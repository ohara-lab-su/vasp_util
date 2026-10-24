# RMC 法とは

Reverse Monte Carlo（RMC）法は、散乱実験などで得られたデータと整合する原子配置を、原子位置の試行変更と受理・棄却の反復によって探索する手法です。

## 実験データとの一致度

RMC では、原子配置から計算した散乱関数と実験データの差を評価します。例えば、測定点ごとの標準偏差を $\sigma_i$ とすると、一致度を表す量は次のように記述できます。

```{math}
\chi^2 = \sum_i \frac{\left[S_{\mathrm{calc}}(Q_i)-S_{\mathrm{exp}}(Q_i)\right]^2}{\sigma_i^2}
```

ここで $S_{\mathrm{calc}}$ は原子配置から計算した構造因子、$S_{\mathrm{exp}}$ は実験値です。複数のデータセットや構造制約を利用する場合は、それらの寄与も評価に関係します。実際の評価関数と係数の定義は RMC_POT の設定およびバージョンに依存します。

## 原子移動の受理・棄却

原子配置を試行的に変更し、その前後の一致度の差

```{math}
\Delta\chi^2 = \chi^2_{\mathrm{new}}-\chi^2_{\mathrm{old}}
```

を求めます。RMC_POT のユーザーガイドに示される受理則は、

```{math}
P_{\mathrm{accept}} = \min\left[1,\exp(-\Delta\chi^2)\right]
```

です。この式では、一致度が改善する変更（$\Delta\chi^2\leq0$）は受理され、悪化する変更も一定の確率で受理されます。


## 標準偏差の役割

測定点ごとの標準偏差 $\sigma_i$ は、実験データと計算値の残差に対する重みを定めます。同じ残差でも $\sigma_i$ が小さい測定点ほど、$\chi^2$ への寄与が大きくなります。

## 参考資料

- Orsolya Gereben, *RMC_POT user guide*：受理確率と $\chi^2$ の定義、およびデータセットごとの標準偏差の指定については公式マニュアルを参照してください。
- https://www.szfki.hu/~nphys/rmc++/RMC_POT_user_guide.pdf
