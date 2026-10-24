# RMCPOT Input File Reference

# cfg file
The `cfg` file specifies the atomic configuration. For a detailed explanation, see [the cfg file reference](rmcpot_cfg_explained.md).

# sq file
```{code}
2832
Dataset measured at BL04B2
0.263585 2.81259 0.308196 0.164155 0.329761 0.0218585 0.0878205 0.0882089 
0.281276 2.3427 0.308147 0.16408 0.329845 0.0218421 0.087817 0.0882679 
0.298966 1.91993 0.308095 0.164001 0.329935 0.0218247 0.0878133 0.0883307 
0.316656 1.57281 0.30804 0.163917 0.33003 0.0218063 0.0878092 0.0883972 
0.334346 1.29722 0.307982 0.163829 0.33013 0.0217868 0.0878049 0.0884676 
0.352037 1.06632 0.307921 0.163735 0.330235 0.0217663 0.0878003 0.0885417 
0.369727 0.88715 0.307857 0.163637 0.330346 0.0217447 0.0877954 0.0886195
   :        : 
```
The first column contains q [Å⁻¹]; the second column contains the experimentally measured S(q); columns three onward contain weighting factors.

```math
coeff_{ii} = \frac{c_i^2 \overline{b_i}^2}{\sum_{i} \sum_{j} c_i c_j \overline{b_i b_j}} \qquad , \qquad 
coeff_{ij} = \frac{c_i c_j \overline{b_i b_j}}{\sum_{i} \sum_{j} c_i c_j \overline{b_i b_j}}
```
See equation E3 in the [official RMC_POT user guide](https://www.szfki.hu/~nphys/rmc++/RMC_POT_user_guide.pdf).
These coefficients are used to construct the total S(q) from the Faber–Ziman partial structure factors S_ij(q).
T. E. Faber and J. M. Ziman (1964), DOI: https://doi.org/10.1080/14786436508211931

When total-scattering measurements from SPring-8 BL04B2 are analyzed using the IGOR-macro analysis software, the weighting factors are also provided as output. If these data are available, there is no need to calculate the factors separately.
http://rud.spring8.or.jp/member/0020758/distrbution.html

# dat file

```{code}
comment
0.0842566414       ! number density
1 1 1 1 1 1 ! cut offs
0.01 0.01 0.01   ! maximum moves
0.025        ! r spacing
.false.      ! whether to use moveout option
0            ! number of configurration to collect
5000         ! step for printing
0 0          ! time limit, step for saving
0 0 1 0      ! g(r), neutron, x-ray, EXAFS
S_q_fqd_0.3_0.03_40.sq
1 991
1.0
5E-3
.false.
.true.
.false.
.false.
0         ! number of cos. distr of bond angles constraint, dcos_theta (spacing in cos(theta) space
0  ! no of coord. constr.
0         ! no of av. coord. contsr.
0         ! potential
0         ! FNC switch
0         ! initial bin shift;
1         ! xmax used in the run.
1         ! number of atoms moved in a single move
200       ! size of the history buffer
10        ! number of display update beteen each history buffering
0         ! indicator of custom move
0         ! whether to load the histgram form file, if posible [0:no 1:yes]
5        ! maximum number of atoms in a gridcell
0 0       ! frction of swaps, ntypes*(ntypes-1)/2 0 not allowded or 1 allowed for the possible mixed part
4         ! total number of threads to use
```
The entries below explain each line in order. Line numbers are assigned solely for reference to the example above.

**1) `comment`**

A comment line containing a short description of the input or the sample name (optional).

**2) `0.0842566414       ! number density`**

Number density of the system, in atoms/Å³. It must be consistent with the atom count and simulation-box volume in the `cfg` file (the value is specified in two places).

**3) `1 1 1 1 1 1 ! cut offs`**

Cutoff distances for atomic species or cutoff-related settings. The example has six entries; the required count depends on the number of species and the internal format. Many implementations use minimum allowed pair separations. For three species the expected pair order is 11, 12, 13, 22, 23, 33; for n species, 11, 12, …, 1n, 22, 23, …, 2n, …, nn. Confirm the exact semantics for the version in use.

**4) `0.01 0.01 0.01   ! maximum moves`**

Maximum displacement amplitude per atomic move, in Å. Multiple entries may correspond to species or move types. This parameter influences acceptance and exploration, but no universal target acceptance rate is assumed: it also depends on constraints and the current structure.

**5) `0.025        ! r spacing`**

Bin width for the radial distribution function g(r), in Å. Smaller spacing increases resolution and computational cost.

**6) `.false.      ! whether to use moveout option`**

Boolean switch (`.true.`/`.false.`) for the moveout option, which is intended to resolve pairs violating minimum-distance constraints. Exact behavior is implementation-dependent; consult the manual.

**7) `0            ! number of configuration to collect`**

Number of configurations to collect; set to zero here. Verify separately how intermediate configuration saving is controlled.

