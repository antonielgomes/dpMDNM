# PDIM

**PDIM** (**P**oints in **DIM**ensions) is a minimization script that distributes N points on the surface of a D-dimensional unit-sphere according to an energetic potential of repulsion function E.

In other words, normalized vectors are randomly placed in a unit-sphere, and then minimized to generate a uniform distribution.

<p align="center"><img src="https://github.com/antonielgomes/dpMD/blob/main/PDIM/PDIM.png" width="1000"/></p>

Examples of the minimization progress can be seen in [two](https://youtu.be/p4m_wOLcfo4) and [three](https://youtu.be/elFgtv4bCA0) dimensions.

This script was devised to boost `protein conformational changes` using normal modes. We mapped the `normal mode space` into a `Euclidean space` for a **rational** normal mode combination and protein conformational exploration.

Uniform sets of vectors separated by 1 Å from 2 to 8 dimensions (1.05 Å in 3 dimensions) can be accessed in the [points](https://github.com/antonielgomes/dpMD/tree/main/PDIM/points) directory.
They can be used as weights for combining vectors in `orthogonal spaces`.

### Code availability
PDIM is written in `Python` and uses `numpy` and `scipy` libraries for calculations. The code is available ([PDIM.py](https://github.com/antonielgomes/dpMD/blob/main/PDIM/PDIM.py)) for those who are interested in optimizing it according to their own needs. However, a standalone executable is available for [Linux](https://google.com) and [Windows](https://google.com).

### Usage
PDIM reads input variables directly from the command line:
```
python3 PDIM.py -p 10 -d 3 -c 10 -t 0.01 -m classical -o n -s exp
```
or using the standalone script:
```
./PDIM -p 10 -d 3 -c 10 -t 0.01 -m classical -o n -s exp
```
In this example, 10 points (-p, integer) are distributed in a sphere of 3 dimensions (-d, integer). 10 minimization cycles (-c, integer) are performed, with a tolerance energy (-t, float) of 0.001 per cycle. The classical minimization algorithm (-m, string) is used without outputting every minimization step (-o, string). The exponent s is incremented (-s, string) by a power of 2 after each minimization cycle.

PDIM generates `start.txt` and `points.txt` files, which correspond to the initial and final sets of points, respectively.

During minimization, the following variables are printed in every step:
- Mdist: minimal Euclidean distance of the system
- Mangle: minimal angle of the system
- Energy: energy of the system

They are meaningful for monitoring the quality and `convergence` of data.

### Tips
- Performance is highly affected as higher dimensions are considered. Consider using the `mirrored` algorithm. In this case, an `even number` of vectors is mandatory.
- Sometimes convergence is achieved with smooth minimization progress. In such cases, consider using the `-s sum` flag with a higher number of cycles (-c).
- Although a rigorous convergence tolerance (-t) slows the minimization progress, it is likely to result in a better final set of points. Consider using `lower values`, such as 0.001. 
- The initial set of points is completely random, so a distinct final set of points is expected. It is reasonable to consider performing several runs and selecting the one with `higher` Mdist or Mangle.
- Higher `s` means a higher energy. This explains why E is higher in a new cycle. Compare energy values only `within a cycle`.
- If you want to obtain the set of points of every step, use `-o y`. It will generate files called step_**$(step number)**.txt.

### Reference
If you use dpMDNM or PDIM, please refer to the following publication:

Gomes, A. A. S.; Costa, M. G. S.; Louet, M.; Floquet, N.; Bisch, P. M.; Perahia, D. Extended Sampling of Macromolecular Conformations from Uniformly Distributed Points on Multidimensional Normal Mode Hyperspheres.  _J. Chem. Theory Comput._ **2024**, XX (X), XXX-XXX. DOI: [10.1021/acs.jctc.4c01054](https://doi.org/10.1021/acs.jctc.4c01054)

### Contact
Questions or suggestions should be addressed to antonielaugusto@gmail.com
