# Running distribited-points Molecular Dynamics

In this tutorial, dpMD is applied to [Lysozyme](https://www.rcsb.org/structure/3LZT), a classical example.
dpMD was implemented to extract the best of two worlds: [CHARMM](https://www.charmm.org/) is used for normal mode calculations and file processing, while [NAMD](http://www.ks.uiuc.edu/Research/namd/) is used as MD engine. Therefore, **both programs must be installed and paths must be updated in all bash scripts used in this tutorial**.

All necessary [inputs](https://github.com/antonielgomes/dpMD/tree/main/tutorial/inputs) and [scripts](https://github.com/antonielgomes/dpMD/tree/main/tutorial/scripts) files can be downloaded for performing dpMD locally.

### System files
Before performing dpMD, the following input files for CHARMM and NAMD are required:
- NAMD equilibrated files:
  - Coordinates: `step6.coor` and `step6.pdb` (the last one can be generated with [CHARMM](https://www.charmm.org/) or [VMD](https://www.ks.uiuc.edu/Research/vmd/))
  - Velocities: `step6.vel`
  - Cell dimensions: `step6.xsc`
  - system:
- CHARMM parameter files:
  - Paramater files: `step1.psf` for the protein and `step3.psf` for the system
  - Stream file: `step3.str`
  - Crystal images: `crystal_image.str`
 - Topology files:
  -  The `toppar.str` stream file reads all topology files inside the [toppar](https://github.com/antonielgomes/dpMD/tree/main/tutorial/toppar/) directory.

**NOTE:** All these files can be generate using the [CHARMM-GUI](https://www.charmm-gui.org/) server.

### Normal mode calculations
As dpMD uses normal modes (NMs) to obtain large conformational exploration, they must be calculated and provided as `mass-weighted` coordinate files. Although NMs can be calculated by several tools, this tutorial uses [CHARMM](https://www.charmm.org/), which minimizes the equilibrated protein in vacuum and then calculates NMs. These files are already available inside the [modes](https://github.com/antonielgomes/dpMD/tree/main/tutorial/modes) directory.
The minimized structure are available in crd and pdb files, filling the b-factor column with NM fluctuations in angstrom (`minimized-angstrom`), as a magnitude vector (`minimized-b-factor`) and as b-factor (`minimized-vector-magnitude`). The `modes.mod` contains all calculated NMs.

This protocol provides [scripts](https://github.com/antonielgomes/dpMD/tree/main/tutorial/scripts) for performing NM calculations.
The first 194 low-frequeny NMs can be by running the following command:
```
charmm -i scripts/normal-modes.inp
```
Following, NMs can be written as coordinates vectors or trajectories. Here, only the first 14 low-frequency NMs will be generated:
```
charmm -i scripts/normal-modes-dcd-crd.inp nmodes=14
```
### Normal mode combinations
To obtain uniformly combined set of NM vectors, the input files `input-modes.txt` - containing the uniformly distributed set of vectors obtained from [PDIM](https://github.com/antonielgomes/dpMD/tree/main/PDIM) - and `list-modes.txt` - containing the NM numbers will be provided. Both are available into the [scripts](https://github.com/antonielgomes/dpMD/tree/main/tutorial/scripts) directory.
In this tutorial, six combinations (`ncomb`, number of vectors) will be generated, while it will be read only the first 14 low-frequency NMs (`nmodes`).
```
charmm -i scripts/normal-mode-combination.inp ncomb=6 nmodes=14 inputfile=./inputs/input-modes.txt listmodes=./inputs/list-modes.txt 
```
**NOTE:** Each column weights a NM. Certify that the number of modes in `list-modes.txt` (two modes, 7 and 8) corresponds to the number of dimensions (columns) in the `input-modes.txt` file (two columns, one for modes 7 and another for 8).

### dpMD: first stage
##### Generating structures along combined normal modes with VMOD
In this step, the vacuum minimized structure will be displaced along all uniformly combined NM vectors using the `vmod.inp` script, located into the [scripts](https://github.com/antonielgomes/dpMD/tree/main/tutorial/scripts) directory. This step can be done automatically by running `vmod.sh` script in bash:
```
bash scripts/vmod.sh
```
The `vmod` directory will be generated, containing directories for each combined NM vector (mode-**$(mode number)**). For each one, vaccum minimized structures (conformation_**$(step)**.crd) will be generated with displacements from 0 to 3 Å in a step of 0.1 Å along the combined vector.

### dpMD: second stage
##### Targeting the equilibrated system towards every VMOD structure
In this step, all conformations gnerated along combined vectors will be generated under explicit solver from the equilibrated system with [Targeted Molecular Dynamics (TMD)](https://doi.org/10.1080/08927029308022170) simulations.
First, generata all conformations in the PDB format, c:
```
charmm -i scripts/dpmd-target.inp ncomb=6
```
A `dpMD directory` will be created, containing corresponding directory for each combined vector. Inside, all conformations will be found in the PDB format. Following, the `dpmd-tmd.inp` script will perform [TMD](https://doi.org/10.1080/08927029308022170). This step can be done automatically by running `dpmd-tmd.sh` script in bash:
```
bash scripts/dpmd-tmd.sh
```
For each combined vector directory inside the `dpMD directory`, a `tmd directory` will contain all solvated structures.
Now, each conformation will be equilibrated under position restraints for solvent accommodation. Firstly, generate all conformations in the PDB format for positional restraints:
```
charmm -i scripts/dpmd-restraints.inp ncomb=6
```
Then, equilibrate every solvated conformation running the `dpmd-equi.inp` script. This step can be done automatically by running `dpmd-equil.sh` script in bash:
```
bash scripts/dpmd-equil.sh
```
For each combined vector directory inside the `dpMD directory`, a `equil directory` will contain all equilibrated systems.

### dpMD: third stage
##### Exploring the conformational space with unrestrained MD simulations
As a final step, all generated conformations will be subsequently submitted to standard MD for efficient protein conformational sampling, running the `dpmd-free-md.inp` script. This step can be done automatically by running `dpmd-free-md.sh` script in bash:
```
bash scripts/dpmd-free-md.sh
```
For each combined vector directory inside the `dpMD directory`, a `free-md directory` will contain trajectories of all conformations after standard MD. These data can be further analyzed to extract valuable structural, dynamicas and functional aspects of a given protein.

### Bonus: **Molecular Dynamicas with excited Nornal Modes (MDeNM) with NAMD**

```
scripts/mdenm-namd-exc.sh
```

```
scripts/mdenm-namd-md.sh
```

### Contact
Questions or suggestions should be addressed to antonielaugusto@gmail.com
