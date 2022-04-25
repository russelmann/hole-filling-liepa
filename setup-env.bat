REM Install and configure Conda environment.
@REM See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
call conda env create --file environment.yml --prefix env
call conda activate ../env
call conda config --env --set env_prompt ({name})
call conda activate ../env
call conda deactivate
REM Installation finished.
