
#PBS -N spoter-zhuo-sweep
#PBS -q gpu
#PBS -l walltime=24:00:00

#PBS -l select=1:ncpus=1:ngpus=1:cluster=adan:mem=10gb
#PBS -j oe
#PBS -m ae

echo "Experiment starting..."

cd /storage/plzen4-ntis/home/mbohacek/spoter-zhuo

module add conda-modules
conda activate cslr-transformers

wandb agent matyasbohacek/Zhuo-collab-SPOTER-Sweep/bh6fc056

