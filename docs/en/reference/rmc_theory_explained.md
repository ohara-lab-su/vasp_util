# What Is the RMC Method?

Reverse Monte Carlo (RMC) is a method for finding atomic configurations consistent with data obtained from scattering experiments and other measurements. It iteratively proposes changes to atomic positions and accepts or rejects them.

## Agreement with Experimental Data

RMC evaluates the difference between scattering functions calculated from an atomic configuration and experimental data. For example, if the standard deviation at measurement point $i$ is $\sigma_i$, a measure of agreement can be written as

```{math}
\chi^2 = \sum_i \frac{\left[S_{\mathrm{calc}}(Q_i)-S_{\mathrm{exp}}(Q_i)\right]^2}{\sigma_i^2}
```

Here, $S_{\mathrm{calc}}$ is the structure factor calculated from the atomic configuration, and $S_{\mathrm{exp}}$ is the measured value. When multiple datasets or structural constraints are used, their contributions also enter the evaluation. The precise objective function and coefficient definitions depend on the RMC_POT settings and version.

## Acceptance and Rejection of Atomic Moves

After a trial modification of the atomic configuration, calculate the change in agreement:

```{math}
\Delta\chi^2 = \chi^2_{\mathrm{new}}-\chi^2_{\mathrm{old}}
```

The acceptance rule given in the RMC_POT user guide is

```{math}
P_{\mathrm{accept}} = \min\left[1,\exp(-\Delta\chi^2)\right]
```

Under this rule, moves that improve agreement ($\Delta\chi^2\leq0$) are accepted, while moves that worsen agreement can still be accepted with a finite probability.

## Role of Standard Deviations

The standard deviation $\sigma_i$ at each measurement point determines the weight assigned to the residual between experimental and calculated values. For the same residual, a point with smaller $\sigma_i$ makes a larger contribution to $\chi^2$.

## References

- Orsolya Gereben, *RMC_POT user guide*. Consult the official manual for the definitions of acceptance probability and $\chi^2$, as well as the specification of standard deviations for each dataset.
- https://www.szfki.hu/~nphys/rmc++/RMC_POT_user_guide.pdf
