@echo off
echo Starting QSimulateX Frontend...
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
)

REM Start the development server
echo.
echo ===============================================
echo   QSimulateX Frontend Starting...
echo   Web UI will be available at: http://localhost:3000
echo ===============================================
echo.

call npm run dev
