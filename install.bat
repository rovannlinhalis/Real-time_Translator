@echo off
REM Installation script for Real-time Translator on Windows

echo Installing Real-time Translator...

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install basic dependencies
echo Installing core dependencies...
pip install python-dotenv

REM Install Python packages
echo Installing Python packages...
pip install openai speechrecognition python-dotenv numpy

REM Optional GUI dependencies
echo Attempting to install GUI dependencies...
pip install pyttsx3

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Run the demo: python demo.py
echo 2. Configure API key in config.env
echo 3. For CLI version: python translator_cli.py
echo 4. For GUI version: python translator_app.py
echo.
echo If you encounter issues:
echo - Install packages individually: pip install package-name
echo - For audio support, install PyAudio: pip install pyaudio