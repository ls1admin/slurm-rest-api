#!/bin/bash
echo "Activating conda environment"
source activate env/
rc=$?; if [[ $rc != 0 ]]; then echo "Did you forget to run build.sh first?"; exit $rc; fi

echo "Running tests"
python -m unittest discover -s slurm-rest-api/
