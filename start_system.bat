@echo off
echo Starting AI Powered Attendance Tracking System...

echo Installing dependencies...
cd backend
pip install fastapi uvicorn pymongo python-multipart

echo Starting Backend Server...
start /B python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo Waiting for backend to start...
timeout /t 5

echo Installing frontend dependencies...
cd ..\frontend
pip install streamlit plotly pandas requests

echo Starting Frontend...
cd streamlit_app
start streamlit run Home.py --server.port 8501

echo System started successfully!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo API Docs: http://localhost:8000/docs

pause