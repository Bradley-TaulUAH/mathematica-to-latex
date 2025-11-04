# Architecture

This document describes the architecture and design of the Mathematica to LaTeX converter.

## Overview

The converter is a single-file Python script (`mathematica_to_latex.py`) that transforms Mathematica notebook files (`.nb`) into LaTeX format. It uses only Python standard library components.

## Components

### Main Module (`mathematica_to_latex.py`)

**Key Functions:**

1. **Symbol Mapping (`SYMBOL_MAP`)**: A dictionary that maps Mathematica symbols to LaTeX equivalents
   - Greek letters (lowercase and uppercase)
   - Mathematical operators
   - Special symbols

2. **`convert_notebook(input_file)`**: Main conversion function
   - Reads the `.nb` file as plain text
   - Parses the notebook structure
   - Extracts cells and content
   - Applies symbol conversions
   - Formats output as LaTeX

3. **Text Processing**:
   - Subscript/superscript handling
   - Table extraction from GridBox structures
   - Graphics detection
   - Code block formatting
   - Section heading generation

4. **`main()`**: CLI entry point
   - Argument parsing
   - File I/O handling
   - Multi-file processing

## Data Flow

```
Input: .nb file(s)
    ↓
Read file content
    ↓
Parse Mathematica structure
    ↓
Extract cells (Input/Output/Text)
    ↓
Apply symbol conversions
    ↓
Format as LaTeX
    ↓
Generate document structure
    ↓
Output: .tex file
```

## Design Decisions

### Why Single File?
- Simplicity: Easy to distribute and use
- No dependencies: Works with standard Python
- Portability: Single file is easier to integrate

### Why Not Execute Code?
- Security: Mathematica code could be malicious
- Simplicity: Execution would require Mathematica installation
- Focus: Tool is for conversion, not computation

### Pattern Matching Approach
- Uses regex for symbol replacement
- Handles most common Mathematica patterns
- Trade-off: Not a full parser, but sufficient for most use cases

## Limitations

The converter uses text-based pattern matching rather than full AST parsing:
- Cannot handle all complex Mathematica expressions
- FormBox and other internal representations are simplified
- Some edge cases may require manual fixes

## Extension Points

Future contributors could enhance:

1. **Symbol coverage**: Add more Mathematica → LaTeX mappings in `SYMBOL_MAP`
2. **Cell types**: Better handling of different cell types
3. **Graphics**: Automatic graphics extraction (would require external tools)
4. **Tables**: More sophisticated table parsing
5. **Options**: Additional command-line options for customization

## Testing

Currently manual testing with example notebooks. Future improvements could include:
- Unit tests for symbol conversion
- Integration tests with known good conversions
- Regression tests for edge cases

## Dependencies

**Runtime**: None (Python 3.6+ standard library only)
- `re` - Regular expressions
- `argparse` - Command-line argument parsing
- `sys`, `os`, `pathlib` - File system operations
- `base64` - For handling embedded data (if needed)

**Development**:
- `setuptools` - For package distribution
- Standard Python development tools

## Performance

- File I/O is the primary bottleneck
- Processing is typically < 1 second for small notebooks
- Memory usage scales with input file size
- No streaming/chunking - entire file read into memory

## File Format

Mathematica `.nb` files are actually plain text with nested structures. The converter:
1. Reads as UTF-8 text
2. Uses regex to identify patterns
3. Converts patterns to LaTeX equivalents
4. Structures output with standard LaTeX document structure
