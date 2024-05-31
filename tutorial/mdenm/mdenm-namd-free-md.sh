#!/bin/bash

#free-md
echo "Performing free-md"

nreps=$(wc -l ./inputs/list-modes.txt | awk '{print $1}')

cd ./mdenm/excitations/

for rep in $(seq 1 $nreps); do
	export rep=$rep
	echo "replica ${rep}:"
	mkdir ./$rep/free-md/
	cd ./$rep/free-md/
	scp ../../../namd/namd-free-md.inp ./namd-free-md.inp

	for exc in {1..10}; do
		export exc=$exc
		echo "excitation ${exc} submitted"
		/usr/local/namd2/namd2 +p2 namd-free-md.inp > md-rep-$rep-e$exc.out
		sleep 3
	done
	cd ../../
done
