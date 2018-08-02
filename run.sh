#!/bin/bash

echo ""
echo "Activating conda environment"
source activate env/
rc=$?; if [[ $rc != 0 ]]; then echo "Did you forget to run build.sh first?"; exit $rc; fi

echo ""
echo "Exporting flask environment variable"
export FLASK_APP=slurm-rest-api

echo ""
echo "Running Application"
flask run --host='0.0.0.0'
