# Mathematica to LaTeX Converter

This script converts Mathematica notebook files (`.nb`) to well-formatted LaTeX documents (`.tex`) that compile cleanly and look professional.

## Features

- **Improved Document Structure**: Proper sections, subsections, and paragraph spacing
- **Better Formatting**: Uses modern LaTeX packages for professional appearance
- **Symbol Conversion**: Converts Mathematica special symbols (Greek letters, operators) to LaTeX
- **Code Display**: Shows Mathematica input code in formatted listing blocks
- **Display Modes**: Choose to show input code only, output only, or both
- **Table Support**: Extracts and formats GridBox tables
- **Graphics Placeholders**: Detects graphics and provides clear instructions for exporting them
- **Multi-Document Support**: Combine multiple notebooks into a single PDF

## Installation

No installation required beyond Python 3. The script uses only standard library modules.

For LaTeX compilation, you'll need a LaTeX distribution:
- **Linux**: `sudo apt-get install texlive-latex-base texlive-latex-extra`
- **macOS**: Install MacTeX from https://www.tug.org/mactex/
- **Windows**: Install MiKTeX from https://miktex.org/

## Usage

### Basic Usage (Single Notebook)

```bash
python3 mathematica_to_latex.py "notebook.nb" -o output.tex
```

### Multiple Notebooks (Combined Document)

```bash
python3 mathematica_to_latex.py "problem1.nb" "problem2.nb" "problem3.nb" -o combined.tex
```

### Display Mode Options

Control what gets included in the output:

```bash
# Show only Mathematica input code (no results)
python3 mathematica_to_latex.py "notebook.nb" -o output.tex --mode input-only

# Show only results/output (no code)
python3 mathematica_to_latex.py "notebook.nb" -o output.tex --mode output-only

# Show both input code and results (default)
python3 mathematica_to_latex.py "notebook.nb" -o output.tex --mode both
```

### Automatic Graphics Extraction (with Wolfram Engine)

If you have Wolfram Engine installed, you can automatically extract graphics:

```bash
# Automatically extract graphics during conversion
python3 mathematica_to_latex.py "notebook.nb" -o output.tex --auto-extract-graphics
```

This will:
- Detect all graphics in the notebook
- Use Wolfram Engine to export them as PNG files
- Include them directly in the LaTeX output (no manual export needed!)
- Fall back to placeholders if Wolfram Engine is not available

**Benefits for repository users:** If you run the conversion with `--auto-extract-graphics` and commit the generated PNG files, other users can compile the LaTeX without needing Wolfram Engine themselves.

### Compile to PDF

```bash
pdflatex output.tex
```

## Example

```bash
# Convert a single notebook
python3 mathematica_to_latex.py "HW 8-1 pb 8.nb" -o hw8_problem8.tex

# Compile to PDF
pdflatex hw8_problem8.tex

# Combine multiple notebooks
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o homework8.tex
pdflatex homework8.tex
```

## What Gets Converted

- **Input Code**: Mathematica code is displayed in formatted code blocks
- **Output Text**: Print statements and output cells are converted to paragraphs
- **Tables**: GridBox tables are converted to LaTeX tabular environments
- **Mathematical Expressions**: Mathematica symbols are converted to LaTeX math notation
- **Graphics**: Placeholder frames are created with instructions for exporting figures

## Graphics Handling

Mathematica notebook files (`.nb`) store graphics as compressed binary data. This script provides two ways to handle graphics:

### Option 1: Automatic Extraction (Recommended - Requires Wolfram Engine)

If you have Wolfram Engine installed, use the `--auto-extract-graphics` flag:

```bash
python3 mathematica_to_latex.py "notebook.nb" -o output.tex --auto-extract-graphics
```

**What happens:**
1. Script detects all graphics in the notebook
2. Uses Wolfram Engine to automatically extract them as PNG files
3. Graphics are saved to the figures directory (e.g., `HW_8-1_pb_4_figures/`)
4. LaTeX code directly references the extracted images
5. PDF compiles with all graphics included!

**For repository maintainers:** Run the conversion with `--auto-extract-graphics` once and commit both the `.tex` file and the generated PNG files. Other users can then compile the LaTeX without needing Wolfram Engine.

### Option 2: Manual Export (No Wolfram Engine Required)

If Wolfram Engine is not available, the script creates visible placeholder frames:

1. Convert the notebook (placeholders will be created automatically)
2. Export graphics manually from Mathematica:
   ```mathematica
   Export["figure_1.png", graphicsObject, ImageResolution -> 300]
   ```
3. Place PNG files in the figures directory (e.g., `HW_8-1_pb_4_figures/`)
4. Uncomment the `\includegraphics` lines in the `.tex` file
5. Recompile the LaTeX document

**Batch export from Mathematica:**
```mathematica
(* Get all graphics from the current notebook *)
graphics = Cases[NotebookGet[EvaluationNotebook[]], _Graphics | _Graphics3D, Infinity];
Do[Export["figure_" <> ToString[i] <> ".png", graphics[[i]], ImageResolution -> 300], {i, Length[graphics]}]
```

## Document Structure

The generated LaTeX follows a professional academic paper style:

- **Document class**: `letterpaper, 12pt` for standard US letter format
- **Packages**: `tabularx`, `amsmath`, `graphicx`, `cite`, `hyperref`, `bm`, `float`
- **Hyperlinks**: Colored links (blue for internal/citations, magenta for files)
- **Title**: Bold formatting with italic author attribution
- **Structure**: Uses `\section{}` and `\paragraph{}` for organization
- **Tables**: Bordered tables with proper alignment
- **Figures**: With captions and labels
- **Code listings**: Syntax-highlighted Mathematica code blocks

## Improvements Over Basic Conversion

This converter addresses common issues with raw Mathematica-to-LaTeX conversion:

1. **No More "Super Linear" Output**: Content is organized into proper sections and paragraphs, not just one long linear sequence
2. **Professional Academic Style**: Uses standard 12pt letterpaper format with proper sectioning
3. **Proper Document Structure**: `\section{}` and `\paragraph{}` for clear hierarchy
4. **Symbol Translation**: Greek letters and mathematical operators are correctly converted
5. **Readable Tables**: Tables with borders and proper alignment
6. **Visible Figure Placeholders**: Graphics locations are clearly marked with frames
7. **Hyperlinked PDF**: Internal links, citations, and URLs are properly hyperlinked

## Limitations

- Complex Mathematica graphics cannot be directly extracted (manual export required)
- FormBox expressions are replaced with `[formula]` placeholders
- Very complex nested structures may need manual review

## Troubleshooting

### LaTeX Won't Compile

- Make sure you have all required LaTeX packages installed
- Check the `.log` file for specific errors
- Verify the `.tex` file doesn't have unmatched braces

### Missing Graphics

- The script creates placeholders; you must export graphics manually from Mathematica
- Follow the instructions in the generated `.tex` file comments

### Symbols Not Converting

- Some rare Mathematica symbols may not be in the conversion dictionary
- You can manually edit the `.tex` file to fix these cases

## License

This tool is provided as-is for educational and research purposes.
