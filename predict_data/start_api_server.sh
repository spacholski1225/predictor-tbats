#!/bin/bash

# Script to install dependencies and start the TBATS prediction API server

# Change to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find virtual environment activation script"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "Starting TBATS Prediction API Server..."
echo "API endpoint available at: http://localhost:5000/predictData"
python -m predict_data.run_server

# Deactivate virtual environment on exit
deactivate