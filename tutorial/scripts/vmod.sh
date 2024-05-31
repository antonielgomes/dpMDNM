#!/bin/bash

nreps=$(wc -l inputs/list-modes.txt | awk '{print $1}')

for i in $(seq 1 $nreps); do
 mkdir -p vmod/mode-${i}
 /usr/local/charmm/c41b1/charmm -i scripts/vmod.inp modnu=${i} -o vmod/mode-${i}/vmod-${i}.out
done
