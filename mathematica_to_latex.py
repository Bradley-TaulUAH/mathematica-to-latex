#!/usr/bin/env python3
"""
Mathematica to LaTeX Converter

Converts Mathematica notebook files (.nb) to LaTeX format with proper formatting.
"""

import re
import argparse
import sys
from pathlib import Path


# Mathematica symbol to LaTeX conversion dictionary
SYMBOL_MAP = {
    # Greek letters (lowercase)
    r'\[Alpha]': r'\alpha',
    r'\[Beta]': r'\beta',
    r'\[Gamma]': r'\gamma',
    r'\[Delta]': r'\delta',
    r'\[Epsilon]': r'\epsilon',
    r'\[Zeta]': r'\zeta',
    r'\[Eta]': r'\eta',
    r'\[Theta]': r'\theta',
    r'\[Iota]': r'\iota',
    r'\[Kappa]': r'\kappa',
    r'\[Lambda]': r'\lambda',
    r'\[Mu]': r'\mu',
    r'\[Nu]': r'\nu',
    r'\[Xi]': r'\xi',
    r'\[Omicron]': r'o',
    r'\[Pi]': r'\pi',
    r'\[Rho]': r'\rho',
    r'\[Sigma]': r'\sigma',
    r'\[Tau]': r'\tau',
    r'\[Upsilon]': r'\upsilon',
    r'\[Phi]': r'\phi',
    r'\[Chi]': r'\chi',
    r'\[Psi]': r'\psi',
    r'\[Omega]': r'\omega',
    
    # Greek letters (uppercase)
    r'\[CapitalAlpha]': r'A',
    r'\[CapitalBeta]': r'B',
    r'\[CapitalGamma]': r'\Gamma',
    r'\[CapitalDelta]': r'\Delta',
    r'\[CapitalEpsilon]': r'E',
    r'\[CapitalZeta]': r'Z',
    r'\[CapitalEta]': r'H',
    r'\[CapitalTheta]': r'\Theta',
    r'\[CapitalIota]': r'I',
    r'\[CapitalKappa]': r'K',
    r'\[CapitalLambda]': r'\Lambda',
    r'\[CapitalMu]': r'M',
    r'\[CapitalNu]': r'N',
    r'\[CapitalXi]': r'\Xi',
    r'\[CapitalOmicron]': r'O',
    r'\[CapitalPi]': r'\Pi',
    r'\[CapitalRho]': r'P',
    r'\[CapitalSigma]': r'\Sigma',
    r'\[CapitalTau]': r'T',
    r'\[CapitalUpsilon]': r'\Upsilon',
    r'\[CapitalPhi]': r'\Phi',
    r'\[CapitalChi]': r'X',
    r'\[CapitalPsi]': r'\Psi',
    r'\[CapitalOmega]': r'\Omega',
    
    # Special characters
    r'\[HBar]': r'\hbar',
    r'\[Bullet]': r'\bullet',
    r'\[Checkmark]': r'\checkmark',
    r'\[Times]': r'\times',
    r'\[PlusMinus]': r'\pm',
    r'\[MinusPlus]': r'\mp',
    r'\[LessEqual]': r'\leq',
    r'\[GreaterEqual]': r'\geq',
    r'\[NotEqual]': r'\neq',
    r'\[Infinity]': r'\infty',
    r'\[PartialD]': r'\partial',
    r'\[Integral]': r'\int',
    r'\[Sum]': r'\sum',
    r'\[Product]': r'\prod',
    r'\[Element]': r'\in',
    r'\[NotElement]': r'\notin',
    r'\[Subset]': r'\subset',
    r'\[Superset]': r'\supset',
    r'\[Union]': r'\cup',
    r'\[Intersection]': r'\cap',
    r'\[ForAll]': r'\forall',
    r'\[Exists]': r'\exists',
    r'\[RightArrow]': r'\rightarrow',
    r'\[LeftArrow]': r'\leftarrow',
    r'\[LeftRightArrow]': r'\leftrightarrow',
    r'\[Implies]': r'\Rightarrow',
    r'\[DoubleRightArrow]': r'\Rightarrow',
    r'\[DoubleLeftRightArrow]': r'\Leftrightarrow',
    r'\[Proportion]': r'\propto',
    r'\[Proportional]': r'\propto',
    r'\[EmptySet]': r'\emptyset',
    r'\[Perpendicular]': r'\perp',
    r'\[Parallel]': r'\parallel',
    r'\[Angle]': r'\angle',
    r'\[Degree]': r'^\circ',
    r'\[Sqrt]': r'\sqrt',
    
    # Diacritics
    r'\[ODoubleDot]': r'\ddot{o}',
    r'\[UDoubleDot]': r'\ddot{u}',
    r'\[ADoubleDot]': r'\ddot{a}',
    
    # Formatting
    r'\[IndentingNewLine]': '\n',
    r'\[NewLine]': '\n',
    r'\[InvisibleSpace]': '',
    r'\[NonBreakingSpace]': '~',
    r'\[ThinSpace]': r'\,',
    r'\[MediumSpace]': r'\:',
    r'\[ThickSpace]': r'\;',
    r'\[VeryThinSpace]': r'\!',
}


