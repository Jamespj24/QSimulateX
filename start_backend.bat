@echo off
echo Starting QSimulateX Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Start the FastAPI server
echo.
echo ===============================================
echo   QSimulateX Backend Starting...
echo   API will be available at: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ===============================================
echo.

python -m quantum_simulator.api
