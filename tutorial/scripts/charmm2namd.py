import sys
import struct
import re

"""
Converting Charmm coordinates and velocities
to NAMD binaries from a .rst file
Cell basis vectors found in source/image/crystal.src:

Lattice Vectors:
A = ',XTLABC(1),XTLABC(2),XTLABC(4)
B = ',XTLABC(2),XTLABC(3),XTLABC(5)
C = ',XTLABC(4),XTLABC(5),XTLABC(6)

Usage: python charmm2namd.py input.rst out.coor out.vel out.xsc
Antoniel A. S. Gomes, 10/09/2018
"""

with open(sys.argv[1], 'r') as f: # Reading .rst file
        pbclst = [] # Creating pbc list
	coorlst = [] # Creating coordinates list
	vellst = [] # Creating velocities list
	pbclst.append(str('# NAMD extended system configuration output file\n#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z o_x o_y o_z s_x s_y s_z s_u s_v s_w'))
        for line in f:
		if '!CRYSTAL PARAMETERS' in line:
			n = 1
			for line in f:
				if n == 1:
					line = re.sub('([D])(...)',r'\1\2 ', line)
					line = re.sub('D',r'e', line)
					pbclst.append(str(line.split()[0]))
					pbclst.append(str(line.split()[1]))
					pbclst.append(str(line.split()[2]))
				if n == 2:
					line = re.sub('([D])(...)',r'\1\2 ', line)
					line = re.sub('D',r'e', line)
					pbclst.append(str(line.split()[0]))
					pbclst.append(str(line.split()[1]))
					pbclst.append(str(line.split()[2]))
					break
				n += 1
                if '!NATOM,NPRIV,NSTEP,NSAVC,NSAVV,JHSTRT,NDEGF,SEED,NSAVL' in line:
			pbclst.append(str(next(f).split()[2]))
		if '!XOLD, YOLD, ZOLD' in line:
			for line in f:
				line = re.sub('([D])(...)',r'\1\2 ', line)
				line = re.sub('D',r'e', line)
				if line == '\n': break
				coorlst.append(line.split())

                if '!VX, VY, VZ' in line:
                        for line in f:
                                line = re.sub('([D])(...)',r'\1\2 ', line)
                                line = re.sub('D',r'e', line)
                                if line == '\n': break
                                vellst.append(line.split())

with open(sys.argv[2],'wb') as outcoor: # Coordinates output
	outcoor.write(struct.pack('i',int(len(coorlst)))) # Writing the number of atoms in NAMD binary
	for i in coorlst:
		for a in i:
			outcoor.write(struct.pack('d',float(str(a)))) # Writing coordinates as NAMD binary

with open(sys.argv[3],'wb') as outvel: # Velocities output
	outvel.write(struct.pack('i',int(len(vellst)))) # Writing the number of atoms in NAMD binary
	for i in vellst:
		for a in i:
			outvel.write(struct.pack('d',float(str(a)))) # Writing velocities as NAMD binary

with open(sys.argv[4],'w') as outpbc: # PBC output
	outpbc.write(str(pbclst[0]) + '\n' + str(pbclst[7]) + ' ' + str(pbclst[1]) + ' ' + str(pbclst[2]) + ' ' + str(pbclst[4])\
	+ ' ' + str(pbclst[2]) + ' ' + str(pbclst[3]) + ' ' + str(pbclst[5])\
	+ ' ' + str(pbclst[4]) + ' ' + str(pbclst[5]) + ' ' + str(pbclst[6])\
	+ ' 0 0 0 ' + '0 0 0'+ ' 0 0 0')
