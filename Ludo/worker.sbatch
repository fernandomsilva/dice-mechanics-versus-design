#!/bin/bash
#
#SBATCH --job-name=Worker_Dice
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --array=0-399
#SBATCH --time=40:00:00
#SBATCH --mem=8GB
#SBATCH --mail-type=END
#SBATCH --mail-type=BEGIN
#SBATCH --mail-user=fdm240@nyu.edu

module purge
module load python3/intel/3.6.3

python evolutionWorker.py results-ludo-first-player $SLURM_ARRAY_TASK_ID 10 300

