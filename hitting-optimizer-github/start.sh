#!/bin/bash
# Quick Start Script for Enhanced Hitting Optimizer

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ENHANCED HITTING OPTIMIZER - WEB INTERFACE LAUNCHER      ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if requirements are installed
echo ""
echo "Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip install -r requirements.txt
fi

# Check if directories exist
echo ""
echo "Creating directories..."
mkdir -p ~/hitting_optimizer_uploads
mkdir -p ~/hitting_optimizer_results
echo "✓ Done"

# Start the server
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Starting Enhanced Hitting Optimizer Server         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Web Interface: http://localhost:5000"
echo ""
echo "Features:"
echo "  • Create athlete profiles (height/weight normalized)"
echo "  • Upload .mot files for analysis"
echo "  • Auto-scan Downloads folder for batch analysis"
echo "  • View detailed biomechanics metrics"
echo "  • Get AI-powered training recommendations"
echo "  • Track improvement over time"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
