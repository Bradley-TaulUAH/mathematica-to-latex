# Usage Guide

## Desktop GUI (Popup Window)

When you run `python mathematica_gui.py` or `python run_gui.py`, a popup window appears with the following interface:

```
┌──────────────────────────────────────────────────────────────┐
│  🔄 Mathematica to LaTeX/Markdown Converter                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Input Mathematica Notebook (.nb):                          │
│  ┌────────────────────────────────────────┐  ┌─────────┐   │
│  │ /path/to/notebook.nb                   │  │ Browse..│   │
│  └────────────────────────────────────────┘  └─────────┘   │
│                                                              │
│  Output Directory:                                           │
│  ┌────────────────────────────────────────┐  ┌─────────┐   │
│  │ /path/to/output                        │  │ Browse..│   │
│  └────────────────────────────────────────┘  └─────────┘   │
│                                                              │
│  Output Format:                                              │
│  ( ) LaTeX only    ( ) Markdown only    (●) Both formats    │
│                                                              │
│                    ┌─────────┐  ┌───────┐                   │
│                    │ Convert │  │ Clear │                   │
│                    └─────────┘  └───────┘                   │
│                                                              │
│  [████████░░] Converting...                                  │
│                                                              │
│  Status:                                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Starting conversion...                                  │ │
│  │ Input: /path/to/notebook.nb                            │ │
│  │ Output Directory: /path/to/output                      │ │
│  │ Format: both                                           │ │
│  │ ────────────────────────────────────────────────────   │ │
│  │ Conversion successful!                                 │ │
│  │ LaTeX: /path/to/output/notebook.tex                    │ │
│  │ Markdown: /path/to/output/notebook.md                  │ │
│  │ ✓ Conversion completed successfully!                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Select a Mathematica notebook file (.nb), choose output    │
│  format, and click Convert.                                 │
└──────────────────────────────────────────────────────────────┘
```

## Step-by-Step Instructions

### 1. Launch the GUI
```bash
python mathematica_gui.py
```
or
```bash
python run_gui.py
```

A popup window will appear on your screen.

### 2. Select Input File
- Click the "Browse..." button next to "Input Mathematica Notebook"
- Navigate to your `.nb` file
- Select the file and click "Open"

The selected file path will appear in the text field.

### 3. Choose Output Directory (Optional)
- Click the "Browse..." button next to "Output Directory"
- Select where you want the converted files saved
- If not specified, files are saved in the same directory as the input file

### 4. Select Output Format
Choose one of three options:
- **LaTeX only**: Creates only a `.tex` file
- **Markdown only**: Creates only a `.md` file  
- **Both formats**: Creates both `.tex` and `.md` files (default)

### 5. Convert
- Click the "Convert" button
- A progress bar appears while converting
- Status messages appear in the status area
- When complete, you'll see success message with file locations

### 6. Find Your Files
The converted files will be in the output directory you specified:
- `filename.tex` - LaTeX version
- `filename.md` - Markdown version

## Command-Line Alternative

For quick conversions or scripting:

```bash
# Convert to both formats
python mathematica_converter.py "HW 8-1 pb 4.nb"

# Convert to LaTeX only
python mathematica_converter.py "HW 8-1 pb 4.nb" latex

# Convert to Markdown with custom output directory
python mathematica_converter.py "HW 8-1 pb 4.nb" markdown ./output
```

## Tips

- The GUI remembers your last output directory
- Large notebooks may take a few seconds to convert
- You can convert multiple files by running the conversion multiple times
- The converter handles complex mathematical notation automatically
- Generated LaTeX files are ready to compile with standard LaTeX compilers
- Generated Markdown files work with GitHub, GitLab, and most Markdown renderers

## Troubleshooting

**GUI doesn't appear:**
- Make sure Python 3.7+ is installed
- Install tkinter if needed (see README.md)
- Try the web GUI: `python web_gui.py`
- Try command-line: `python mathematica_converter.py`

**Conversion errors:**
- Ensure the file is a valid Mathematica notebook (.nb)
- Check that you have write permissions in the output directory
- Try a different output directory
- Check the status area for specific error messages

**Output doesn't look right:**
- The converter provides a good starting point but complex notebooks may need manual refinement
- Check the generated files with a text editor
- Mathematical notation should be preserved but may need adjustments
- Consider the limitations mentioned in README.md
