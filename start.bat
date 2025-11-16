@echo off
REM start.bat - create venv if missing, install requirements, run main.py
setlocal

cd /d "%~dp0"

REM if venv python doesn't exist, create virtual environment
echo Checking for virtual environment...
if not exist ".venv\Scripts\python.exe" (
	echo Creating virtual environment...
	python -m venv .venv || (
		echo ERROR: Failed to create venv. Make sure Python is on PATH.
		exit /b 1
	)
)

REM Activate venv
echo Activating virtual environment...
call ".venv\Scripts\activate.bat" || (
	echo ERROR: Failed to activate virtual environment.
	exit /b 1
)

REM Ensure pip/tools are up-to-date
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel >nul

REM Install requirements if requirements.txt exists
echo Checking for requirements list...
if exist "requirements.txt" (
	echo Installing requirements...
	python -m pip install -r "requirements.txt" || (
		echo ERROR: Failed to install requirements.
		exit /b 1
	)
) else (
	echo No requirements.txt found, try running anyway
)

REM Run main.py (forward any arguments)
echo Running main program...
python "main.py" %* 
endlocal

