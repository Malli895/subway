@echo off
echo Creating/setting up virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment exists.
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing requirements...
pip install -r requirements.txt
echo Starting Streamlit dashboard...
start chrome http://localhost:8501
streamlit run dashboard.py --server.headless true --server.port 8501 --browser.gatherUsageStats false
echo Dashboard running at http://localhost:8501
echo Close this window to stop the server.
pause