def convert_subscripts(text):
    """Convert Mathematica subscript notation to LaTeX subscripts."""
    # Pattern for escaped backslashes followed by [Subscript ...]
    # Example: r\\\\[Subscript 1] -> r_1
    text = re.sub(r'(\w+)\\\\\\\\?\[Subscript\s+([^\]]+)\]', r'\1_{\2}', text)
    
    # Pattern for Subscript[base, sub]
    text = re.sub(r'Subscript\[([^,]+),\s*([^\]]+)\]', r'\1_{\2}', text)
    
    return text


def convert_superscripts(text):
    """Convert Mathematica superscript notation to LaTeX superscripts."""
    # Pattern for Superscript[base, super]
    text = re.sub(r'Superscript\[([^,]+),\s*([^\]]+)\]', r'\1^{\2}', text)
    
    # Pattern for Power[base, exponent]
    text = re.sub(r'Power\[([^,]+),\s*([^\]]+)\]', r'\1^{\2}', text)
    
    return text


def convert_symbols(text):
    """Convert Mathematica special symbols to LaTeX."""
    for math_symbol, latex_symbol in SYMBOL_MAP.items():
        text = text.replace(math_symbol, latex_symbol)
    
    # Handle \.b2 (subscript 2 notation)
    text = re.sub(r'\\\.b(\d)', r'^{\1}', text)
    
    # Handle special Unicode characters
    text = text.replace('≥', r'\geq')
    text = text.replace('≤', r'\leq')
    text = text.replace('±', r'\pm')
    text = text.replace('×', r'\times')
    text = text.replace('÷', r'\div')
    text = text.replace('≠', r'\neq')
    text = text.replace('∞', r'\infty')
    text = text.replace('∂', r'\partial')
    text = text.replace('∫', r'\int')
    text = text.replace('∑', r'\sum')
    text = text.replace('∏', r'\prod')
    text = text.replace('√', r'\sqrt')
    
    return text


def extract_gridbox_table(text):
    """Extract table data from a GridBox structure."""
    # Look for GridBox[{ rows }]
    gridbox_match = re.search(r'GridBox\[\{', text, re.DOTALL)
    if not gridbox_match:
        return None
    
    # Find the matching closing bracket using stack-based parsing
    start_pos = gridbox_match.end()
    bracket_count = 1
    pos = start_pos
    
    while pos < len(text) and bracket_count > 0:
        if text[pos] == '{':
            bracket_count += 1
        elif text[pos] == '}':
            bracket_count -= 1
        pos += 1
    
    if bracket_count != 0:
        return None
    
    grid_content = text[start_pos:pos-1]
    
    # Now extract rows - split by comma at top level
    rows = []
    current_row = []
    bracket_count = 0
    cell_start = 0
    
    i = 0
    while i < len(grid_content):
        char = grid_content[i]
        
        if char == '{':
            if bracket_count == 0:
                cell_start = i + 1
            bracket_count += 1
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0:
                # End of a row
                row_content = grid_content[cell_start:i]
                
                # Extract all string literals from this row
                cell_strings = re.findall(r'\\<\\"(.*?)\\"\\>', row_content, re.DOTALL)
                if cell_strings:
                    cells = []
                    for cell in cell_strings:
                        cell = cell.replace('\\n', '\n')
                        cell = cell.replace('\\"', '"')
                        cells.append(cell)
                    rows.append(cells)
        
        i += 1
    
    return rows if rows else None


