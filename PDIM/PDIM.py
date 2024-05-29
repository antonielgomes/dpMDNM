"""
PDIM distributes N Points on the surface of a D-DIMensions unit sphere
by an energetic potential of repulsion function E.
The Least-Squares approximation algorith is used to
minimize the energy function (E) of the system.

Reference:
D. A. Kottwitz. The Densest Packing of Equal Circles on a Sphere.
Acta Cryst. (1991). A47, 158-165

Required libraries: scipy and numpy.

Default example:
For 10 points in 3 dimensions with 10 cycles and energy gradient tolerance of 1e-3 using the classical minimization method:

Usage:
python PDIM.py -p 10 -d 3 -c 10 -t 0.001 -m classical -o n -s exp

-p: number of points. Integer number
-d: number of dimensions. Integer number
-c: number of cycles. Integer number
-t: energy gradient tolerance. Float number
-m: minimization method (classical or mirrored). String
-o: output points during minimization (y or n). String
-s: s increment (sum or exp). String

Printed variables:
- Initial/Final Points: coordinates of the points
- Mdist: minimal euclidean distance of the system
- Mangle: minimal angle of the system
- Energy: energy of the system*

*: compare the energies only from its correspondent cycle

Tricks:
- The best solution is when s tends to infinity,
  however you must start from a small value.
  This script considers s equals the number of dimensions - 2
  incremented by N every cycle -c;
- The accuracy of the minimization is directly dependents of both
  (i) the energy gradient tolerance (-t) of the gradient (dE) and
  (ii) the number of cycles (-c);
- If you are satisfied with the minimized codes (See Mdist and Mangle), you can
  stop the script typing Ctrl+C to return the last minimized points
- Sometimes the minimal energy is not reached probably due
  a large number of points, unfortunately
- When using the mirrored minimization method, think about symmetry

Author: Antoniel A. S. Gomes (antonielaugusto@gmail.com)
"""
