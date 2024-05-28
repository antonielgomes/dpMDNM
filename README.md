# dpMD

calculate normal modes
charmm -i scripts/normal-modes.inp


generate crd and dcd of modes:
charmm -i scripts/normal-modes-dcd-crd.inp nmodes=20


generating normal mode combination
bash scripts/mdenm-modes-combination.sh

combine normal modes: charmm -i scripts/generate-combined-modes.inp ncomb=6

MDeNM
scripts/mdenm-namd-exc.sh
scripts/mdenm-namd-md.sh

VMOD
scripts/runvmod-comb.sh = run vmod to obtain displaced conformations

TMD
charmm -i scripts/target.inp nreps=6
bash scripts/tmd-namd.sh
charmm -i scripts/restraints.inp nreps=6
bash scripts/tmd-equil-namd.sh
bash scripts/tmd-free-md-namd.sh
