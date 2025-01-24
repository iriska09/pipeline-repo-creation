#!/bin/bash

# Exit on any error
set -e

# Get the current working directory
WORKSPACE=$(pwd)

# Setup Python virtual environment
python3 -m venv "$WORKSPACE/venv"

# Activate virtual environment
source "$WORKSPACE/venv/bin/activate"

# Install dependencies
pip install requests python-dotenv

# Create repository
python "$WORKSPACE/repo_creat.py" "$1"

# Create Jenkins pipeline job
python "$WORKSPACE/create_pipeline.py" "$1" "$2"
