# Mathematica to LaTeX Converter

A Python script to convert Mathematica notebook files (.nb) to LaTeX format.

## Features

- Converts Mathematica notebooks to compilable LaTeX documents
- Translates Greek letters and special symbols to LaTeX commands
- Handles subscripts and superscripts
- Extracts and formats tables from GridBox structures
- Cleans up formatting issues and line breaks
- Supports multiple input files

## Installation

No installation required. Just Python 3.6+ is needed.

## Usage

### Convert a single notebook

```bash
python mathematica_to_latex.py "notebook.nb" -o output.tex
```

### Convert multiple notebooks into one document

```bash
python mathematica_to_latex.py "file1.nb" "file2.nb" "file3.nb" -o combined.tex
```

### Example with the provided notebooks

```bash
python mathematica_to_latex.py "HW 8-1 pb 8.nb" -o hw8-pb8.tex
```

## Symbol Conversions

The script automatically converts Mathematica symbols to LaTeX:

### Greek Letters
- `\[Alpha]` → `\alpha`
- `\[Beta]` → `\beta`
- `\[Pi]` → `\pi`
- `\[Sigma]` → `\sigma`
- `\[CapitalDelta]` → `\Delta`
- And many more...

### Special Symbols
- `\[HBar]` → `\hbar`
- `\[Times]` → `\times`
- `\[PlusMinus]` → `\pm`
- `\[GreaterEqual]` → `\geq`
- `\[Bullet]` → `\bullet`
- `\[Checkmark]` → `\checkmark`

### Subscripts and Superscripts
- `\\[Subscript 0]` → `_{0}`
- `\.b2` → `^{2}`

## Limitations

- **FormBox expressions**: Complex formatted expressions are replaced with `[formula]` placeholders as they contain Mathematica's internal formatting that's difficult to convert automatically
- **Code cells**: Input code cells are skipped, only output/Print cells are converted
- **Complex tables**: Some table structures may not convert perfectly
- **Manual review recommended**: Always review and potentially edit the generated LaTeX for best results

## Compiling the Output

The generated LaTeX can be compiled with standard LaTeX distributions:

```bash
pdflatex output.tex
```

Required LaTeX packages (automatically included in the output):
- amsmath
- amssymb
- graphicx
- array
- booktabs

## Known Issues

Some notebooks may have compilation warnings or errors that need manual fixing:
- Complex mathematical expressions in FormBox format are replaced with placeholders
- Some spacing around mathematical operators may need adjustment
- Variable names concatenated with Greek letters (e.g., `\alphax`) are automatically spaced

## Examples

### Input (Mathematica)
```
Print["Boundary conditions: \[Psi](\[PlusMinus]a) = 0"]
```

### Output (LaTeX)
```latex
$Boundary conditions: \psi(\pm a) = 0$
```

## License

This tool is provided as-is for educational and research purposes.

## Contributing

Feel free to submit issues or pull requests for improvements.
