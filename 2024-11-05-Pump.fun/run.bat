@echo off
REM Set the name for the virtual environment
set VENV_NAME=venv

REM Create a virtual environment
python -m venv %VENV_NAME%

REM Activate the virtual environment
call %VENV_NAME%\Scripts\activate

REM Upgrade pip (optional)
python -m pip install --upgrade pip

REM Install required modules from requirements.txt
pip install -r requirements.txt

REM Run the main.py file
python main.py