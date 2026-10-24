# RMC Method and RMC_POT

Reverse Monte Carlo (RMC) constructs three-dimensional atomic configurations consistent with data obtained from scattering experiments and other measurements. It evaluates the difference between scattering quantities calculated from the atomic configuration and measured values, and repeatedly proposes changes to atomic positions.

RMC_POT handles neutron diffraction $S(Q)$, X-ray diffraction $F(Q)$ and $I(Q)$, electron diffraction $F(g)$, and EXAFS $E(k)$, among other quantities. Partial pair distribution functions $g_{ij}(r)$ are important structural quantities obtained from the atomic configuration.

Scattering data alone may not uniquely determine the local structure. Therefore, interatomic distances, coordination numbers, bond angles, FNC, and other structural constraints can be combined as necessary.

To start an RMC_POT calculation, prepare an initial atomic configuration, calculation settings, and the experimental data to be used. The roles of the files are summarized under [Input Files](input.md).

For the theory, see [Introduction to the RMC Method](../reference/rmc_theory_explained.md).

*Reference: RMC_POT user guide 2023.1, I.A–I.C, I.K–I.Q.*
