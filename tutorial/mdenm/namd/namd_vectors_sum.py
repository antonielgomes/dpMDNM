import sys
import struct

"""
Summing two each elements in pairs
of NAMD binaries files as one

This script was written to obtain a vector mode as NAMD binary file
Basically, the script takes XYZ values of each atom in each file
then it sums each value and write it to a file

Usage: python charmm2namd.py file1.vel file2.vel out.vel
Antoniel A. S. Gomes, 14/02/2020
"""

def mklst(list):
	lst=[]
	with open(list, 'rb') as f: # Reading .crd file
		file=f.read()
		natoms = struct.unpack('i', file[0:4])
		totval=(natoms[0]*3*8)+4
		init=4
		end=totval
		incr=8
		for atom in range(0,natoms[0]):
			alst=[]
			for val in range(0,3):
				alst.append(struct.unpack('d', file[init:init+incr])[0])
				init = init+incr
			lst.append(alst)
	return lst

def sumlsts(l1,l2):
	if (len(l1) - len(l2)) != 0:
		print("\nI can't sum lists with different sizes.")
		exit()
	sumlsts=[]
	for a, b in zip(l1,l2):
		sumlsts.append([sum(x) for x in zip(a, b)])
	return sumlsts

#Input files
lst1=mklst(sys.argv[1])
lst2=mklst(sys.argv[2])

slst=sumlsts(lst1,lst2)

with open(sys.argv[3],'wb') as outsum: # Sum output
	outsum.write(struct.pack('i',int(len(slst)))) # Writing the number of atoms in NAMD binary
	for i in slst:
		for a in i:
			outsum.write(struct.pack('d',float(str(a)))) # Writing sum coordinates as NAMD binary

