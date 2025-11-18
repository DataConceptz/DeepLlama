#!/bin/bash
# Run script for DeepLlama

echo "Starting DeepLlama - AI Literature Review Tool"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo ""
    echo "⚠️  Warning: Ollama does not appear to be running!"
    echo "   Please start Ollama before using AI features."
    echo "   Visit https://ollama.ai for installation instructions."
    echo ""
fi

# Run the application
echo ""
echo "Launching DeepLlama..."
python3 main.py
