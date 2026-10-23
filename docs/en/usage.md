# Usage Guide: Python API examples based on the implementation

These examples reproduce the code from the Japanese manual. They have not been tested against a live VASP calculation. Input files, element names, site numbers, and cutoffs must be adapted to the target system.

## 1. Reading a POSCAR structure

VaspPoscar reads lattice vectors, element labels, site indices, and atomic coordinates. The individual-atom accessors use 1-based atom numbering, while NumPy arrays use Python’s 0-based indexing. Cartesian input coordinates are converted internally to fractional (Direct) coordinates. Lattice vectors returned by get_lattice_vectors() include the POSCAR scaling factor; the parser supports positive scaling, negative target-volume scaling, and three-component scaling.

```python
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    print("atoms:", poscar.get_num_atoms())
    print("elements:", poscar.get_elements())
    print("atom species:", poscar.get_atom_indices())
    print("lattice (Å):\n", poscar.get_lattice_vectors())
    print("scale specification:", poscar.get_scale())
    print("fractional coordinates:\n", poscar.get_coords_direct())
    print("first atom (Å):", poscar.get_cartesian_position(1))


if __name__ == "__main__":
    main()
```

### Mapping element-local and global atom indices

Use get_global_index(element, site) to convert a 1-based element-local site index into the global 1-based atom index. The inverse accessors recover the element and element-local index. The chosen element must be present in the structure.

```python
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"
ELEMENT: str = "Li"
LOCAL_SITE: int = 1


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    global_index: int = poscar.get_global_index(ELEMENT, LOCAL_SITE)
    print("global index:", global_index)
    print("element:", poscar.get_element_by_global_index(global_index))
    print("local index:", poscar.get_local_index_by_global_index(global_index))
    print("all global indices:", poscar.get_element_site_indices(ELEMENT))


if __name__ == "__main__":
    main()
```

### Coordinate conversion and periodic boundary conditions (PBC)

Convert Direct coordinates and Cartesian coordinates using the lattice matrix. The shortest periodic displacement is calculated in fractional coordinates and converted back to Cartesian coordinates before evaluating its Euclidean norm in ångströms.

```python
import numpy as np
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"
INDEX_A: int = 1
INDEX_B: int = 2


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    a = poscar.get_direct_position(INDEX_A)
    b = poscar.get_direct_position(INDEX_B)
    displacement_direct = poscar.get_shortest_pbc_direct_vector(a, b)
    displacement_cartesian = poscar.conv_direct_to_cartesian(displacement_direct)
    print("minimum-image displacement (Å):", displacement_cartesian)
    print("distance (Å):", float(np.linalg.norm(displacement_cartesian)))
    print("back to Direct:", poscar.conv_cartesian_to_direct(displacement_cartesian))


if __name__ == "__main__":
    main()
```

## 2. Neighbor search and coordination environments

VaspPoscarAnalyzer combines structural data with interatomic-distance and nearest-neighbor routines. The examples apply periodic boundary conditions and optionally filter neighbors by chemical element. Neighbor ordering and return shapes should be checked against the current API signatures.

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

POSCAR_FILE: str = "POSCAR"
CENTER: int = 1
NEIGHBOR_COUNT: int = 4


def main() -> None:
    analyzer = VaspPoscarAnalyzer(VaspPoscar(POSCAR_FILE))
    distance = analyzer.get_interatomic_distance(1, 2, pbc=True)
    vector, vector_length = analyzer.get_distance_vector(1, 2, pbc=True)
    print("interatomic distance (Å):", float(distance))
    print("vector (Å):", vector, "norm (Å):", vector_length)
    neighbors = analyzer.get_neighbors(CENTER, NEIGHBOR_COUNT, target_elements=["O", "S"])
    for neighbor in neighbors:
        print(neighbor)


if __name__ == "__main__":
    main()
