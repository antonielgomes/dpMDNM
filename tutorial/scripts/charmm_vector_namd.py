import sys
import struct

"""
Converting Charmm coordinates
to NAMD binaries from a .crd file

This script was written to obtain a vector mode as NAMD binary file
Basically, the script takes XYZ values of each atom in .crd file

Usage: python charmm2namd.py input.crd out.vel
Antoniel A. S. Gomes, 14/02/2020
"""

with open(sys.argv[1], 'r') as f: # Reading .crd file
	coorlst = [] # Creating coordinates list
	vellst = [] # Creating coordinates list

	for line in f:
		if '  EXT' in line:
			n = 1
			for line in f:
				llst=[]
				llst.append(str(line.split()[4]))
				llst.append(str(line.split()[5]))
				llst.append(str(line.split()[6]))
				if line == '\n': break
				coorlst.append(llst)
				n += 1

with open(sys.argv[2],'wb') as outcoor: # Coordinates output
	outcoor.write(struct.pack('i',int(len(coorlst)))) # Writing the number of atoms in NAMD binary
	for i in coorlst:
		for a in i:
			outcoor.write(struct.pack('d',float(str(a)))) # Writing coordinates as NAMD binary

