@echo off

rem Set the path to your virtual environment
set VENV_PATH=.

rem Check if the virtual environment exists
if not exist %VENV_PATH%\Scripts\activate (
    echo Creating virtual environment...
    python -m venv %VENV_PATH%
)

rem Activate the virtual environment
call %VENV_PATH%\Scripts\activate

rem Upgrade pip
python -m pip install --upgrade pip

rem Install requirements
pip install -r requirements.txt

rem Remove existing build and dist directories
rmdir /s /q build
rmdir /s /q dist

rem Run PyInstaller with the specified command and additional options
pyinstaller --onefile --add-data ".env;." emailing.py

rem Deactivate the virtual environment
call %VENV_PATH%\Scripts\deactivate
