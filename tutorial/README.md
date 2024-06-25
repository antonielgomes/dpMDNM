# Running distributed points Molecular Dynamics with Normal Modes

This tutorial applies dpMDNM to [Lysozyme](https://www.rcsb.org/structure/3LZT), a classic example.
dpMDNM was implemented to extract the best of two worlds: [CHARMM](https://www.charmm.org/) is used for normal mode calculations and file processing, while [NAMD](http://www.ks.uiuc.edu/Research/namd/) is used as MD engine. **Both programs must be installed, and paths must be updated in all bash scripts used in this tutorial**. Additional program flags (number of processes, GPU usage, etc.) should also be specified.

All necessary [inputs](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/inputs) and [scripts](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/scripts) files can be downloaded for performing dpMDNM locally.

### System files
Before performing dpMDNM, the following input files for CHARMM and NAMD are required:
- NAMD equilibrated files:
  - Coordinates: `step6.coor` and `step6.pdb` (the last one can be generated with [CHARMM](https://www.charmm.org/) or [VMD](https://www.ks.uiuc.edu/Research/vmd/))
  - Velocities: `step6.vel`
  - Cell dimensions: `step6.xsc`
  - system:
- CHARMM parameter files:
  - Parameter files: `step1.psf` for the protein and `step3.psf` for the system
  - Stream file: `step3.str`
  - Crystal images: `crystal_image.str`
 - Topology files:
  -  The `toppar.str` stream file reads all topology files inside the [toppar](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/toppar/) directory.

**NOTE:** All these files can be generated using the [CHARMM-GUI](https://www.charmm-gui.org/) server.

### Normal mode calculations
As dpMDNM uses normal modes (NMs) to obtain large conformational exploration, they must be calculated and provided as `mass-weighted` coordinate files. Although NMs can be calculated by several tools, this tutorial uses [CHARMM](https://www.charmm.org/), which minimizes the equilibrated protein in vacuum and then calculates NMs. These files are already available inside the [modes](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/modes) directory.
The minimized structure is available in crd and pdb formats, filling the b-factor column with NM fluctuations in angstrom (`minimized-angstrom`), as a magnitude vector (`minimized-b-factor`), and as b-factor (`minimized-vector-magnitude`). The `modes.mod` contains all calculated NMs. They have the same XYZ coordinates.

This protocol provides [scripts](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/scripts) for performing NM calculations.
100 low-frequency NMs can be calculated by running the following command:
```
charmm -i scripts/normal-modes.inp nmodes=100
```
Following, NMs can be written as coordinate vectors or trajectories. Here, only the first 14 low-frequency NMs will be generated:
```
charmm -i scripts/normal-modes-dcd-crd.inp nmodes=14
```
### Normal mode combinations
To obtain a uniformly combined set of NM vectors, the input files `input-modes.txt` - containing the uniformly distributed set of vectors obtained from [PDIM](https://github.com/antonielgomes/dpMDNM/tree/main/PDIM) - and `list-modes.txt` - containing the NM numbers - should be provided. Both are available in the [scripts](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/scripts) directory.
In this tutorial, six combinations (`ncomb`, number of vectors) of two NMs will be generated, while it will be read only the first 14 low-frequency NMs (`nmodes`):
```
charmm -i scripts/normal-mode-combination.inp ncomb=6 nmodes=14 inputfile=./inputs/input-modes.txt listmodes=./inputs/list-modes.txt 
```
**NOTE:** Each row is a combination and each column is aNM weight. Certify that the number of modes in `list-modes.txt` (two modes, 7 and 8) corresponds to the number of dimensions (columns) in the `input-modes.txt` file (two columns, one for modes 7 and another for 8). Three columns per combination (row) should be provided for three modes.

### First stage: dpVAC
##### Generating structures along combined normal modes with VMOD
In this step, the vacuum minimized structure used in NM calculations will be displaced along all uniformly combined NM vectors using the `vmod.inp` script, located in the [scripts](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/scripts) directory. This step can be done automatically by running the `vmod.sh` script in bash:
```
bash scripts/vmod.sh
```
The `vmod` directory will be generated, containing directories for each combined NM vector (mode-**$(mode number)**). For each one, vacuum-minimized structures (conformation_**$(step)**.crd) will be generated with displacements from 0 to 3 Å in a step of 0.1 Å along the combined vector.

### Second stage: dpSOL
##### Targeting the equilibrated system towards every VMOD structure
All conformations will be generated under explicit solver starting from the equilibrated system using [TMD](https://doi.org/10.1080/08927029308022170). First, convert all conformations generated by VMOD to the pdb format:
```
charmm -i scripts/dpmdnm-target.inp ncomb=6
```
A `dpmdnm directory` will be created, containing a corresponding directory for each combined vector. Inside, all conformations will be found in the pdb format. Following, the `dpmdnm-tmd.inp` script will perform [TMD](https://doi.org/10.1080/08927029308022170). This step can be done automatically by running the `dpmdnm-tmd.sh` script in bash:
```
bash scripts/dpmdnm-tmd.sh
```
For each combined vector directory inside the `dpmdnm directory`, a `tmd directory` will contain all solvated structures.
Now, each conformation will be equilibrated under position restraints for solvent accommodation. Firstly, generate all conformations in the pdb format for positional restraints:
```
charmm -i scripts/dpmdnm-restraints.inp ncomb=6
```
Then, equilibrate every solvated conformation running the `dpmdnm-equi.inp` script. This step can be done automatically by running the `dpmdnm-equil.sh` script in bash:
```
bash scripts/dpmdnm-equil.sh
```
For each combined vector directory inside the `dpmdnm directory`, an `equil directory` will contain all equilibrated systems.

### Third stage: dpMDNM
##### Exploring the conformational space with unrestrained MD simulations
As a final step, all generated conformations will be subsequently submitted to standard MD for efficient protein conformational sampling, running the `dpmdnm-free-md.inp` script. This step can be done automatically by running the `dpmdnm-free-md.sh` script in bash:
```
bash scripts/dpmdnm-free-md.sh
```
For each combined vector directory inside the `dpmdnm directory`, a `free-md directory` will contain trajectories of all conformations after standard MD. These data can be further analyzed to extract valuable structural, dynamic, and functional aspects of a given protein.

### Bonus: Using uniformly combined vectors with Molecular Dynamics with excited Normal Modes

[MDeNM](https://doi.org/10.1021/acs.jctc.5b00003) is a `multi-replica` method to explore protein conformational changes through successive kinetic excitations along a diverse set of combined NM vectors using short standard MD simulations. Initially, MDeNM devised to run in CHARMM. Recently our team implemented this technique to work with elastic NMs or Principal Components within the R program, termed [MDexciteR](https://doi.org/10.1021/acs.jctc.2c00599), enabling MDeNM to run with several MD engines, such as [GROMACS](https://www.gromacs.org/), [AMBER](https://ambermd.org/), or [NAMD](http://www.ks.uiuc.edu/Research/namd/). We make efforts to spread MDeNM and facilitate its usage among researchers interested in performing efficient protein conformational explorations.
Further, the efficacy of MDeNM was improved by using uniformly combined NMs, implementing the same methodological procedure for running with [NAMD](http://www.ks.uiuc.edu/Research/namd/) through Python programming. All input files are located in the [MDeNM](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/mdenm) directory, which contains the following:
- MDeNM input parameters:
  - Temperature input, number of replicas, and output names are inside the `input-mdenm.txt` file.
  - Excitation vectors are generated by the `mdenm-combined-modes.inp` file.
  - Automated scripts for generatin excitation vectors (`mdenm-combined-modes.sh`), excitation steps (`mdenm-namd-exc.sh` ), and standard free-md calculations (`mdenm-namd-free-md.sh`).
- NAMD directory:
  - Python scripts `charmm_vector_namd.py` - for converting charmm coordinates to the namd format - and `namd_vectors_sum.py` - for generating the excited system inputs.
  - NAMD input scripts `namd-exc.inp` - for performing excitation steps - and `namd-free-md.inp` - for performing standard free-md of each excitation.

**NOTE:** it is necessary generating combined NM vectors, as explained in [normal-mode-combinations](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial#normal-mode-combinations).

In the first step, process files, and directories will be generated, including excitation vectors (`vectormodes.crd` files) for each combined NM automatically by running the `mdenm-combined-modes.sh` script in bash:
```
bash mdenm/mdenm-combined-modes.sh
```
The `excitations` directory will be generated inside the [MDeNM](https://github.com/antonielgomes/dpMDNM/tree/main/tutorial/mdenm) directory. A directory will be generated for each combined NM - or replica (in this case, directories from 1 to 6).
Then, perform the excitation step:
```
bash mdenm/mdenm-namd-exc.sh
```
It will generate 10 excitations for each combined NM.
Following, run the standard free-md step:
```
bash mdenm/mdenm-namd-free-md.sh
```
A `free-md` directory will be created for each combined NM, containing trajectories of all excitations after standard MD. These data can be further analyzed to extract valuable structural, dynamic, and functional aspects of a given protein.

### Contact
Questions or suggestions should be addressed to antonielaugusto@gmail.com
