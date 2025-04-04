@echo off
:: Move to your project directory
cd /d C:\Users\posla\Documents\Projects\verse-of-the-day

:: Activate your virtual environment
call venv\Scripts\activate

:: Open VS Code in this directory
code .

:: Run your Python script
python main.py

:: Keep the command prompt open to view output
pause
