#!/bin/bash

echo "Performing free-md"

nreps=$(wc -l inputs/list-modes.txt | awk '{print $1}')
for rep in $(seq 1 $nreps); do
	export rep=$rep
	echo "mode-${rep}..."
	mkdir ./dpmd/mode-${rep}/free-md/
	cd    ./dpmd/mode-${rep}/free-md/
	scp ../../../scripts/dpmd-free-md.inp ./dpmd-free-md.inp

	for dstep in 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3; do
		export dstep=$dstep
		echo "step ${dstep} submitted"
		/usr/local/namd2/namd2 +p 2 dpmd-free-md.inp > free-md_${rep}_${dstep}.out
		sleep 3
	done
	cd ../../../
done