```

### Filtering nearest neighbors by element

Restrict neighbor searches using target_elements and inspect the returned neighbor records. Atom identifiers in these APIs are 1-based unless the implementation explicitly documents otherwise.

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

POSCAR_FILE: str = "POSCAR"
CENTER_ELEMENT: str = "P"
CENTER_LOCAL_SITE: int = 1
NEIGHBOR_ELEMENT: str = "O"
MAX_NEIGHBORS: int = 4


def main() -> None:
    analyzer = VaspPoscarAnalyzer(VaspPoscar(POSCAR_FILE))
    neighbors = analyzer.get_nearest_neighbors(
        center_element=CENTER_ELEMENT,
        center_local_site_index=CENTER_LOCAL_SITE,
        max_neighbors=MAX_NEIGHBORS,
        neighbor_element=NEIGHBOR_ELEMENT,
        pbc=True,
    )
    for element, site, global_index, distance, displacement in neighbors:
        print(element, site, global_index, distance, displacement)


if __name__ == "__main__":
    main()
```

## 3. Comparing atomic displacements between structures

Compare corresponding atoms in two POSCAR structures to analyze displacement vectors and jump events. Meaningful comparisons require compatible atom counts and ordering. Apply PBC when displacements may cross a cell boundary.

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

BEFORE_FILE: str = "POSCAR_before"
AFTER_FILE: str = "POSCAR_after"
ELEMENT: str = "Li"
THRESHOLD_ANGSTROM: float = 2.0


def main() -> None:
    before = VaspPoscarAnalyzer(VaspPoscar(BEFORE_FILE))
    after = VaspPoscarAnalyzer(VaspPoscar(AFTER_FILE))
    indices = before.poscar.get_element_site_indices(ELEMENT)
    for global_index in indices:
        distance = before.get_jump_distance(after, global_index, pbc=True)
        jumped = before.is_jump(after, global_index, THRESHOLD_ANGSTROM, pbc=True)
        print(global_index, distance, jumped)


if __name__ == "__main__":
    main()
```

### Scanning MD trajectory files

The trajectory examples traverse a series of structures and summarize step-to-step motion. Verify file naming, frame ordering, and the coordinate convention before interpreting jumps or cumulative displacement.

```python
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

MD_DIRECTORY: str = "md_poscars"
FILE_TEMPLATE: str = "POSCAR_{}"
START_STEP: int = 0
END_STEP: int = 100
ELEMENT: str = "Li"
START_SITE: int = 1
END_SITE: int = 10
JUMP_THRESHOLD: float = 2.0


def main() -> None:
    VaspPoscarAnalyzer.scan_md_series_for_jumps(
        folder_path=MD_DIRECTORY,
        file_template=FILE_TEMPLATE,
        step_min=START_STEP,
        step_max=END_STEP,
        element=ELEMENT,
        start_site=START_SITE,
        end_site=END_SITE,
        threshold=JUMP_THRESHOLD,
        show_non_jumps=False,
    )


if __name__ == "__main__":
    main()
```

## 4. Editing INCAR

VaspIncar reads and edits INCAR tags. Writing an edited INCAR changes an input file; preserve the original if reproducibility or comparison matters.

```python
from vasp_util.vasp_incar import VaspIncar

INCAR_FILE: str = "INCAR"


def main() -> None:
    incar = VaspIncar(incar_name=INCAR_FILE, auto_write=False)
    incar.init()
    print("old ENCUT:", incar.get("ENCUT", default=None))
    incar.set("ENCUT", 520, auto_write=False)
    incar.set("EDIFF", 1e-6, auto_write=False)
    incar.set_tag("ISMEAR", 0, auto_write=False)
    incar.set_tag("SIGMA", 0.05, auto_write=False)
    incar.write()
    print("updated INCAR:", incar.export_dict())


if __name__ == "__main__":
    main()
```

### Comparing two INCAR files

Compare tag sets and values from two INCAR files to identify changes in calculation settings. Compare both absent tags and explicitly assigned values.

```python
from vasp_util.vasp_incar import VaspIncar