def extract_string_content(text):
    """Extract content from string literals in Mathematica cells."""
    results = []
    
    # Extract content between Mathematica string delimiters "\<\"...\"\>"
    # This is the format used in Print statements and output cells
    # In raw file: \<\"...\"\> but when read, becomes: \\<\\"...\\">\\>
    matches = re.findall(r'\\<\\"(.*?)\\"\\>', text, re.DOTALL)
    for match in matches:
        # Clean up escaped characters
        content = match.replace('\\n', '\n')
        content = content.replace('\\"', '"')
        content = content.replace('\\\\', '\\')
        
        # Remove line continuation backslashes (backslash followed by newline)
        content = re.sub(r'\\\n', ' ', content)
        
        # Skip if it's just whitespace or newlines
        if content.strip() and content.strip() not in ['\\', '\n']:
            results.append(content)
    
    if results:
        return '\n'.join(results)
    
    return ''


def is_math_content(text):
    """Determine if text contains mathematical content that should be in math mode."""
    # Check for LaTeX math symbols
    math_indicators = [
        r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon', r'\zeta', r'\eta', 
        r'\theta', r'\iota', r'\kappa', r'\lambda', r'\mu', r'\nu', r'\xi',
        r'\pi', r'\rho', r'\sigma', r'\tau', r'\upsilon', r'\phi', r'\chi', 
        r'\psi', r'\omega', r'\hbar', r'\times', r'\pm', r'\geq', r'\leq',
        '_', '^'
    ]
    
    return any(indicator in text for indicator in math_indicators)


def process_cell_content(cell_text):
    """Process a single cell's content."""
    # Check if this is a code cell (Input) - skip these
    if '"Input"' in cell_text:
        return ''
    
    # Check if this cell contains a GridBox (table)
    table_data = extract_gridbox_table(cell_text)
    if table_data:
        return ('TABLE', table_data)
    
    # Extract string content from Print cells and TextData cells
    content = extract_string_content(cell_text)
    
    if not content or len(content) < 3:
        return ''
    
    # Convert symbols
    content = convert_symbols(content)
    
    # Convert subscripts and superscripts
    content = convert_subscripts(content)
    content = convert_superscripts(content)
    
    # Clean up trailing backslashes and dollar signs
    content = re.sub(r'\\\$', '', content)
    content = re.sub(r'\\\s*$', '', content)  # Remove trailing backslash
    content = re.sub(r'\\$', '', content)
    
    # Clean up whitespace
    content = re.sub(r'[ \t]+', ' ', content)
    content = re.sub(r'\n\n+', '\n\n', content)
    
    return content.strip()


def extract_cells_from_notebook(notebook_content):
    """Extract cells from a Mathematica notebook."""
    cells = []
    
    # Split by Cell[ markers - handle nested structures
    # Look for Cell[BoxData[...]] or Cell[TextData[...]] or Cell["string", ...]
    lines = notebook_content.split('\n')
    in_cell = False
    cell_lines = []
    bracket_count = 0
    
    for line in lines:
        if line.startswith('Cell['):
            in_cell = True
            cell_lines = [line]
            bracket_count = line.count('[') - line.count(']')
        elif in_cell:
            cell_lines.append(line)
            bracket_count += line.count('[') - line.count(']')
            
            if bracket_count <= 0:
                # End of cell
                cell_content = '\n'.join(cell_lines)
                
                # Process the cell content
                processed = process_cell_content(cell_content)
                if processed:
                    # Could be a string or a tuple ('TABLE', data)
                    if isinstance(processed, tuple) and processed[0] == 'TABLE':
                        cells.append(processed)
                    elif isinstance(processed, str) and len(processed) > 3:
                        cells.append(processed)
                
                in_cell = False
                cell_lines = []
                bracket_count = 0
    
    return cells


