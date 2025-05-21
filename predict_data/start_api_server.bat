@echo off
REM Script to install dependencies and start the TBATS prediction API server

REM Change to the script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Error: Could not find virtual environment activation script
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo Starting TBATS Prediction API Server...
echo API endpoint available at: http://localhost:5000/predictData
python -m predict_data.run_server

REM Deactivate virtual environment on exit
deactivate