FIRST_INCAR: str = "INCAR.initial"
SECOND_INCAR: str = "INCAR.relaxed"


def main() -> None:
    first = VaspIncar(incar_name=FIRST_INCAR, auto_write=False)
    second = VaspIncar(incar_name=SECOND_INCAR, auto_write=False)
    first.init()
    second.init()
    differences = first.diff_with(second)
    for tag, values in differences.items():
        print(tag, values)


if __name__ == "__main__":
    main()
```

## 5. Creating and updating KPOINTS

VaspKpoints provides KPOINTS input generation and editing. Ensure the generated mesh and centering convention match the intended calculation.

```python
from vasp_util.vasp_kpoints import VaspKpoints

KPOINTS_FILE: str = "KPOINTS"


def main() -> None:
    kpoints = VaspKpoints(kpoints_name=KPOINTS_FILE, auto_write=False)
    kpoints.set_mode("Gamma", auto_write=False)
    kpoints.set_grid(2, 2, 2, auto_write=False)
    kpoints.set_shift(0, 0, 0, auto_write=False)
    kpoints.set_comment("Gamma-centered mesh", auto_write=False)
    kpoints.write()
    print(kpoints.export_dict())


if __name__ == "__main__":
    main()
```

## 6. Generating POTCAR

VaspPotcar assembles element-dependent PAW potential data. The correct potential library and element ordering are essential; generation requires locally available VASP potential files.

```python
from vasp_util.vasp_potcar import VaspPotcarBuilder

POTENTIAL_DIRECTORY: str = "~/potpaw_PBE.64"
ELEMENTS: list[str] = ["Li", "P", "S"]
OUTPUT_FILE: str = "POTCAR"


def main() -> None:
    builder = VaspPotcarBuilder(base_dir=POTENTIAL_DIRECTORY)
    for element in ELEMENTS:
        print(element, builder.choose_potential(element))
    success = builder.build(elements=ELEMENTS, poscar_name=OUTPUT_FILE)
    print("POTCAR written:", success)


if __name__ == "__main__":
    main()
```

## 7. Analyzing OUTCAR SCF and ionic-relaxation histories

VaspOutcar parses the electronic and ionic output history, including free energy, energy without entropy, extrapolated sigma→0 energy, atomic positions, and forces. The implementation expects a finished OUTCAR and may raise an exception for incomplete output.

```python
import numpy as np
from vasp_util.vasp_outcar import VaspOutcar

OUTCAR_FILE: str = "OUTCAR"


def main() -> None:
    outcar = VaspOutcar(OUTCAR_FILE)
    print("finalized:", outcar.is_finalized())
    print("ionic steps:", outcar.get_ionstep_count())
    for mode in ("toten", "e0", "sigma0"):
        energies = outcar.get_energy_ionstep(mode=mode)
        print(mode, energies)
    matrix = outcar.get_energy_matrix(mode="e0")
    flat = outcar.get_energy_flat(mode="e0")
    print("SCF matrix shape:", matrix.shape)
    print("valid SCF energies:", flat.size)
    print("finite energy values:", int(np.isfinite(matrix).sum()))


if __name__ == "__main__":
    main()
```

### Atomic positions, forces, and magnetic moments

The OUTCAR parser retains per-ion positions and forces and resolves magnetic moments into s, p, d, and total contributions when present. Its ionic-step indexing follows the implementation’s NSW+1 convention; absent blocks should not be interpreted as physical zero without checking the parser.

```python
import numpy as np
from vasp_util.vasp_outcar import VaspOutcar

OUTCAR_FILE: str = "OUTCAR"


