#!/bin/bash

# Exit on any error
set -e

# Setup Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install requests python-dotenv

# Create repository
python repo_creat.py "$1"

# Create Jenkins pipeline job
python create_pipeline.py "$1" "$2"
