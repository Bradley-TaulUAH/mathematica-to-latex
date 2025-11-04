# Mathematica to LaTeX Converter

<<<<<<< HEAD
A Python script that converts Mathematica notebook (.nb) files to LaTeX format, extracting comments, code, output tables, and formatted text.

## Features

- **Parses Mathematica notebook structure**: Extracts content from `Cell[...]` expressions
- **Handles multiple cell types**: Input, Output, Print, and Text cells
- **Extracts comments**: Converts `(* comment *)` blocks to readable LaTeX text
- **Formats tables**: Converts GridBox outputs to LaTeX tabular environments
- **Greek letters and symbols**: Converts Mathematica notation like `\[Alpha]` to LaTeX `$\alpha$`
- **Unicode support**: Handles subscripts, superscripts, and special mathematical symbols
- **LaTeX special characters**: Properly escapes `&`, `%`, `$`, `_`, `{`, `}`, `#`, `^`, `~`, `\`

## Usage

```bash
python3 mathematica_to_latex.py <notebook1.nb> [notebook2.nb ...] [-o output.tex]
```

### Examples

Convert a single notebook:
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 8.nb"
```

Specify output filename:
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" -o "homework4.tex"
```

**Combine multiple notebooks into one document:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o combined.tex
```

When combining multiple notebooks, each notebook becomes a separate `\section{}` in the output document.

## Requirements

- Python 3.6 or higher
- No external dependencies required

## What Gets Extracted

### Comments
Mathematica comments in `(* ... *)` blocks are extracted and converted to plain text with proper LaTeX formatting.

### Tables
GridBox structures (tables) are converted to LaTeX `tabular` environments with proper formatting:

```latex
\begin{center}
\begin{tabular}{|c|c|}
\hline
Level & Energy \\
\hline
E1 & 6.7185 \\
\hline
\end{tabular}
\end{center}
```

### Greek Letters and Symbols
- `\[Alpha]` → `$\alpha$`
- `\[Beta]` → `$\beta$`
- `\[HBar]` → `$\hbar$`
- `\[Pi]` → `$\pi$`
- And many more...

### Unicode Subscripts and Superscripts
- Subscripts: `₀`, `₁`, `₂`, etc. → `$_0$`, `$_1$`, `$_2$`
- Superscripts: `²`, `³` → `$^2$`, `$^3$`

## What Gets Skipped

- Internal metadata (UUIDs, cache info, positions)
- Cell timing information
- Graphics/plots (documented separately)
- Raw notebook structure information

## Graphics and Plots

Graphics and plots are not automatically extracted. To include them in your LaTeX document:

1. In Mathematica, export plots manually using: `Export["plot.png", plot]`
2. Place the image files in the same directory as your LaTeX document
3. Manually add figure environments in the generated LaTeX:

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.8\textwidth]{plot.png}
  \caption{Your caption here}
  \label{fig:plot}
