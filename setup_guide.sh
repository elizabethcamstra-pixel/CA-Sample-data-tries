#!/bin/bash

# Chamber Location Analytics - Setup Script
# This script helps you get started quickly

echo "📍 Chamber Location Analytics - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Generate sample data
echo "Generating sample data..."
python3 data_sources.py
echo "✓ Sample data created"
echo ""

# Create data directories
echo "Creating data directories..."
mkdir -p member_data
mkdir -p exports
mkdir -p logs
echo "✓ Directories created"
echo ""

# Success message
echo "=============================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run the dashboard:    streamlit run location_analytics_dashboard.py"
echo "2. Read the guide:       cat PLACER_ALTERNATIVE_GUIDE.md"
echo "3. Get API keys:"
echo "   - SafeGraph:          https://www.safegraph.com/"
echo "   - Census Bureau:      https://api.census.gov/data/key_signup.html"
echo ""
echo "For help: see README.md"
echo "=============================================="
