#!/bin/bash
# Convert all Mathematica notebooks in the current directory to LaTeX

echo "Converting Mathematica notebooks to LaTeX..."
echo

for nb in *.nb; do
    if [ -f "$nb" ]; then
        echo "Converting: $nb"
        python3 mathematica_to_latex.py "$nb"
        echo
    fi
done

echo "Done! LaTeX files generated."
echo
echo "To compile a LaTeX file:"
echo "  pdflatex <filename>.tex"
echo
echo "Or upload the .tex files to Overleaf for online compilation."