\end{figure}
```

## Testing

The script has been tested with three quantum mechanics notebooks:
- `HW 8-1 pb 4.nb` - Variational method calculations
- `HW 8-1 pb 5-all.nb` - Rayleigh-Ritz method with complex tables
- `HW 8-1 pb 8.nb` - Barrier in well with energy level tables

## Output Structure

The generated LaTeX document includes:
- Standard article document class
- Required packages: `amsmath`, `amssymb`, `listings`, `graphicx`, `float`
- Title page with notebook filename (single notebook) or "Combined Homework Problems" (multiple notebooks)
- Extracted content in order of appearance
- When combining multiple notebooks, each notebook becomes a separate `\section{}` with the filename as the section title

## Limitations

- Code cells are not currently formatted (only comments are extracted)
- Graphics must be handled manually
- Some complex formatting may not be preserved
- Very large notebooks may take time to process

## Compiling the LaTeX

To compile the generated LaTeX file:
=======
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/Bradley-TaulUAH/mathematica-to-latex)](https://github.com/Bradley-TaulUAH/mathematica-to-latex/issues)
[![GitHub stars](https://img.shields.io/github/stars/Bradley-TaulUAH/mathematica-to-latex)](https://github.com/Bradley-TaulUAH/mathematica-to-latex/stargazers)

A powerful Python tool that converts Wolfram Mathematica notebook files (`.nb`) into well-formatted LaTeX documents. Perfect for academic papers, reports, and documentation that need to include Mathematica computations.

## 📑 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Symbol Conversions](#symbol-conversions)
- [Limitations](#limitations--known-issues)
- [Compiling the Output](#compiling-the-output)
- [Working with Graphics](#working-with-graphics)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## ✨ Features

- 📝 **Complete Conversion**: Transforms Mathematica notebooks into compilable LaTeX documents
- 💻 **Code & Results**: Preserves both input code and output with proper formatting
- 🎨 **Smart Formatting**: Automatic section headings and improved readability
- 🖼️ **Graphics Handling**: Detects figures and provides export instructions
- 🔣 **Symbol Translation**: Comprehensive Greek letters and mathematical symbols conversion
- ⬆️⬇️ **Subscripts/Superscripts**: Proper handling of mathematical notation
- 📊 **Table Support**: Extracts and formats tables from GridBox structures
- 🔄 **Batch Processing**: Convert multiple notebooks into a single document
- 🧹 **Clean Output**: Removes formatting artifacts and normalizes line breaks

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher (no additional packages required)

### Installation

Clone this repository:

```bash
git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
cd mathematica-to-latex
```

### Basic Usage

**Convert a single notebook:**

```bash
python mathematica_to_latex.py "notebook.nb" -o output.tex
```

**Convert multiple notebooks into one document:**

```bash
python mathematica_to_latex.py "file1.nb" "file2.nb" "file3.nb" -o combined.tex
```

**Try with the provided examples:**

```bash
python mathematica_to_latex.py "examples/HW 8-1 pb 8.nb" -o output.tex
```

## 🔤 Symbol Conversions

The script automatically converts Mathematica notation to LaTeX equivalents:

| Type | Mathematica | LaTeX | Description |
|------|-------------|-------|-------------|
| Greek Letters | `\[Alpha]`, `\[Beta]`, `\[Gamma]` | `\alpha`, `\beta`, `\gamma` | All Greek letters supported |
| Capitals | `\[CapitalDelta]`, `\[CapitalPi]` | `\Delta`, `\Pi` | Greek capitals |
| Special | `\[HBar]`, `\[Times]`, `\[PlusMinus]` | `\hbar`, `\times`, `\pm` | Mathematical operators |
| Comparisons | `\[GreaterEqual]`, `\[LessEqual]` | `\geq`, `\leq` | Relational operators |
| Subscripts | `\[Subscript x, 0]` | `x_{0}` | Subscript notation |
| Superscripts | `\.b2` | `^{2}` | Superscript notation |

See the full list of conversions in the [comparison.md](comparison.md) file.

## ⚠️ Limitations & Known Issues

- **FormBox expressions**: Complex formatted expressions are replaced with `[formula]` placeholders
- **Graphics**: Graphics are detected but must be manually exported from Mathematica
- **Complex tables**: Some advanced table structures may need manual adjustment
- **Manual review**: Always review the generated LaTeX before final use

For detailed limitations, see the sections below.

## 📦 Compiling the Output

Compile the generated LaTeX with any standard LaTeX distribution:
>>>>>>> origin/main

```bash
pdflatex output.tex
```

<<<<<<< HEAD
Or use Overleaf by uploading the `.tex` file directly.

## License

This script is provided as-is for converting Mathematica notebooks to LaTeX format.
=======
**Required LaTeX packages** (automatically included in the output):
- `amsmath`, `amssymb` - Mathematical symbols and equations
- `graphicx` - Image inclusion
- `array`, `booktabs` - Table formatting
- `listings` - Code blocks with syntax highlighting
- `xcolor` - Color support

## 🖼️ Working with Graphics

The converter automatically detects graphics and adds placeholders. To include actual images:

1. **Export from Mathematica:**
   ```mathematica
   Export["figure_1.png", yourGraphicsObject, ImageResolution -> 300]
   ```

2. **Organize files:**
   - Create a figures directory (e.g., `notebook_figures/`)
   - Place exported PNG files there

3. **Compile:** The LaTeX document will reference these images automatically

## 📚 Examples

The `examples/` directory contains sample Mathematica notebooks and their converted LaTeX output. These demonstrate the converter's capabilities with real-world homework problems.

### Example Conversion

**Mathematica Input:**
```mathematica
Print["Boundary conditions: \[Psi](\[PlusMinus]a) = 0"]
```

**LaTeX Output:**
```latex
$Boundary conditions: \psi(\pm a) = 0$
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute
- Report bugs and request features via [GitHub Issues](https://github.com/Bradley-TaulUAH/mathematica-to-latex/issues)
- Submit pull requests for improvements
- Share example notebooks for testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for converting academic Mathematica notebooks to LaTeX
- Designed to handle physics and mathematics coursework
- Contributions and feedback welcome!

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Bradley-TaulUAH/mathematica-to-latex/issues)
- **Documentation**: See this README and example files
- **Questions**: Open a GitHub issue for help

---

**Note**: This is a utility tool for educational and research purposes. Always review and test the generated LaTeX before using it in production documents.
>>>>>>> origin/main
