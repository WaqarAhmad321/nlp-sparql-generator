#!/bin/bash

# Installation script for NL to SPARQL Converter

echo "============================================"
echo "NL to SPARQL Converter - Installation"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies!"
    exit 1
fi

echo ""
echo "Downloading spaCy language model..."
python3 -m spacy download en_core_web_sm

if [ $? -ne 0 ]; then
    echo "Warning: Failed to download spaCy model. Will try on first run."
fi

echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "To test without UI:"
echo "  python3 test_queries.py"
echo ""
