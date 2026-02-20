#!/bin/bash

# Zadara Storage MCP Server Setup Script

echo "=========================================="
echo "Zadara Storage MCP Server Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠ No .env file found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠ IMPORTANT: Edit the .env file and add your Zadara credentials"
    echo "   - ZADARA_VPSA_URL"
    echo "   - ZADARA_VPSA_API_KEY"
    echo "   - ZADARA_OBJECT_STORAGE_URL"
    echo "   - ZADARA_OBJECT_ACCESS_KEY"
    echo "   - ZADARA_OBJECT_SECRET_KEY"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Zadara credentials"
echo "2. Test the server: python3 server.py"
echo "3. Configure Claude Desktop with the path to server.py"
echo ""
echo "For detailed instructions, see README.md"
