# Examples

This directory contains sample Mathematica notebook files and their converted LaTeX outputs.

## Files

- **`HW 8-1 pb 4.nb`** - Sample homework problem notebook
- **`HW 8-1 pb 5-all.nb`** - Comprehensive homework problem set
- **`HW 8-1 pb 8.nb`** - Another homework problem example
- **`HW_8-1_pb_8_output.tex`** - Converted LaTeX output (output only, no code)
- **`HW_8-1_pb_8_with_code.tex`** - Converted LaTeX with Mathematica code included
- **`example_output.tex`** - General example of converter output

## Usage

Try converting these examples:

```bash
# Basic conversion
python ../mathematica_to_latex.py "HW 8-1 pb 8.nb" -o test_output.tex

# Convert multiple files
python ../mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 8.nb" -o combined.tex
```

## Compiling

After conversion, compile the LaTeX files:

```bash
pdflatex HW_8-1_pb_8_output.tex
```

Make sure you have a LaTeX distribution installed (e.g., TeX Live, MiKTeX, or MacTeX).
