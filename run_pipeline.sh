#!/bin/bash

# this code will exit if there is going to be any error 
set -e


WORKSPACE=$(pwd)
echo " current working directory: $WORKSPACE"

# check the content of the working directory
echo "Contents of the working directory:"
ls -la $WORKSPACE

# set up virtual environment to avoide conflicts
echo "Setting up  virtual environment "
python3 -m venv "$WORKSPACE/venv"
# Activate virtual environment
source "$WORKSPACE/venv/bin/activate"

# list installed packages to see and verify
echo "all installed packages in the  environment"
pip list

# install all dependencies
echo "installing dependencies "
pip install requests python-dotenv python-jenkins

# list packages to check if it is installed  verify
echo "list installed packages after installation"
pip list

# list everything again to check before running the script
echo "this is the contents of the working directory "
ls -la $WORKSPACE

# run the repo creation python script $1 first commad line argument passed represents a repo name 
echo "Running repo_creat.py file "
python "$WORKSPACE/repo_create.py" "$1"

# run the pipeliine creation python script jenkins job name and repo sname form command line argument
echo "Running create_pipeline.py file"
python "$WORKSPACE/pipeline_create.py" "$1" "$2"

