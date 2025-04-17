#!/bin/bash
project_name="InsuranceClaimAutomation"

# Create virtual environment
python3 -m venv env

# Activate it and install dependencies
source ./env/Scripts/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install ipykernel

# Add as Jupyter kernel
python -m ipykernel install --user --name=${project_name} --display-name "Python (${project_name})"

echo "setup complete. Kernel 'Python (${project_name})' is ready."

# Dynamically generate a project directory tree structure
tree -I '__pycache__|env|.git' -L 2

deactivate
