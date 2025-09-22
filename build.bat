@echo off
REM Build script for Real-time Translator on Windows

echo Building Real-time Translator...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Create executable
echo Creating executable...
pyinstaller --onefile --windowed --name "RealTimeTranslator" translator_app.py

REM Copy configuration template
copy config.env.example dist\config.env.example

echo Build complete! Executable is in the 'dist' directory.
echo Before running:
echo 1. Copy config.env.example to config.env
echo 2. Edit config.env and add your OpenAI API key
echo 3. Run the executable