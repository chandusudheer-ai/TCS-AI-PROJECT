@echo off

echo.
echo Installing required Python packages...
echo.

pip install -r requirements.txt

echo.
echo =========================================
echo Starting Streamlit Application...
echo =========================================
echo.

streamlit run app.py

pause