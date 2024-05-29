# PDIM

**PDIM** (**P**oints in **DIM**ensions) is a minimization script that distibutes N points on the surface of a D-dimensional unit-sphere according to an energetic potential of repulsion function E.

In other words, normalized vectors (radius = 1) are randomly distributed in a unit-sphere, then minimized to generate a uniform distribution.

This script was devised to boost `protein conformational changes` using normal modes. We mapped the `normal mode space` into an `Euclidean space` for a **rational** normal mode combination and protein conformational exploration.

Normal mode combined vectors separated by 1 Å from 2 to 8 dimensions (1.05 Å in 3 dimensions) can be accessed in the [points](https://github.com/antonielgomes/dpMD/tree/main/PDIM/points) directory.
These values can be used as weights for combining vectors in `orthogonal spaces`.

### Code availability
**PDIM** is written in `Python` and uses `numpy` and `scipy` libraries for calculations. The code is free ([PDIM.py](https://github.com/antonielgomes/dpMD/blob/main/PDIM/PDIM.py))for anyone who is interested to optimize it according to their own needs. However, a standalone executable is available for [Linux](https://google.com) and [Windows](https://google.com).

### Cite us!
If you use PDIM or dpMD, please refer to the following publication:

### Usage
PDIM incorporates variables directly from the command line:
```
./PDIM.py -p 10 -d 3 -c 10 -t 0.001 -m classical -o n -s exp
```
or using the python script:
```
python3.8 PDIM.py -p 10 -d 3 -c 10 -t 0.001 -m classical -o n -s exp
```
In this example, 10 points (-p, integer) are distributed in a sphere of 3 dimensions (-d, integer). 10 minimization cycles (-c, integer) are performed, with a tolerance energy (-t, float) of 0.001 per cycle. The classical minimization algorithm (-m, string) is used, without outputting every minimization step (-o, string). The expoent s is incremented (-s, string) by a power of 2 after every minimization cycle.

PDIM generates `start.txt` and `points.txt` files, corresponding to the initial and the final sets of points, respectively.

During minimization, the following variables are printed in every step:
- Mdist: minimal euclidean distance of the system
- Mangle: minimal angle of the system
- Energy: energy of the system

### Tips
- Where can I chat with other ColabFold users?
  - See our [Discord](https://discord.gg/gna8maru7d) channel!

### FAQ
- Why
  - Points are generated randomly and further minimized. Sometimes, it is required several runs to obtain the best distribution of points.
- Why is nergy higher in a new cicle?
  - This is due the s increment, which increases E.


orges-Araújo [^1][^2]; Ana C. Borges-Araújo [^1]; Tugba Nur Ozturk[^3]; Daniel P. Ramirez-Echemendia[^4]; Balázs Fábián [^5]; Timothy S. Carpenter[^3]; Sebastian Thallmair [^6]; Jonathan Barnoud [^7][^8]; Helgi I. Ingólfsson[^3]; Gerard Hummer [^5]; D. Peter Tieleman[^4]; Siewert J. Marrink [^9]; Paulo C. T. Souza [^2]; Manuel N. Melo [^1]

[^1]: Instituto de Tecnologia Química e Biológica António Xavier, Universidade Nova de Lisboa, Av. da República, 2780-157, Oeiras, Portugal;
[^2]: M
