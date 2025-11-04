# Mathematica to LaTeX Converter

A comprehensive tool for converting Mathematica notebook files (.nb) to professional LaTeX documents, featuring both a desktop GUI and advanced command-line interface.

## Features

### Advanced Conversion Engine (Integrated from PR #3 & #4)
- **Professional LaTeX output**: Proper document structure with sections, paragraphs, tables, and figures
- **Display modes**: Choose "input-only" (code), "output-only" (results), or "both" (code + results)
- **Symbol translation**: 50+ Mathematica symbols automatically converted (Greek letters, operators, special characters)
- **Automatic graphics extraction**: Extract graphics using Wolfram Engine (when available)
- **Table formatting**: GridBox tables → LaTeX tabular environments
- **Code listings**: Syntax-highlighted Mathematica code blocks
- **Math mode handling**: Automatic detection and proper LaTeX math wrapping
- **Multi-notebook support**: Combine multiple notebooks into single document

### User-Friendly GUI
- **Desktop popup interface**: Native GUI with tkinter (no web browser needed)
- **File browser dialogs**: Easy file and directory selection
- **Display mode selector**: Radio buttons for input-only/output-only/both
- **Graphics toggle**: Enable/disable automatic graphics extraction
- **Real-time status**: Live progress updates in scrolling text area
- **Progress indicator**: Visual progress bar during conversion

## Requirements

- Python 3.7 or higher
- tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
cd mathematica-to-latex
```

2. Verify tkinter is available (optional):
```bash
python -c "import tkinter; print('tkinter is available')"
```

That's it! No external dependencies required for the GUI.

## Usage

### Quick Start

The easiest way to launch the GUI:

```bash
python run_gui.py
```

This will automatically launch the desktop GUI popup window (or fallback to web GUI if tkinter is not available).

### Desktop GUI Mode (Recommended)

To explicitly run the desktop GUI:

```bash
python mathematica_gui.py
```

In the GUI window:
- Click "Add Files..." to select one or more Mathematica notebook (.nb) files
  - Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple files
  - Multiple files will be combined into a single LaTeX document
- Choose the output directory (defaults to the same location as first input file)
- Select display mode:
  - **Input Cells Only**: Shows only code
  - **Output Cells Only**: Shows only results
  - **Input & Output Cells**: Shows both (recommended)
- Optionally enable "Auto-extract graphics" if you have Wolfram Engine installed
- Click "Convert to LaTeX" to start the conversion
- View the results in the status area at the bottom

**Note:** tkinter comes pre-installed with Python on Windows and macOS. On Linux, you may need to install it:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

### Web GUI Mode (Alternative)

If you prefer a web interface or tkinter is not available, you can use the web-based GUI:

1. Install Flask:
```bash
pip install flask werkzeug
```

2. Start the web server:
```bash
python web_gui.py
```

3. Open your browser to `http://localhost:5000`

### Command-Line Mode (Advanced Features)

For scripting, automation, or advanced features:

```bash
python mathematica_to_latex.py <input.nb> [options]
```

**Options:**
- `-o, --output <file>`: Output LaTeX file (default: derived from input)
- `--mode <mode>`: Display mode - `input-only`, `output-only`, or `both` (default: `both`)
- `--auto-extract-graphics`: Automatically extract graphics using Wolfram Engine

**Examples:**

Basic conversion:
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb"
```

Show only results (no code):
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb" --mode output-only -o results.tex
```

Convert with automatic graphics extraction:
```bash
python mathematica_to_latex.py "HW 8-1 pb 5-all.nb" --auto-extract-graphics
```

Combine multiple notebooks:
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o combined.tex
```

## How It Works

The converter:
1. Reads the Mathematica notebook file (.nb format)
2. Parses the notebook structure to extract cells and content
3. Converts Mathematica-specific syntax to LaTeX/Markdown equivalents
4. Handles common mathematical symbols and formatting
5. Outputs clean, readable LaTeX and/or Markdown files

## Supported Conversions

- Mathematical symbols (α, β, π, ∞, etc.)
- Mathematical operators (≤, ≥, ≠, ±, etc.)
- Integrals, sums, and other mathematical expressions
- Section headers and text formatting
- Code cells and comments

## Limitations

- The converter provides a good starting point but may require manual refinement for complex notebooks
- Very complex nested structures may not convert perfectly
- Some advanced Mathematica-specific features may not have direct LaTeX/Markdown equivalents

## Screenshot

### Desktop GUI Interface
The application provides a clean, easy-to-use popup window interface for converting Mathematica notebooks.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## Example Files

The repository includes example Mathematica notebooks:
- `HW 8-1 pb 4.nb` - Infinite square well variational calculation
- `HW 8-1 pb 5-all.nb` - Additional physics problems
- `HW 8-1 pb 8.nb` - More examples

You can use these files to test the converter.

## Development

### Project Structure

```
mathematica-to-latex/
├── mathematica_converter.py  # Core conversion logic
├── mathematica_gui.py         # GUI application
├── requirements.txt           # Python dependencies (none required)
├── README.md                  # This file
└── *.nb                       # Example Mathematica notebooks
```

### Running Tests

Test the converter with the example files:

```bash
# Test with GUI
python mathematica_gui.py

# Test command-line
python mathematica_converter.py "HW 8-1 pb 4.nb"
```
