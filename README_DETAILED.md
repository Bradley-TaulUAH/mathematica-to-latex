# Mathematica to LaTeX Converter - Detailed Guide

A comprehensive, professional tool for converting Mathematica notebook files (.nb) to high-quality LaTeX documents. Features an easy-to-use desktop GUI and powerful command-line interface with advanced formatting capabilities.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start Guide](#quick-start-guide)
5. [Desktop GUI Usage](#desktop-gui-usage)
6. [Command-Line Usage](#command-line-usage)
7. [Display Modes Explained](#display-modes-explained)
8. [Graphics Extraction](#graphics-extraction)
9. [Symbol Translation](#symbol-translation)
10. [Advanced Features](#advanced-features)
11. [Output Structure](#output-structure)
12. [Troubleshooting](#troubleshooting)
13. [Examples](#examples)
14. [Project Structure](#project-structure)

---

## Overview

This tool converts Mathematica notebook files (.nb) into professional LaTeX documents suitable for academic papers, homework submissions, and technical reports. It intelligently parses Mathematica's complex notebook structure and produces clean, compilable LaTeX code with proper formatting.

### What Does It Do?

- **Extracts content** from Mathematica notebooks (code, output, text, tables, graphics)
- **Converts symbols** (Greek letters, mathematical operators, special characters)
- **Formats code** with syntax highlighting in LaTeX listings
- **Creates tables** from Mathematica GridBox structures
- **Extracts graphics** automatically (with Wolfram Engine)
- **Generates professional LaTeX** with proper document structure

---

## Features

### Conversion Features

✅ **Professional LaTeX Output**
- Complete document structure with preamble, title, sections
- Proper use of LaTeX packages (amsmath, graphicx, listings, etc.)
- Academic paper formatting (12pt, letterpaper, 1-inch margins)

✅ **Display Mode Control**
- **Input-only**: Show only Mathematica code (for code documentation)
- **Output-only**: Show only results (for clean reports)
- **Both**: Show both code and results (for homework/tutorials)

✅ **Symbol Translation (50+ symbols)**
- Greek letters: α, β, γ, δ, ε, π, ψ, ω, etc.
- Operators: ≤, ≥, ≠, ±, ×, ÷, etc.
- Special: ∞, ∫, ∑, ∏, ∂, ℏ, etc.
- Auto-converts: `\[Alpha]` → `\alpha`, `\[Infinity]` → `\infty`

✅ **Automatic Graphics Extraction**
- Uses Wolfram Engine to extract plots and graphics
- Exports as high-resolution PNG files (300 DPI)
- Automatically includes in LaTeX with proper figure environments
- Falls back to placeholders if Wolfram Engine unavailable

✅ **Table Formatting**
- Converts GridBox structures to LaTeX tabular
- Preserves table structure and alignment
- Handles nested cell content

✅ **Code Listings**
- Syntax-highlighted Mathematica code
- Proper escaping of special characters
- Line breaking and formatting
- Distinguishes between input and output

✅ **Multi-Notebook Support**
- Combine multiple notebooks into one document
- Automatic page breaks between notebooks
- Preserves individual notebook sections

### GUI Features

🖥️ **Desktop Interface**
- Native popup window (tkinter)
- No web browser required
- File browser dialogs
- Real-time progress updates
- Visual progress bar

🎛️ **Control Options**
- Display mode selector (radio buttons)
- Graphics extraction toggle (checkbox)
- Output directory chooser
- Live status logging

---

## Installation

### Requirements

- **Python 3.7 or higher**
- **tkinter** (for desktop GUI - usually pre-installed)
- **Wolfram Engine** (optional - for automatic graphics extraction)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
cd mathematica-to-latex
```

### Step 2: Verify Python

```bash
python --version
# Should show Python 3.7 or higher
```

### Step 3: Check tkinter (Optional)

```bash
python -c "import tkinter; print('✓ tkinter is available')"
```

If tkinter is not available:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **Arch**: `sudo pacman -S tk`
- **Windows/macOS**: Usually pre-installed

### Step 4: Install Wolfram Engine (Optional)

For automatic graphics extraction, install Wolfram Engine:
1. Download from: https://www.wolfram.com/engine/
2. Follow installation instructions for your OS
3. Verify: `wolframscript --version`

**Note:** Graphics extraction is optional. Without Wolfram Engine, the converter will create placeholder boxes for graphics with instructions on how to export them manually.

---

## Quick Start Guide

### The Fastest Way to Convert

1. **Launch the GUI:**
   ```bash
   python run_gui.py
   ```
   or
   ```bash
   python mathematica_gui.py
   ```

2. **In the GUI window:**
   - Click "Browse..." to select your `.nb` file
   - Choose where to save the output
   - Select display mode (or keep default "Both")
   - Click "Convert to LaTeX"

3. **Compile the output:**
   ```bash
   pdflatex output.tex
   ```

That's it! You now have a professional LaTeX document.

---

## Desktop GUI Usage

### Starting the GUI

```bash
python mathematica_gui.py
```

or use the auto-launcher:

```bash
python run_gui.py
```

The auto-launcher will:
- Try to launch the desktop GUI first
- Fall back to web GUI if tkinter is unavailable
- Show helpful error messages if needed

### GUI Window Layout

```
┌─────────────────────────────────────────────────────┐
│   Mathematica to LaTeX Converter                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Input Mathematica Notebook (.nb):                  │
│  [________________________] [Browse...]              │
│                                                      │
│  Output Directory:                                   │
│  [________________________] [Browse...]              │
│                                                      │
│  Display Mode:                                       │
│  ◉ Input & Output Cells (Code + Results)            │
│  ○ Input Cells Only (Code)                          │
│  ○ Output Cells Only (Results)                      │
│                                                      │
│  ☑ Auto-extract graphics (requires Wolfram Engine)  │
│                                                      │
│         [Convert to LaTeX]  [Clear]                 │
│                                                      │
│  ====== Progress Bar ======                         │
│                                                      │
│  Status & Output:                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │ Starting conversion...                        │  │
│  │ ✓ Conversion completed successfully!         │  │
│  │ LaTeX output written to: output.tex          │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step GUI Instructions

#### Step 1: Select Input File
1. Click the **"Browse..."** button next to "Input Mathematica Notebook"
2. Navigate to your `.nb` file
3. Select the file and click "Open"
4. The file path will appear in the text box

#### Step 2: Choose Output Directory
1. Click the **"Browse..."** button next to "Output Directory"
2. Navigate to where you want to save the output
3. Click "Select Folder"
4. **Tip:** If you don't select a directory, it defaults to the same location as the input file

#### Step 3: Select Display Mode

**Input & Output Cells (Code + Results)** ⬅ *Recommended for homework/tutorials*
- Shows both Mathematica input cells (code) in highlighted boxes
- Shows output cells (results) below each code block
- Best for: Homework assignments, tutorials, documentation

**Input Cells Only (Code)**
- Shows only the Mathematica input cells (code)
- Hides all output cells and results
- Best for: Code documentation, sharing algorithms

**Output Cells Only (Results)**
- Shows only the output cells (results and computed output)
- Hides all input cells (code)
- Best for: Research papers, clean reports, publications

#### Step 4: Graphics Extraction (Optional)

Check the box **"Auto-extract graphics"** if:
- You have Wolfram Engine installed
- Your notebook contains plots or graphics
- You want automatic high-resolution exports

Leave unchecked if:
- You don't have Wolfram Engine
- No graphics in your notebook
- You'll export graphics manually

#### Step 5: Convert

1. Click **"Convert to LaTeX"**
2. Watch the progress bar animate
3. Read status updates in the output area
4. Wait for "✓ Conversion completed successfully!"

#### Step 6: Review Output

The status area shows:
- Input file being processed
- Display mode used
- Graphics extraction status
- Output file location
- File size
- Compilation command

Example output:
```
======================================================================
Starting conversion...
Input: /path/to/notebook.nb
Output Directory: /path/to/output
Display Mode: both
Auto-extract graphics: Yes
======================================================================

✓ Conversion completed successfully!

LaTeX output written to: /path/to/output/notebook.tex
File size: 15432 characters

To compile the LaTeX document:
  pdflatex notebook.tex

======================================================================
```

---

## Command-Line Usage

For automation, scripting, or advanced users.

### Basic Syntax

```bash
python mathematica_to_latex.py <input_file> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output <file>` | Output LaTeX filename | `<input_name>.tex` |
| `--mode <mode>` | Display mode: `input-only`, `output-only`, or `both` | `both` |
| `--auto-extract-graphics` | Extract graphics with Wolfram Engine | Disabled |

### Examples

#### Example 1: Basic Conversion

```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb"
```

Output: `HW 8-1 pb 4.tex` in the same directory

#### Example 2: Custom Output Location

```bash
python mathematica_to_latex.py "notebook.nb" -o ./output/homework.tex
```

Output: `./output/homework.tex`

#### Example 3: Output Only (Clean Report)

```bash
python mathematica_to_latex.py "analysis.nb" --mode output-only -o report.tex
```

Output: Clean LaTeX with only results, no code

#### Example 4: Input Only (Code Documentation)

```bash
python mathematica_to_latex.py "algorithm.nb" --mode input-only -o code.tex
```

Output: LaTeX with only code, no output

#### Example 5: With Graphics Extraction

```bash
python mathematica_to_latex.py "plots.nb" --auto-extract-graphics
```

Output: 
- `plots.tex` with included graphics
- `plots_figures/` directory with extracted PNG files

#### Example 6: Combine Multiple Notebooks

```bash
python mathematica_to_latex.py \
  "chapter1.nb" \
  "chapter2.nb" \
  "chapter3.nb" \
  -o complete_document.tex
```

Output: Single LaTeX document with all three notebooks, separated by `\newpage`

#### Example 7: Batch Processing Script

```bash
#!/bin/bash
# Convert all .nb files in current directory

for file in *.nb; do
    echo "Converting $file..."
    python mathematica_to_latex.py "$file" --mode both
done

echo "All conversions complete!"
```

---

## Display Modes Explained

### Mode: `both` (Default)

**Shows:** Code + Results

**Example Output:**
```latex
\noindent\textbf{Input:}
\begin{lstlisting}
Solve[x^2 - 5x + 6 == 0, x]
\end{lstlisting}

\paragraph{}
${{x \rightarrow 2}, {x \rightarrow 3}}$
```

**Compiled PDF shows:**
```
Input:
┌─────────────────────────────────┐
│ Solve[x^2 - 5x + 6 == 0, x]    │
└─────────────────────────────────┘

{{x → 2}, {x → 3}}
```

**Best for:**
- Homework submissions (show your work)
- Tutorials and teaching materials
- Documentation with examples
- Reproducible research

---

### Mode: `input-only`

**Shows:** Only Code

**Example Output:**
```latex
\noindent\textbf{Input:}
\begin{lstlisting}
Solve[x^2 - 5x + 6 == 0, x]
\end{lstlisting}
```

**Compiled PDF shows:**
```
Input:
┌─────────────────────────────────┐
│ Solve[x^2 - 5x + 6 == 0, x]    │
└─────────────────────────────────┘
```

**Best for:**
- Algorithm documentation
- Code listings
- Sharing computational methods
- Appendices with code

---

### Mode: `output-only`

**Shows:** Only Results

**Example Output:**
```latex
\paragraph{}
${{x \rightarrow 2}, {x \rightarrow 3}}$
```

**Compiled PDF shows:**
```
{{x → 2}, {x → 3}}
```

**Best for:**
- Research papers
- Clean reports
- Publications (no code clutter)
- Final results presentation

---

## Graphics Extraction

### Automatic Extraction (Requires Wolfram Engine)

When enabled, the converter:
1. Scans the notebook for Graphics and Graphics3D objects
2. Extracts each graphic from Output cells
3. Filters duplicate or incomplete graphics
4. Exports as high-resolution PNG (300 DPI)
5. Saves to `<notebook_name>_figures/` directory
6. Includes in LaTeX with `\includegraphics`

**Enable in GUI:** Check "Auto-extract graphics" checkbox

**Enable in CLI:** Add `--auto-extract-graphics` flag

**Example:**
```bash
python mathematica_to_latex.py "plots.nb" --auto-extract-graphics
```

**Output structure:**
```
plots.tex                    ← LaTeX document
plots_figures/               ← Graphics directory
├── figure_1.png            ← First graphic (300 DPI)
├── figure_2.png            ← Second graphic (300 DPI)
└── figure_3.png            ← Third graphic (300 DPI)
```

**LaTeX code generated:**
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{plots_figures/figure_1.png}
\caption{Figure 1}
\label{fig:1}
\end{figure}
```

### Manual Extraction (Without Wolfram Engine)

If Wolfram Engine is not available, the converter creates placeholder boxes:

**LaTeX code generated:**
```latex
\begin{figure}[H]
\centering
\fbox{\parbox{0.7\textwidth}{\centering\vspace{1cm}
\textit{Figure placeholder: Export figure_1.png from Mathematica}
\vspace{1cm}}}
% \includegraphics[width=0.7\textwidth]{plots_figures/figure_1.png}
\caption{Figure 1}
\label{fig:1}
\end{figure}
```

**To manually export graphics:**

1. Open your notebook in Mathematica
2. Find the graphic output cell
3. Right-click on the graphic
4. Select "Save Graphic As..."
5. Save as PNG with the name shown (e.g., `figure_1.png`)
6. Place in the `<notebook_name>_figures/` directory
7. Uncomment the `\includegraphics` line in the LaTeX file
8. Recompile with `pdflatex`

---

## Symbol Translation

The converter automatically translates 50+ Mathematica symbols to LaTeX.

### Greek Letters (Lowercase)

| Mathematica | LaTeX | Symbol |
|-------------|-------|--------|
| `\[Alpha]` | `\alpha` | α |
| `\[Beta]` | `\beta` | β |
| `\[Gamma]` | `\gamma` | γ |
| `\[Delta]` | `\delta` | δ |
| `\[Epsilon]` | `\epsilon` | ε |
| `\[Theta]` | `\theta` | θ |
| `\[Lambda]` | `\lambda` | λ |
| `\[Mu]` | `\mu` | μ |
| `\[Pi]` | `\pi` | π |
| `\[Sigma]` | `\sigma` | σ |
| `\[Phi]` | `\phi` | φ |
| `\[Psi]` | `\psi` | ψ |
| `\[Omega]` | `\omega` | ω |

### Greek Letters (Uppercase)

| Mathematica | LaTeX | Symbol |
|-------------|-------|--------|
| `\[CapitalDelta]` | `\Delta` | Δ |
| `\[CapitalGamma]` | `\Gamma` | Γ |
| `\[CapitalLambda]` | `\Lambda` | Λ |
| `\[CapitalPi]` | `\Pi` | Π |
| `\[CapitalSigma]` | `\Sigma` | Σ |
| `\[CapitalPhi]` | `\Phi` | Φ |
| `\[CapitalPsi]` | `\Psi` | Ψ |
| `\[CapitalOmega]` | `\Omega` | Ω |

### Mathematical Operators

| Mathematica | LaTeX | Symbol |
|-------------|-------|--------|
| `\[LessEqual]` | `\leq` | ≤ |
| `\[GreaterEqual]` | `\geq` | ≥ |
| `\[NotEqual]` | `\neq` | ≠ |
| `\[PlusMinus]` | `\pm` | ± |
| `\[Times]` | `\times` | × |
| `\[Element]` | `\in` | ∈ |
| `\[Subset]` | `\subset` | ⊂ |
| `\[Union]` | `\cup` | ∪ |
| `\[Intersection]` | `\cap` | ∩ |

### Special Symbols

| Mathematica | LaTeX | Symbol |
|-------------|-------|--------|
| `\[Infinity]` | `\infty` | ∞ |
| `\[Integral]` | `\int` | ∫ |
| `\[Sum]` | `\sum` | ∑ |
| `\[Product]` | `\prod` | ∏ |
| `\[PartialD]` | `\partial` | ∂ |
| `\[HBar]` | `\hbar` | ℏ |
| `\[RightArrow]` | `\rightarrow` | → |
| `\[LeftRightArrow]` | `\leftrightarrow` | ↔ |

### Subscripts and Superscripts

| Mathematica | LaTeX |
|-------------|-------|
| `Subscript[x, 1]` | `x_1` |
| `Superscript[x, 2]` | `x^2` |
| `Power[x, n]` | `x^n` |

---

## Advanced Features

### Multi-Notebook Conversion

Combine multiple notebooks into a single LaTeX document:

```bash
python mathematica_to_latex.py \
  "part1.nb" \
  "part2.nb" \
  "part3.nb" \
  -o complete.tex
```

**Result:**
- Single LaTeX file with all content
- Automatic `\newpage` between notebooks
- Individual titles preserved
- All graphics in separate directories

### Table Formatting

GridBox tables are automatically converted:

**Mathematica:**
```mathematica
Grid[{
  {"Name", "Value"},
  {"Alpha", 1.23},
  {"Beta", 4.56}
}]
```

**LaTeX Output:**
```latex
\begin{table}[H]
\centering
\begin{tabular}{|c|c|}
\hline
Name & Value \\
\hline
Alpha & 1.23 \\
\hline
Beta & 4.56 \\
\hline
\end{tabular}
\end{table}
```

### Code Listings with Syntax Highlighting

Input code is formatted with the `listings` package:

```latex
\lstset{
  language=Mathematica,
  basicstyle=\small\ttfamily,
  keywordstyle=\color{blue},
  commentstyle=\color{green!60!black},
  stringstyle=\color{red},
  numbers=none,
  frame=single,
  breaklines=true,
  backgroundcolor=\color{gray!10}
}
```

### Math Mode Auto-Detection

The converter automatically detects mathematical content and wraps it in `$...$`:

**Before:** `The value is \alpha x + \beta`

**After:** `The value is $\alpha x + \beta$`

---

## Output Structure

### Generated LaTeX Document Structure

```latex
\documentclass[letterpaper,12pt]{article}
\usepackage{tabularx}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[margin=1in,letterpaper]{geometry}
\usepackage{cite}
\usepackage[final]{hyperref}
\usepackage{bm}
\usepackage{float}
\usepackage{listings}
\usepackage{xcolor}

% Configure listings for Mathematica
\lstset{...}

\begin{document}

\title{\textbf{Notebook Title}}
\author{\textit{Generated from Mathematica Notebook}}
\date{}
\maketitle

% Content from notebook cells

\end{document}
```

### File Output Structure

After conversion, you'll have:

```
output-directory/
├── notebook.tex              ← Main LaTeX document
└── notebook_figures/         ← Graphics directory (if extracted)
    ├── figure_1.png
    ├── figure_2.png
    └── figure_3.png
```

---

## Troubleshooting

### Issue: GUI won't launch

**Error:** `ModuleNotFoundError: No module named 'tkinter'`

**Solution:**
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **Arch:** `sudo pacman -S tk`
- **Alternative:** Use web GUI: `python web_gui.py`

### Issue: No graphics extracted

**Error:** "Warning: Wolfram Engine not found"

**Solution:**
1. Install Wolfram Engine from https://www.wolfram.com/engine/
2. Verify installation: `wolframscript --version`
3. Re-run with `--auto-extract-graphics` flag
4. **Alternative:** Export graphics manually from Mathematica

### Issue: LaTeX won't compile

**Error:** Various LaTeX compilation errors

**Solutions:**
- **Missing packages:** Install full TeX distribution (TeX Live or MiKTeX)
- **Special characters:** Check for unescaped `&`, `%`, `$`, `_`, `{`, `}`
- **Missing graphics:** Ensure PNG files exist in `<notebook>_figures/` directory
- **Encoding issues:** Save LaTeX file as UTF-8

### Issue: Symbols not converting

**Problem:** Mathematica symbols appear as `\[Alpha]` instead of `α`

**Solution:**
- This is expected in code listings (preserved for accuracy)
- In output/results, symbols should convert automatically
- Check that you're using `--mode both` or `--mode output-only`

### Issue: Output file is empty or incomplete

**Problem:** Generated LaTeX file is very small or missing content

**Solutions:**
- Check that input file is a valid Mathematica notebook (`.nb`)
- Try opening the notebook in Mathematica first to verify it's not corrupted
- Check the status output for error messages
- Try with a simpler test notebook first

---

## Examples

### Example 1: Homework Assignment

**Goal:** Convert homework with both code and results

```bash
python mathematica_gui.py
```

In GUI:
- Select: `homework5.nb`
- Mode: **Both (Code + Results)**
- Graphics: **Enabled** (if you have plots)
- Click: **Convert to LaTeX**

**Result:** `homework5.tex` showing all work and solutions

**Compile:**
```bash
pdflatex homework5.tex
```

---

### Example 2: Research Paper

**Goal:** Clean output for publication, no code

```bash
python mathematica_to_latex.py "analysis.nb" --mode output-only -o paper.tex
```

**Result:** `paper.tex` with only results, no code clutter

Edit the generated file to:
- Add your name and affiliation
- Add abstract
- Add references
- Customize section titles

**Compile:**
```bash
pdflatex paper.tex
bibtex paper  # if you have references
pdflatex paper.tex
pdflatex paper.tex
```

---

### Example 3: Code Documentation

**Goal:** Document your algorithms

```bash
python mathematica_to_latex.py "algorithms.nb" --mode input-only -o appendix.tex
```

**Result:** `appendix.tex` with code listings only

Integrate into your main document:
```latex
\documentclass{article}
\begin{document}

% ... your main content ...

\appendix
\section{Source Code}
\input{appendix}

\end{document}
```

---

### Example 4: Batch Processing

**Goal:** Convert all notebooks in a directory

```bash
#!/bin/bash
# batch_convert.sh

for notebook in *.nb; do
    echo "Processing $notebook..."
    python mathematica_to_latex.py "$notebook" --mode both
    echo "✓ Done: ${notebook%.nb}.tex"
done

echo ""
echo "All conversions complete!"
echo "Compile with: pdflatex <filename>.tex"
```

Run:
```bash
chmod +x batch_convert.sh
./batch_convert.sh
```

---

## Project Structure

```
mathematica-to-latex/
│
├── mathematica_to_latex.py      # Advanced converter (877 lines)
│   ├── Symbol translation (50+ symbols)
│   ├── Graphics extraction (Wolfram Engine)
│   ├── Table formatting (GridBox → tabular)
│   ├── Code listings (syntax highlighting)
│   └── Multi-notebook support
│
├── mathematica_gui.py            # Desktop GUI (tkinter)
│   ├── File browser dialogs
│   ├── Display mode selector
│   ├── Graphics extraction toggle
│   ├── Real-time status updates
│   └── Progress indicator
│
├── mathematica_converter.py     # Simple converter (compatibility)
│   └── Basic conversion for simple use cases
│
├── run_gui.py                    # Auto-launcher
│   ├── Tries desktop GUI first
│   └── Falls back to web GUI
│
├── web_gui.py                    # Web interface (Flask)
│   ├── Browser-based UI
│   ├── Drag-and-drop upload
│   └── Download converted files
│
├── test_converter.py             # Test suite
│   └── Validates conversion accuracy
│
├── requirements.txt              # Python dependencies
│   └── flask, werkzeug (for web GUI only)
│
├── README.md                     # Basic documentation
├── README_DETAILED.md            # This file (comprehensive guide)
├── USAGE.md                      # Quick reference guide
│
├── templates/                    # Web GUI templates
│   └── index.html
│
├── HW 8-1 pb 4.nb               # Example notebook 1
├── HW 8-1 pb 5-all.nb           # Example notebook 2
└── HW 8-1 pb 8.nb               # Example notebook 3
```

---

## Tips and Best Practices

### For Best Results

1. **Clean your notebook first**
   - Remove unnecessary output cells
   - Clear old evaluations
   - Save before converting

2. **Use meaningful cell structure**
   - Group related code together
   - Add text cells for explanations
   - Use section headers

3. **Test with simple examples first**
   - Start with a small notebook
   - Verify the conversion works
   - Then move to larger documents

4. **Review and edit the output**
   - The converter provides a great starting point
   - Manual refinement may be needed
   - Customize titles, formatting, etc.

5. **Keep graphics organized**
   - Use descriptive names in Mathematica
   - Export at high resolution (300 DPI)
   - Check all graphics display correctly

### LaTeX Compilation Tips

1. **First compilation:**
   ```bash
   pdflatex document.tex
   ```

2. **If you have figures:**
   - Ensure PNG files exist in `<notebook>_figures/`
   - Check paths in LaTeX are correct

3. **If you have references:**
   ```bash
   pdflatex document.tex
   bibtex document
   pdflatex document.tex
   pdflatex document.tex
   ```

4. **For hyperlinks:**
   - The generated document includes hyperref
   - Internal links are colored blue
   - Compile twice for correct links

---

## Getting Help

### Common Questions

**Q: Can I convert Jupyter notebooks?**
A: No, this tool is specifically for Mathematica `.nb` files. For Jupyter, use `nbconvert`.

**Q: Will this work with old Mathematica versions?**
A: Yes, the `.nb` format is relatively stable across versions. Older notebooks should work fine.

**Q: Can I customize the LaTeX output?**
A: Yes! The generated `.tex` file is plain text. Edit it to customize formatting, add content, change styles, etc.

**Q: Does this work on Windows/Mac/Linux?**
A: Yes, it's pure Python and cross-platform. GUI works on all platforms with tkinter.

**Q: Can I integrate this into my workflow?**
A: Absolutely! Use the command-line interface in scripts, Makefiles, or CI/CD pipelines.

### Support

- **Issues:** Open an issue on GitHub
- **Questions:** Check existing issues or ask a new question
- **Contributions:** Pull requests welcome!

---

## License

This project is open source and available under the MIT License.

---

## Acknowledgments

- Integrates advanced conversion features from PR #3 and PR #4
- Built with Python standard library (minimal dependencies)
- Uses tkinter for cross-platform GUI
- Wolfram Engine integration for graphics extraction

---

## Version History

- **v2.0** - Integrated advanced converter with GUI
  - Professional LaTeX output
  - Display mode control
  - Graphics extraction
  - Enhanced GUI

- **v1.0** - Initial release
  - Basic conversion
  - Simple GUI

---

**Last Updated:** 2025-11-04

**Documentation Version:** 2.0

---

*For quick reference, see `USAGE.md`. For basic information, see `README.md`.*
