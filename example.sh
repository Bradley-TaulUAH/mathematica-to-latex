#!/bin/bash
# Example demonstration of the Mathematica to LaTeX converter

echo "============================================================"
echo "Mathematica to LaTeX Converter - Example Demonstration"
echo "============================================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Check if dependencies are installed
echo "Step 1: Checking dependencies..."
if ! python3 -c "import yaml, sympy" 2>/dev/null; then
    echo "  Installing dependencies..."
    pip install -q -r requirements.txt
    echo "  ✓ Dependencies installed"
else
    echo "  ✓ Dependencies already installed"
fi
echo ""

# Show the configuration
echo "Step 2: Configuration (homework-8-1/config.yaml):"
echo "---"
cat homework-8-1/config.yaml
echo "---"
echo ""

# Run the conversion
echo "Step 3: Running conversion..."
python3 convert.py homework-8-1
echo ""

# Show results
if [ -f homework-8-1/latex/generated.tex ]; then
    echo "Step 4: Conversion Results:"
    echo "  ✓ Generated file: homework-8-1/latex/generated.tex"
    
    file_size=$(stat -f%z homework-8-1/latex/generated.tex 2>/dev/null || stat -c%s homework-8-1/latex/generated.tex 2>/dev/null)
    echo "  ✓ File size: ${file_size} bytes"
    
    # Count sections
    section_count=$(grep -c "\\\\section{" homework-8-1/latex/generated.tex)
    echo "  ✓ Problems converted: ${section_count}"
    
    echo ""
    echo "Step 5: Preview (first 20 lines of Problem 8):"
    echo "---"
    sed -n '/\\section{Problem 8}/,+20p' homework-8-1/latex/generated.tex
    echo "..."
    echo "---"
else
    echo "Error: Generated file not found"
    exit 1
fi

echo ""
echo "============================================================"
echo "Next Steps:"
echo "  1. Review the generated file: homework-8-1/latex/generated.tex"
echo "  2. Compile with: cd homework-8-1/latex && pdflatex generated.tex"
echo "  3. Modify config.yaml to customize display modes"
echo "  4. See USAGE.md for detailed instructions"
echo "============================================================"
