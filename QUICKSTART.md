# Quick Start Guide

Get started with the Mathematica to LaTeX converter in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- Mathematica notebook files (.nb)
- (Optional) LaTeX distribution for PDF compilation

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

That's it! You're ready to go.

## Basic Usage

### 1. Prepare Your Notebooks

Create a homework directory and place your notebooks inside:

```bash
mkdir -p my-homework/notebooks
cp your-notebook-file.nb my-homework/notebooks/
```

### 2. Create Configuration File

Create `my-homework/config.yaml`:

```yaml
homework:
  name: "My Homework"
  title: "Problem Set Title"
  author: "Your Name"
  
problems:
  - file: "your-notebook-file.nb"
    name: "Problem 1"
    display: "output-only"
    description: "Brief description"
```

### 3. Create LaTeX Template

Copy the template from the example:

```bash
mkdir -p my-homework/latex
cp homework-8-1/latex/main.tex my-homework/latex/
```

### 4. Run Conversion

```bash
python convert.py my-homework
```

### 5. View Results

The generated LaTeX file will be at:
```
my-homework/latex/generated.tex
```

Compile it to PDF:
```bash
cd my-homework/latex
pdflatex generated.tex
```

## Display Modes Explained

Choose the appropriate display mode for each problem:

### `output-only` - Clean Results
- Shows: Only outputs and results
- Hides: Mathematica input code
- Best for: Final answer presentations

### `input-output` - Show Your Work
- Shows: Both code and outputs
- Best for: Tutorials, showing methodology

### `full` - Complete Documentation
- Shows: Everything including intermediate steps
- Best for: Complete problem documentation

## Example

Try the included example:

```bash
# Run the example demonstration
./example.sh

# Or run manually:
python convert.py homework-8-1
```

This converts three quantum mechanics problems demonstrating different display modes.

## Quick Tips

1. **Start simple**: Convert one notebook first to test
2. **Use meaningful names**: Give each problem a descriptive name
3. **Add descriptions**: They appear in the LaTeX output
4. **Review before compiling**: Check generated.tex before making PDF
5. **Iterate**: Adjust display modes and reconvert as needed

## Common Issues

### Problem: "Module 'yaml' not found"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Config file not found"
**Solution:** Make sure `config.yaml` is in your homework directory

### Problem: "No cells extracted"
**Solution:** Check that your .nb file is a valid Mathematica notebook

### Problem: LaTeX won't compile
**Solution:** Check generated.tex for special characters that need escaping

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed documentation
- Read [README.md](README.md) for complete overview
- Experiment with different display modes
- Customize the LaTeX template to your preferences

## Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Review [USAGE.md](USAGE.md) for troubleshooting
3. Verify your configuration file syntax
4. Try with a simpler notebook first

## Full Documentation

- [USAGE.md](USAGE.md) - Detailed usage guide
- [README.md](README.md) - Project overview
- [example.sh](example.sh) - Working example script

Happy converting!
