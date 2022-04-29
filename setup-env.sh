#!/bin/sh
# Install and configure Conda environment.
# See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
conda env create --file module/environment.yml --prefix ./env
conda activate ./env
conda config --env --set env_prompt '({name})'
conda activate ./env
conda deactivate
echo Installation finished.