def main() -> None:
    outcar = VaspOutcar(OUTCAR_FILE)
    last_step: int = outcar.get_ionstep_count() - 1
    positions = outcar.get_positions(last_step)
    forces = outcar.get_forces(last_step)
    magnetic_moments = outcar.get_magmom_atom(last_step)
    print("positions shape:", positions.shape)
    print("forces shape:", forces.shape)
    print("max force (eV/Å):", float(np.nanmax(np.linalg.norm(forces, axis=1))))
    print("magmom (s,p,d,total) shape:", magnetic_moments.shape)
    print("total magnetization:", outcar.get_magmom_total(last_step))


if __name__ == "__main__":
    main()
```

## 8. Managing input and execution with Vasp

Vasp coordinates input preparation, execution, and postprocessing. The examples demonstrate explicit configuration; execution requires a correctly installed VASP binary and suitable runtime environment.

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

VASP_BINARY: str = "vasp_gam"


def main() -> None:
    config = Config()
    config.dft_bin = VASP_BINARY
    config.run_mode = "local"
    vasp = Vasp(config=config, make_default_input=False)
    vasp.set_tag("EDIFF", 1e-6)
    vasp.set_tag("NELM", 100)
    print(vasp.get_tag("EDIFF"))
    print(vasp.export_incar_dict())
    print(vasp.export_kpoints_dict())
    vasp.preprocess()
    succeeded = vasp.run(mode="local")
    print("VASP succeeded:", succeeded)


if __name__ == "__main__":
    main()
```

### MPI execution

Configure the MPI executable and process count for the local machine or scheduler. The example illustrates invocation and does not substitute for the site-specific batch system.

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

VASP_BINARY: str = "vasp_std"
PROCESS_COUNT: int = 8


def main() -> None:
    config = Config()
    vasp = Vasp(config=config, dft_bin=VASP_BINARY, make_default_input=False)
    vasp.set_mpi(mpi_cmd="mpirun", mpi_flag="-np", num_procs=PROCESS_COUNT)
    vasp.preprocess()
    result = vasp.run(mode="mpi")
    print(result)


if __name__ == "__main__":
    main()
```

## 9. Structure interchange with RMC

The conversion utilities connect VASP structures and RMC-related formats, including POSCAR-to-CFG and XDATCAR-to-POSCAR conversion. Preserve atom ordering, lattice information, and frame selection when exchanging structures.

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

CFG_NAME: str = "relaxed"


def main() -> None:
    config = Config()
    vasp = Vasp(config=config, make_default_input=False)
    vasp.contcar2cfg(cfg_name=CFG_NAME)


if __name__ == "__main__":
    main()
```

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

LOG_DIRECTORY: str = "vasp_log"
CFG_NAME: str = "relaxed"


def main() -> None:
    vasp = Vasp(config=Config(), make_default_input=False)
    success = vasp.postprocess(log_dir=LOG_DIRECTORY, cfg_name=CFG_NAME)
    print("postprocess:", success)


if __name__ == "__main__":
    main()
```

## 10. Configuration and side effects

Config(yaml_path=...) populates instance attributes, whereas Config.load_yaml(...) updates class-level attributes and therefore has broader effects. Explicit non-None Vasp arguments override the corresponding configuration settings. Distinguish read-only parsing from write operations such as set_tag, write, postprocess, and POTCAR generation; back up input files before modifying them.

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

CONFIG_FILE: str = "config.yml"


def main() -> None:
    config = Config(yaml_path=CONFIG_FILE)
    vasp = Vasp(config=config, make_default_input=False)
    print("run mode:", config.run_mode)
    print("binary:", vasp.dft_bin)


if __name__ == "__main__":
    main()
```

## 11. Using the API reference

The generated API reference is rebuilt from the current src/vasp_util tree at every documentation build. Consult it for actual method signatures and source docstrings. When an example and an installed package differ, the installed version’s implementation takes precedence.

## Complete method and function inventory

The generated API reference covers all discovered modules, classes, methods, and top-level functions, including APIs not demonstrated in this guide.

## API maintenance and regeneration

Run docs/build.sh to regenerate the API pages and build the Sphinx site. Hand-written manuals are not overwritten by the API generator.

