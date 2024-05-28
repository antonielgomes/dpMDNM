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

import sys
import time
import getopt
import signal
import itertools
import numpy as np
from scipy.optimize import minimize

print(__doc__)
start = time.time()

#If no parameters are given
if not sys.argv[1:]:
    print('Input error:\nNo input parameters')
    print('\nPlease, give at lease one of the parameters below:')
    print('\n-p: number of points. Integer number\n-d: number of dimensions. Integer number')
    print('-c: number of cycles. Integer number\n-t: energy gradient tolerance. Float number')
    print('-m: minimization method (classical or mirrored). String')
    print('-o: print points every step (y = yes and n = no). String')
    print('-s: increment s by 1 (sum) or a power of 2 (exp). String')
    print('\nStandard usage: python PDIM.py -p 10 -d 3 -c 10 -t 0.001 -m classical -o n -s exp')
    print('\nNot clear enough? Read the documentation above! :)')
    sys.exit()

#Read inputs
variables, arguments = getopt.getopt(sys.argv[1:], 'p:d:c:t:m:o:s:', ['--npoints', '--ndimensions','--ncycles','--tolerance','--minimization','--output','--sincrement'])
for var, arg in variables:
    if var in ('-p', '--npoints'):
        npoints = int(arg)
    elif var in ('-d', '--ndimensions'):
        ndim = int(arg)
    elif var in ('-c', '--ncycles'):
        ncycles = int(arg)
    elif var in ('-t', '--tolerance'):
        tol = float(arg)
    elif var in ('-m', '--minimization'):
        mtype = str(arg)
    elif var in ('-o', '--output'):
        outfiles = str(arg)
    elif var in ('-s', '--sincrement'):
        sincr = str(arg)

#Try inputs. If not defined, set defaults
try: npoints
except NameError: npoints=None
if npoints is None: npoints=int(10)
if npoints < 1:
    print('Input error:\nThe number of points (-p) must be a positive integer number greater than 1')
    sys.exit()
try: ndim
except NameError: ndim=None
if ndim is None: ndim=int(3)
if ndim < 2:
    print('Input error:\nThe number of dimensions (-d) must be a positive integer number greater than 1')
    sys.exit()
try: ncycles
except NameError: ncycles=None
if ncycles is None: ncycles=int(10)
if ncycles < 1:
    print('Input error:\nThe number of points (-p) must be a positive integer number greater than 0')
    sys.exit()
try: tol
except NameError: tol=None
if tol is None: tol=float(0.001)
if tol < 0:
    print('Input error:\nThe energy gradient tolerance (-t) must be a positive integer number')
    sys.exit()
try: mtype
except NameError: mtype=None
if mtype is None: mtype=str('classical')
elif mtype not in ('classical', 'mirrored'):
    print('Input error:\nUnrecognized parameter for -m: '+str(mtype))
    print('Please select one of the two minimization methods (-m) available:')
    print('\t1) classical: minimize each point in the system\n\t2) mirrored: minimize half of the points in the system, mirroring the other half')
    sys.exit()
try: outfiles
except NameError: outfiles=None
if outfiles is None: outfiles=str('n')
elif outfiles not in ('y', 'n'):
    print('Input error:\nUnrecognized parameter for -o: '+str(outfiles))
    print('Please select one of the two output options:')
    print('\t1) y: print points every minimization step\n\t2) n: do not proint points every minimization step, only initial (start.txt) and final points (points.txt)')
    sys.exit()
try: sincr
except NameError: sincr=None
if sincr is None: sincr=str('exp')
elif sincr not in ('sum', 'exp'):
    print('Input error:\nUnrecognized parameter for -s: '+str(sincr))
    print('Please select one of the two output options:')
    print('\t1) sum: increment s by 1 after every minimization step (s = s + 1)\n\t2) exp: increment s by power of 2 after every minimization step (s = s^2)')
    sys.exit()

#Test if the number of points is an odd number
if mtype == 'mirrored':
    if (npoints % 2) != 0:
        print('Input error:\nThe number of points (-p) is an odd number: '+str(npoints))
        print('Tip: When using the mirrored minimization method, ask for an even number of points')
        sys.exit()

###Functions###

#Mirror a vector
def mirror(v):
    vneg=[]
    for i in range(ndim):
        if (v[i] == 0.0): vneg.append(v[i])
        else: vneg.append(v[i]*-1.0)
    return np.array(vneg)

#Minimal distance of a list of points
def mdist(x):
    di = []
    for i,j in itertools.combinations(x, 2):
        di.append(np.linalg.norm(np.array(i)-np.array(j)))
    return np.min(di)

