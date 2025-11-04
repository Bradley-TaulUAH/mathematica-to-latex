# Mathematica to LaTeX Converter

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

```bash
pdflatex output.tex
```

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
