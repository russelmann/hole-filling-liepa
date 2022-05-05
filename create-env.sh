#!/bin/sh
# Install and configure Conda environment.
# See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
conda env create --file environment.yml --prefix ../hfl-env
conda activate ../hfl-env
conda config --env --set env_prompt '({name})'
conda activate ../hfl-env
conda deactivate
echo Installation finished.
