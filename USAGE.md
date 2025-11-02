# Mathematica to LaTeX Converter - Usage Guide

This tool converts Mathematica notebook files (.nb) to LaTeX documents with configurable display options.

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Set up your directory structure:**
```
homework-X/
├── config.yaml
├── notebooks/
│   ├── problem1.nb
│   ├── problem2.nb
│   └── ...
├── figures/      (auto-created for exported graphics)
└── latex/
    └── main.tex  (template)
```

2. **Create a configuration file** (`config.yaml`):
```yaml
homework:
  name: "Homework 8-1"
  title: "Variational Methods Problems"
  author: "Your Name"
  
problems:
  - file: "problem1.nb"
    name: "Problem 1"
    display: "output-only"
    description: "Brief description"
    
  - file: "problem2.nb"
    name: "Problem 2"
    display: "input-output"
    description: "Another problem"
```

3. **Run the conversion:**
```bash
python convert.py homework-8-1
```

4. **Compile the LaTeX output:**
```bash
cd homework-8-1/latex
pdflatex generated.tex
```

## Display Modes

Configure how each problem appears in the output using the `display` option:

### `output-only`
Shows only the results and outputs from Mathematica computations.
- Best for: Final answers, clean presentation
- Shows: Output cells, Print statements, results
- Hides: Input code

### `input-output`
Shows both Mathematica code and its results.
- Best for: Showing your work, tutorial-style documents
- Shows: Input code blocks, output cells
- Hides: Nothing (except intermediate metadata)

### `full`
Shows everything including intermediate steps and detailed formatting.
- Best for: Complete documentation, debugging
- Shows: All cells, all content

## Configuration File Reference

### Homework Section
```yaml
homework:
  name: "Homework X-Y"        # Short identifier
  title: "Full Title"         # Document title
  author: "Your Name"         # Author name
```

### Problems Section
```yaml
problems:
  - file: "notebook.nb"       # Filename in notebooks/ directory
    name: "Problem 1"         # Section heading in LaTeX
    display: "output-only"    # Display mode (see above)
    description: "Optional"   # Brief description (optional)
```

## Supported Mathematica Cell Types

The converter recognizes and processes these cell types:

- **Input cells**: Mathematica code (shown based on display mode)
- **Output cells**: Computation results
- **Text cells**: Documentation and explanations (always shown)
- **Print cells**: Print statement outputs

## Example Workflow

1. **Organize your notebooks:**
```bash
mkdir -p homework-8-1/notebooks
cp "HW 8-1 pb 4.nb" homework-8-1/notebooks/
cp "HW 8-1 pb 5.nb" homework-8-1/notebooks/
```

2. **Create configuration:**
```bash
cat > homework-8-1/config.yaml << EOF
homework:
  name: "Homework 8-1"
  title: "Quantum Mechanics Problems"
  author: "Bradley Taul"
  
problems:
  - file: "HW 8-1 pb 4.nb"
    name: "Problem 4"
    display: "output-only"
    
  - file: "HW 8-1 pb 5.nb"
    name: "Problem 5"
    display: "input-output"
EOF
```

3. **Run conversion:**
```bash
python convert.py homework-8-1
```

4. **Review and compile:**
```bash
cd homework-8-1/latex
cat generated.tex  # Review output
pdflatex generated.tex
pdflatex generated.tex  # Run twice for TOC
```

## Troubleshooting

### Problem: Notebook parsing errors
**Solution:** Check that your .nb files are valid Mathematica notebooks. Open them in Mathematica to verify.

### Problem: Missing output in LaTeX
**Solution:** Try changing the display mode to "input-output" or "full" to see more content.

### Problem: LaTeX compilation errors
**Solution:** Check generated.tex for special characters that need escaping. The converter handles basic cases but complex Unicode may need manual fixes.

### Problem: Graphics not appearing
**Solution:** Ensure the figures/ directory exists and has write permissions. Graphics extraction is a work in progress.

## Advanced Usage

### Custom LaTeX Template

Modify `homework-X/latex/main.tex` to customize:
- Document class and packages
- Page layout and margins
- Header and footer styles
- Code listing appearance

### Batch Processing

Process multiple homework sets:
```bash
for hw in homework-*; do
    python convert.py "$hw"
done
```

### Integration with Git

Add to `.gitignore`:
```
homework-*/figures/*.png
homework-*/figures/*.jpg
homework-*/latex/generated.tex
homework-*/latex/*.aux
homework-*/latex/*.log
homework-*/latex/*.pdf
```

## Tips for Best Results

1. **Use descriptive problem names** in the config file
2. **Add descriptions** to provide context for each problem
3. **Choose appropriate display modes** based on what you want to show
4. **Test with one problem first** before converting all problems
5. **Review the generated LaTeX** before final compilation
6. **Keep notebooks organized** in the notebooks/ directory

## Limitations

- Complex graphics may not export perfectly (manual review recommended)
- Some advanced Mathematica formatting may not convert exactly
- Unicode characters may need manual escaping in LaTeX
- Very large notebooks may take longer to process

## Getting Help

If you encounter issues:
1. Check the error messages in the console
2. Review the generated.tex file for clues
3. Try simplifying your notebooks
4. Verify all files are in the correct locations