#Minimal angle of a list of points
def mangle(x):
    angles = []
    for i,j in itertools.combinations(codes, 2):
        angles.append(np.arccos(np.clip(np.dot(i, j), -1.0, 1.0)))
    return np.degrees(np.min(angles))

#Energy of list of points (global energy)
def ener(x):
    di = []
    for i,j in itertools.combinations(x, 2):
        di.append(np.linalg.norm(np.array(i)-np.array(j)))
    E = np.sum( ( initialdist / np.array(di) )**s )
    return E

#Elapsed time
def elapsed(x):
    end = x - start
    if end < 60.0:
        print('\nElapsed time: '+str(round(end,2))+' seconds')
    elif (end > 60.0) and (end < 3600):
        min = int(end / 60.0)
        sec = (end -(60. * float(min)))
        print('\nElapsed time: '+str(round(min,2))+' minutes'+' and '+str(round(sec,2))+' seconds')
    else:
        hours = int(end / 3600.)
        min = ((end / 3600.) - float(hours)) * 60
        print('\nElapsed time: '+str(round(hours,2))+' hours'+' and '+str(round(min,2))+' minutes')

#If stopped, save the last minimized codes
def keyboardInterruptHandler(signal, frame):
    print('\n\tMinimization has stopped!\n')
    print('Last Mdist:  '+str(mdist(codes)))
    print('Last Mangle: '+str(mangle(codes)))
    print('Last Energy: '+str(Ef))
    print('\n\tLast Points:\n')
    for i in codes:
        print(' '.join(map(str, i)))
    with open('points.txt', 'w') as f:
        for item in codes:
            f.write(str(' '.join(map(str, item)))+'\n')
    elapsed(time.time())
    sys.exit()

signal.signal(signal.SIGINT, keyboardInterruptHandler)

#Minimization function
def minimization(list):
    #Backup of the last codes
    bcodes = []
    [bcodes.append(x) for x in list]
    #Objective function to minimize each point (local minimization)
    #Classical
    def objclassical(x):
        di = []
        for i in range(len(list)):
            if i != curr:
                d = np.linalg.norm(x-np.array(list[i]))
                di.append(d)
        try:
            e = np.sum( ( initialdist / np.array(di) )**s )
        except OverflowError as x:
            print('\n\tFunction overflow!')
            codes = []
            [codes.append(x) for x in bcodes]
            keyboardInterruptHandler(1.,1.)
        return e
    
    #mirrored
    def objmirrored(x):
        di = []
        tcodes = []
        for i in range(npoints):
            tcodes.append(list[i])
        for i in range(npoints):
            tcodes.append(mirror(list[i]))
        for i in range(len(list)):
            if i != curr:
                d = np.linalg.norm(x-np.array(tcodes[i]))
                di.append(d)
        try:
            e = np.sum( ( initialdist / np.array(di) )**s )
        except OverflowError as x:
            print('\n\t   Function overflow!')
            codes = []
            [codes.append(x) for x in bcodes]
            keyboardInterruptHandler(1.,1.)
        return e

    #Jacobian Matrix to prevent erros
    def jacobian(x):
        x0 = np.asfarray(x)
        f0 = np.atleast_2d(obj(*((x0,))))
        jac = np.zeros([len(x0), len(f0)])
        dx = np.zeros(len(x0))
        for i in range(len(x0)):
            dx[i] = np.sqrt(np.finfo(float).eps)
            jac[i] = (obj(*((x0+dx,))) - f0)/(np.sqrt(np.finfo(float).eps))
            dx[i] = 0.0
        return jac.transpose()
    
    #Constraints to obtain solutions with unit vectors only
    def unit(x):
        return np.linalg.norm(x) - 1.0
    cons = {'type':'eq', 'fun': unit}
    
    #Bounds to limit the solutions from -1 to 1
    bounds = []
    [bounds.append(tuple([-1.,1.])) for x in range(ndim)]

    #Minimize each point
    for i in range(npoints):
        #Temporary codes. A necessary trick to update lists in Python
        tcodes = []
        [tcodes.append(x) for x in list]
        #Energy of the temporary codes
        Eti = ener(tcodes)
        curr = i
        #Define the objective function
        if mtype == 'mirrored': obj=objmirrored
        else: obj=objclassical
        #Local minimization
        sol = minimize(obj, np.array(list[i]), method='SLSQP', constraints=cons, jac=jacobian, args=(), bounds=tuple(bounds), options={'ftol': 1e-5, 'disp': False, 'maxiter': 10000})
        #Prevent erros
        #If the function fails, stop mimization
        #Usually, this happens due to the function exhaustiveness
        if (np.isnan(sol.x).any() ==  True):
            print('\n\tNaN value found!')
            keyboardInterruptHandler(1.,1.)
        elif (np.around(np.linalg.norm(sol.x)) != 1.0):
            print('\n\tPoint jumpped out the sphere!')
            keyboardInterruptHandler(1.,1.)
        #Update the solution to codes
        tcodes[i] = sol.x
        if mtype == 'mirrored': tcodes[i+npoints] = mirror(sol.x)
        #Energy of the codes considering the new solution
        Et = ener(tcodes)
        #Global minimization: accept the new codes only if the energy is decreased
        if (Et < Eti):
            list[i] = sol.x
            if mtype == 'mirrored': list[i+npoints] = mirror(sol.x)
    return list

