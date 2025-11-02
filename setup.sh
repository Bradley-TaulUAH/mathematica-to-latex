#!/bin/bash
# Quick setup script for Mathematica to LaTeX converter

echo "🚀 Setting up Mathematica to LaTeX Converter..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "   Please install Python 3.7 or higher first"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run example to verify
echo ""
echo "🧪 Testing with example..."
python3 convert.py homework-8-1 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Setup complete! Everything is working."
else
    echo "⚠️  Setup complete but example test failed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ You're ready to go!"
echo ""
echo "Quick commands:"
echo "  • Try the example:  ./example.sh"
echo "  • Convert homework: python3 convert.py homework-8-1"
echo "  • Run tests:        python3 test_conversion.py"
echo ""
echo "See QUICKSTART.md for detailed usage instructions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
