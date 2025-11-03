# Mathematica to LaTeX Converter

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
python3 mathematica_to_latex.py <input.nb> [output.tex]
```

### Examples

Convert a single notebook:
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 8.nb"
```

Specify output filename:
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" "homework4.tex"
```

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
- Title page with notebook filename
- Extracted content in order of appearance

## Limitations

- Code cells are not currently formatted (only comments are extracted)
- Graphics must be handled manually
- Some complex formatting may not be preserved
- Very large notebooks may take time to process

## Compiling the LaTeX

To compile the generated LaTeX file:

```bash
pdflatex output.tex
```

Or use Overleaf by uploading the `.tex` file directly.

## License

This script is provided as-is for converting Mathematica notebooks to LaTeX format.
