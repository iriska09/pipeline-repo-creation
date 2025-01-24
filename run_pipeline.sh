#!/bin/bash

# Exit on any error
set -e

# Get the current working directory
WORKSPACE=$(pwd)
echo "Current working directory: $WORKSPACE"

# List the contents of the working directory
echo "Contents of the working directory:"
ls -la $WORKSPACE

# Setup Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv "$WORKSPACE/venv"

# Activate virtual environment
echo "Activating virtual environment..."
source "$WORKSPACE/venv/bin/activate"

# List installed packages for verification
echo "Installed packages in the virtual environment:"
pip list

# Install dependencies
echo "Installing dependencies..."
pip install requests python-dotenv python-jenkins

# List installed packages for verification after installation
echo "Installed packages after installation:"
pip list

# List the contents again to confirm before running the script
echo "Contents of the working directory before running scripts:"
ls -la $WORKSPACE

# Create repository
echo "Running repo_creat.py..."
python "$WORKSPACE/repo_create.py" "$1"

# Create Jenkins pipeline job
echo "Running create_pipeline.py..."
python "$WORKSPACE/pipeline_create.py" "$1" "$2"

