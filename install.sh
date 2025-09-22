#!/bin/bash

# Installation script for Real-time Translator
echo "Installing Real-time Translator..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install basic dependencies
echo "Installing core dependencies..."
pip install python-dotenv

# Try to install audio dependencies
echo "Installing audio dependencies..."
if command -v apt-get &> /dev/null; then
    echo "Detected apt package manager (Ubuntu/Debian)"
    echo "You may need to install system dependencies:"
    echo "sudo apt-get update"
    echo "sudo apt-get install python3-tk portaudio19-dev"
elif command -v brew &> /dev/null; then
    echo "Detected Homebrew (macOS)"
    echo "You may need to install system dependencies:"
    echo "brew install portaudio tk"
fi

# Try to install Python packages
echo "Installing Python packages..."
pip install openai speechrecognition python-dotenv numpy || echo "Some packages failed to install"

# Optional GUI dependencies
echo "Attempting to install GUI dependencies..."
pip install pyttsx3 || echo "TTS package failed to install (optional)"

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run the demo: python3 demo.py"
echo "2. Configure API key in config.env"
echo "3. For CLI version: python3 translator_cli.py"
echo "4. For GUI version: python3 translator_app.py"
echo ""
echo "If you encounter issues:"
echo "- Check system dependencies mentioned above"
echo "- Install packages individually: pip install <package-name>"