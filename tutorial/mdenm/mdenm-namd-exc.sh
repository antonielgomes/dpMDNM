#!/bin/bash

#get number of replicas (mode combinations)
nreps=$(wc -l ./inputs/list-modes.txt | awk '{print $1}')

#generating namd topologies
mkdir ./mdenm/namd/toppar/
python ./scripts/convert_par2namd.py ./toppar.str ./toppar/ ./mdenm/namd/

#generating namd input files
tr '[:upper:]' '[:lower:]' < inputs/step3.str | sed -e "s/ =//g" | grep -v "set prot" > ./mdenm/namd/step3.str

cd ./mdenm/namd/
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
echo "Performing excitations"
cd ../excitations/

for rep in $(seq 1 $nreps); do
	export rep=$rep
	echo "replica ${rep}..."
	cd ./$rep/
	scp ../../namd/namd-exc.inp ./namd-exc.inp

	for exc in {1..10}; do
		export exc=$exc
		echo "excitation ${exc} submitted"
		/usr/local/namd2/namd2 +p 2 namd-exc.inp > rep-$rep-e$exc.out
		sleep 3
	done
	cd ../
done
