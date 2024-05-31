#!/bin/bash

rep=1
rm -r ./mdenm/excitations
mkdir ./mdenm/excitations
mkdir ./mdenm/excitations/struct-list
touch ./mdenm/excitations/struct-list/struct-list.txt

nreps=$(wc -l ./inputs/list-modes.txt | awk '{print $1}')

for rep in $(seq 1 $nreps); do
	mkdir ./mdenm/excitations/$rep
	echo "rep ${rep} submitted"
	charmm -i ./mdenm/mdenm-combined-modes.inp inputfile=./mdenm/input-mdenm.txt rep=$rep -o ./mdenm/excitations/$rep/mdenm-combined-modes.out
	((rep++))
done