def convert_notebook_to_latex(input_file):
    """Convert a Mathematica notebook to LaTeX."""
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract cells
    cells = extract_cells_from_notebook(content)
    
    # Build LaTeX document
    latex_output = []
    
    latex_output.append(r'\documentclass{article}')
    latex_output.append(r'\usepackage{amsmath}')
    latex_output.append(r'\usepackage{amssymb}')
    latex_output.append(r'\usepackage{graphicx}')
    latex_output.append(r'\usepackage{array}')
    latex_output.append(r'\usepackage{booktabs}')
    latex_output.append(r'')
    latex_output.append(r'\begin{document}')
    latex_output.append(r'')
    
    # Add title
    filename = Path(input_file).stem
    latex_output.append(r'\title{' + filename + '}')
    latex_output.append(r'\maketitle')
    latex_output.append(r'')
    
    # Add cells
    for cell in cells:
        # Handle table cells
        if isinstance(cell, tuple) and cell[0] == 'TABLE':
            table_data = cell[1]
            if table_data:
                # Determine number of columns
                max_cols = max(len(row) for row in table_data)
                col_format = 'l' * max_cols
                
                latex_output.append(r'\begin{center}')
                latex_output.append(r'\begin{tabular}{' + col_format + '}')
                latex_output.append(r'\hline')
                
                for i, row in enumerate(table_data):
                    # Convert symbols in cells
                    converted_row = []
                    for cell_val in row:
                        cell_val = convert_symbols(cell_val)
                        cell_val = convert_subscripts(cell_val)
                        cell_val = convert_superscripts(cell_val)
                        if is_math_content(cell_val):
                            cell_val = f'${cell_val}$'
                        converted_row.append(cell_val)
                    
                    # Pad row if needed
                    while len(converted_row) < max_cols:
                        converted_row.append('')
                    
                    latex_output.append(' & '.join(converted_row) + r' \\')
                    
                    # Add hline after header row
                    if i == 0:
                        latex_output.append(r'\hline')
                
                latex_output.append(r'\hline')
                latex_output.append(r'\end{tabular}')
                latex_output.append(r'\end{center}')
                latex_output.append(r'')
            continue
        
        # Skip cells that are just a single backslash or newline or empty
        if cell in ['\\', '\n', '\\n', '', ' ']:
            continue
        
        # Skip cells that start with backslash and are short (likely formatting artifacts)
        if cell.startswith('\\') and len(cell) <= 2:
            continue
        
        # Regular text or math content
        if is_math_content(cell):
            # Wrap in math mode if not already and contains inline math
            if not (cell.startswith('$') or cell.startswith(r'\[') or '$' in cell):
                cell = f'${cell}$'
        
        latex_output.append(cell)
        latex_output.append(r'')
    
    latex_output.append(r'\end{document}')
    
    return '\n'.join(latex_output)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Convert Mathematica notebook files to LaTeX format'
    )
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input Mathematica notebook file(s) (.nb)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output LaTeX file (default: derived from first input file)'
    )
    
    args = parser.parse_args()
    
    # Process each input file
    all_latex = []
    
    for input_file in args.input_files:
        if not Path(input_file).exists():
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Converting {input_file}...")
        latex_content = convert_notebook_to_latex(input_file)
        all_latex.append(latex_content)
    
    # Combine outputs
    if len(all_latex) > 1:
        # Merge multiple documents
        combined = all_latex[0]
        for latex in all_latex[1:]:
            # Extract content between \begin{document} and \end{document}
            content_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', 
                                     latex, re.DOTALL)
            if content_match:
                combined = combined.replace(r'\end{document}', 
                                          content_match.group(1) + r'\end{document}')
        final_latex = combined
    else:
        final_latex = all_latex[0]
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        output_file = Path(args.input_files[0]).stem + '.tex'
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_latex)
    
    print(f"LaTeX output written to {output_file}")


if __name__ == '__main__':
    main()
