#!/bin/bash

#generating namd topologies
mkdir ./dpmdnm/
mkdir ./dpmdnm/toppar/
python ./scripts/convert_par2namd.py ./toppar.str ./toppar/ ./dpmdnm/

#generating namd input files
tr '[:upper:]' '[:lower:]' < inputs/step3.str | sed -e "s/ =//g" | grep -v "set prot" > ./dpmdnm/step3.str

cd ./dpmdnm/
colname=col.col
echo -e "#\n# protein center of mass restraint\n#\n\ncolvar {name COM\ndistance {group1 {" > $colname
echo psfSegID $(grep chain step3.str | awk '{for(i=4;i<NF;++i)print $i}') >> $colname
for i in $(seq 1 $(grep nchains step3.str | awk '{print $NF}')); do
	echo atomNumbersRange $(grep "index" step3.str | awk -v inc=$i '{print $(3+inc)}') >> $colname
done
echo -e "}\n" >> $colname
echo -e "group2 {dummyAtom ($(grep xcen step3.str | awk '{print $NF}'), $(grep ycen step3.str | awk '{print $NF}'), $(grep zcen step3.str | awk '{print $NF}'))}}}\n" >> $colname
echo -e "harmonic {colvars COM\ncenters $(grep xcen step3.str | awk '{print $NF}'), $(grep ycen step3.str | awk '{print $NF}'), $(grep zcen step3.str | awk '{print $NF}')\nforceConstant 1.0}" >> $colname

echo "Input files generated..."

#excitations
echo "Performing tmd"

nreps=$(wc -l ../inputs/list-modes.txt | awk '{print $1}')
for rep in $(seq 1 $nreps); do
	export rep=$rep
	echo "mode-${rep}..."
	mkdir ./mode-${rep}/tmd/
	cd    ./mode-${rep}/tmd/
	scp ../../../scripts/dpmdnm-tmd.inp ./dpmdnm-tmd.inp

	for dstep in 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3; do
		export dstep=$dstep
		echo "step ${dstep} submitted"
		/usr/local/namd2/namd2 +p 2 dpmdnm-tmd.inp > tmd_${rep}_${dstep}.out
		sleep 3
	done
	cd ../../
done
