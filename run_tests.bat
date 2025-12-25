@echo off
echo Installing required packages...
pip install -r test_requirements.txt

echo.
echo Running AI Powered Attendance Tracking System Tests...
echo.

python test_complete_system.py

pause