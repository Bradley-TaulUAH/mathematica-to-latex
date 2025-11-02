# Mathematica to LaTeX Converter

Automated Python script that converts Mathematica notebook files (.nb) to LaTeX documents, with user control over display modes for each problem.

## ⚡ Easiest Way to Get Started

Just run these 2 commands:
```bash
./setup.sh          # One-time setup (installs dependencies)
./example.sh        # See it in action with example notebooks
```

📚 **[Quick Start Guide](QUICKSTART.md)** | 📖 **[Detailed Usage](USAGE.md)**

## Features

- **Configurable Display Modes**: Control whether to show input code, output, or both for each problem
- **Multiple Display Options**:
  - `output-only`: Show only results/output
  - `input-output`: Show both Mathematica code and results
  - `full`: Show everything including intermediate steps
- **Automatic Cell Extraction**: Parse Mathematica notebooks and extract Input, Output, Print, and Text cells
- **LaTeX Generation**: Convert extracted content to properly formatted LaTeX documents
- **Easy Configuration**: YAML-based configuration for homework assignments

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Organize your notebooks:**
```bash
mkdir -p homework-8-1/notebooks
cp "your-notebook.nb" homework-8-1/notebooks/
```

3. **Create configuration file** (`homework-8-1/config.yaml`):
```yaml
homework:
  name: "Homework 8-1"
  title: "Your Homework Title"
  author: "Your Name"
  
problems:
  - file: "your-notebook.nb"
    name: "Problem 1"
    display: "output-only"
    description: "Problem description"
```

4. **Run the converter:**
```bash
python convert.py homework-8-1
```

5. **Compile the LaTeX output:**
```bash
cd homework-8-1/latex
pdflatex generated.tex
```

## Directory Structure

```
mathematica-to-latex/
├── convert.py              # Main conversion script
├── requirements.txt        # Python dependencies
├── USAGE.md               # Detailed usage guide
├── README.md              # This file
└── homework-X/            # Example homework directory
    ├── config.yaml        # Configuration file
    ├── notebooks/         # Input: Mathematica notebooks
    │   └── *.nb
    ├── figures/           # Output: Extracted figures
    │   └── *.png
    └── latex/             # Output: LaTeX files
        ├── main.tex       # LaTeX template
        └── generated.tex  # Generated content
```

## Display Modes

### `output-only`
Shows only the results and outputs from Mathematica computations. Best for final answers and clean presentation.

### `input-output`
Shows both Mathematica code and its results. Best for showing your work and tutorial-style documents.

### `full`
Shows everything including intermediate steps and detailed formatting. Best for complete documentation.

## Documentation

For detailed usage instructions, see [USAGE.md](USAGE.md).

## Example

This repository includes an example conversion of Homework 8-1 with three problems demonstrating variational methods in quantum mechanics.

To run the example:
```bash
python convert.py homework-8-1
```

## Requirements

- Python 3.7+
- PyYAML
- SymPy
- Pillow

For LaTeX compilation:
- LaTeX distribution (TeX Live, MiKTeX, etc.)
- pdflatex

## How It Works

1. **Configuration Parsing**: Reads YAML configuration file specifying notebooks and display preferences
2. **Notebook Parsing**: Extracts cells from Mathematica .nb files
3. **Content Filtering**: Applies display mode to filter which cells to include
4. **LaTeX Conversion**: Converts Mathematica expressions and text to LaTeX format
5. **Document Generation**: Creates complete LaTeX document using template

## Limitations

- Complex graphics may not export perfectly (manual review recommended)
- Some advanced Mathematica formatting may not convert exactly
- Unicode characters may need manual escaping in LaTeX
- Very large notebooks may take longer to process

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - feel free to use and modify as needed.