###Initiation###

#If mirrored is selected, process only half of points
if mtype == 'mirrored':
    npoints = int(npoints/2)

#Prevent s to be equal to zero
if ndim < 3:
    s=int(ndim - 1)
else:
    s=int(ndim - 2)

#Generate the points randomly
codes = []
for i in range(npoints):
    vec = np.random.randn(1,ndim)
    vec /= np.linalg.norm(vec,axis=1)
    codes.append(vec[0])

#Add the mirrored points to codes
if mtype == 'mirrored':
    for i in range(npoints):
        codes.append(mirror(codes[i]))

#Print parameters
print('\t# Start #')
print('\n\tInitial parameters:\n')
print('Number of points:          '+str(len(codes)))
print('Number of dimensions:      '+str(ndim))
print('Number of cycles:          '+str(ncycles))
print('Energy gradient tolerance: '+str(tol))
print('Minimization method:       '+str(mtype))
print('Output:                    '+str(outfiles))
print('s increment:               '+str(sincr))
print('\n\tInitial Points:\n')

#Print the initial codes
for i in codes:
    print(' '.join(map(str, i)))

initialdist = mdist(codes)
print('\nMdist:  '+str(mdist(codes)))
print('Mangle: '+str(mangle(codes)))
print('Energy: '+str(ener(codes)))

#Write the initial codes to a file
with open('start.txt', 'w') as f:
    for item in codes:
        f.write(str(' '.join(map(str, item)))+'\n')

#Initial input variables
Ef = ener(codes) #Energy of the initial codes

#Exponent of the minimization function
#Different values allows good results in different conditions as number of points and/or dimentions
#s=ndim*3
step = 0 #Step number

#Minimization cycle
for cycle in range(ncycles):
    print('\n\tCycle '+str(cycle+1)+' (s = '+str(s)+')')
    dE = np.inf #Initial energy to infinty
    initialdist = mdist(codes) #Initial mdist
    #Minimize until reach the gradient desired
    while (dE > tol):
        step = step + 1
        Ei = ener(codes)
        #Temporary codes. A necessary trick to update lists in Python
        tcodes = []
        [tcodes.append(x) for x in codes]
        #Minimize the codes
        mcodes = minimization(tcodes)
        #Energy of the minimized codes
        Ef = ener(mcodes)
        #Energy variation after minimization
        dE = abs(Ef - Ei)
        #Print parameters
        print('\n\tStep '+str(step))
        print('Mdist:  '+str(mdist(mcodes)))
        print('Mangle: '+str(mangle(mcodes)))
        print('Energy: '+str(Ef))
        #Update codes
        codes = []
        [codes.append(x) for x in mcodes]
        #Write the new codes to a file
        if outfiles == 'y':
                with open('step_%s.txt' % step, 'w') as f:
                    for item in codes:
                        f.write(str(' '.join(map(str, item)))+'\n')
    #Play with the increment of s
    if sincr == 'sum':
        s = s + 1
    elif sincr == 'exp':
        s = s * 2
    #else:
    #    s = s * 2
#    s = s * 2

###Termination###

#Print variables
print('\n\t# Termination #\n')
print('Final Mdist:  '+str(mdist(codes)))
print('Final Mangle: '+str(mangle(codes)))
print('Final Energy: '+str(Ef))
print('\n\tFinal Points:\n')

#Print the final codes
for i in codes:
    print(' '.join(map(str, i)))

#Save the final codes
with open('points.txt', 'w') as f:
    for item in codes:
        f.write(str(' '.join(map(str, item)))+'\n')

# Time elapsed
elapsed(time.time())
sys.exit()