**8) `5000         ! step for printing`**

Number of steps between progress or log outputs.

**9) `0 0          ! time limit, step for saving`**

First value: time limit (minutes). Second: number of steps between saves. Zero often means disabled or default behavior; confirm in the implementation.

**10) `0 0 1 0      ! g(r), neutron, x-ray, EXAFS`**

Flags for g(r), neutron scattering, X-ray scattering and EXAFS, in that order according to the example comment. Here only X-ray is enabled. Check the manual for version-specific meaning and ordering.

**11) `S_q_fqd_0.3_0.03_40.sq`**

Path or filename of the S(q) dataset described above. Relative or absolute paths may be used as supported by the program.

**12) `1 991`**

Dataset read-range parameters, potentially first/last row or minimum/maximum q indices. The precise meaning depends on the RMC_POT version and file format; consult the manual.

**13) `1.0`**

The exact meaning of this value cannot be established from the example alone. Do not assign a parameter name without checking the input specification.

**14) `5E-3`**

Standard deviation assigned to this dataset. It controls weighting of the discrepancy between measured and calculated values in the objective function; it is neither a convergence tolerance nor a temperature. Check whether further parameters or metric-selection settings follow in the version used.

**15) `.false.`**

Dataset-associated logical setting. The name and meaning of this flag cannot be uniquely established from the example; do not speculate about background correction or smoothing.

**16) `.true.`**

Dataset-associated logical setting. The name and meaning of this flag cannot be uniquely established from the example; check the input specification.

**17) `.false.`**

Dataset-associated logical setting. The name and meaning of this flag cannot be uniquely established from the example; check the input specification.

**18) `.false.`**

Dataset-associated logical setting. The name and meaning of this flag cannot be uniquely established from the example; check the input specification.

**19) `0         ! number of cos. distr of bond angles constraint, dcos_theta`**

Number of bond-angle-distribution constraints. Zero disables them. The comment also refers to spacing dcos_theta in cos(theta) space.

**20) `0  ! no of coord. constr.`**

Number of coordination-number constraints. Zero disables them.

**21) `0         ! no of av. coord. contsr.`**

Number of average-coordination constraints; zero disables them.

**22) `0         ! potential`**

Potential-related flag or selector. Zero commonly indicates no potential, but the exact meaning must be checked for the implementation.

**23) `0         ! FNC switch`**

FNC (e.g., Fixed Neighbour Constraints) switch; zero indicates off. Consult the manual for implementation-specific behavior.

**24) `0         ! initial bin shift;`**

Initial histogram/bin offset for g(r) or related quantities. Zero specifies no shift.

**25) `1         ! xmax used in the run.`**

Value controlling the maximum r (xmax), potentially a scale or flag. The meaning of 1 is implementation-dependent.

**26) `1         ! number of atoms moved in a single move`**

Number of atoms moved simultaneously in one move; one atom here. Do not infer support for multi-atom moves: ordinary atomic RMC in RMC_POT 2023.1 free-format input assumes single-atom moves.

**27) `200       ! size of the history buffer`**

Size of the history buffer for move information, acceptance statistics or other history used in analysis.

**28) `10        ! number of display update beteen each history buffering`**

Number of display updates between history-buffer updates; controls progress-display frequency.

**29) `0         ! indicator of custom move`**

Indicator for user-defined/custom moves; zero disables them.

**30) `0         ! whether to load the histgram form file, if posible [0:no 1:yes]`**

Whether to load an existing histogram from a file: 0 = no, 1 = yes.

**31) `5        ! maximum number of atoms in a gridcell`**

Maximum number of atoms in each spatial grid cell; relevant to neighbor searches and neighbor-list construction.

**32) `0 0       ! frction of swaps, ntypes*(ntypes-1)/2`**

Swap settings. The first value controls the swap fraction or related parameter; the second indicates whether swaps are allowed (0 = disallowed, 1 = allowed). The comment associates ntypes × (ntypes − 1) / 2 with possible inter-species pairs.

**33) `4         ! total number of threads to use`**

Total number of threads. Select according to the hardware, and verify actual parallel execution against build settings and runtime environment.

---

## Additional notes and cautions

- The exact sequence and semantics of these fields may differ across RMC_POT/RMC++ versions and implementations. The descriptions above give typical roles and units; refer to the [official manual](https://www.szfki.hu/~nphys/rmc++/RMC_POT_user_guide.pdf) for the authoritative specification.
- The number of atomic species (`ntypes`) in the `cfg` file must match the number expected by type-dependent fields in the `dat` file, including cutoff and per-species parameter lists.
- After changing values, inspect logs, acceptance rates and histogram/bin settings. In particular, maximum displacement strongly affects acceptance.
- Incorrect calculation or ordering of the S(q) weighting coefficients can prevent accurate reproduction of S(q). Use the correct atomic fractions c_i and scattering lengths (or averaged scattering factors).
