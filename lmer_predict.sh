#!/bin/bash
#
#SBATCH --job-name=lmer_predict_test
#SBATCH --output=lmer_predict.log
#
#SBATCH --ntasks=1
#SBATCH --time=4320:00 # 3 days
#SBATCH --mem-per-cpu=100 #megabytes
#SBATCH --cpus-per-task=4

python to_cross_reactivity_matricies.py
