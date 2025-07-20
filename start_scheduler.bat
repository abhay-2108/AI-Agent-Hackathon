@echo off
echo Starting Competitor Feature Tracker Scheduler...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Start the scheduler
echo Starting scheduler...
python scheduler\job_scheduler.py

pause 