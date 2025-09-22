#!/bin/bash

# Build script for Real-time Translator
echo "Building Real-time Translator..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Create executable
echo "Creating executable..."
pyinstaller --onefile --windowed --name "RealTimeTranslator" translator_app.py

# Copy configuration template
cp config.env.example dist/config.env.example

echo "Build complete! Executable is in the 'dist' directory."
echo "Before running:"
echo "1. Copy config.env.example to config.env"
echo "2. Edit config.env and add your OpenAI API key"
echo "3. Run the executable"