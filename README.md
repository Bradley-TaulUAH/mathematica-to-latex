# Mathematica to LaTeX/Markdown Converter

A user-friendly GUI application for converting Mathematica notebook files (.nb) to LaTeX and Markdown formats.

## Features

- **Easy-to-use GUI**: Simple and intuitive graphical interface
- **Multiple output formats**: Convert to LaTeX, Markdown, or both simultaneously
- **Batch processing**: Process multiple files easily
- **Real-time feedback**: See conversion progress and results immediately
- **No external dependencies**: Uses only Python standard library

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
- Click "Browse..." to select your Mathematica notebook (.nb) file
- Choose the output directory (defaults to the same location as input file)
- Select the desired output format:
  - **LaTeX only**: Generates .tex file
  - **Markdown only**: Generates .md file  
  - **Both formats**: Generates both .tex and .md files
- Click "Convert" to start the conversion
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

### Command-Line Mode

For scripting or automation, you can use the command-line interface:

```bash
python mathematica_converter.py <input.nb> [output_format] [output_dir]
```

**Arguments:**
- `input.nb`: Path to the Mathematica notebook file (required)
- `output_format`: `latex`, `markdown`, or `both` (default: `both`)
- `output_dir`: Output directory (default: same as input file)

**Examples:**

Convert to both formats in the same directory:
```bash
python mathematica_converter.py "HW 8-1 pb 4.nb"
```

Convert to LaTeX only:
```bash
python mathematica_converter.py "HW 8-1 pb 4.nb" latex
```

Convert to Markdown in a specific directory:
```bash
python mathematica_converter.py "HW 8-1 pb 4.nb" markdown ./output
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
