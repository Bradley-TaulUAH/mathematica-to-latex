#!/usr/bin/env python3
"""
Mathematica to LaTeX Converter

Converts Mathematica notebook files (.nb) to LaTeX format with improved document structure and formatting.
"""

import re
import argparse
import sys
import os
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
    r'\[Times]': r'\times ',
    r'\[PlusMinus]': r'\pm ',
    r'\[MinusPlus]': r'\mp ',
    r'\[LessEqual]': r'\leq ',
    r'\[GreaterEqual]': r'\geq ',
    r'\[NotEqual]': r'\neq ',
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
    text = re.sub(r'\\\\?\[Subscript\s+([^\]]+)\]', r'_{\1}', text)
    text = re.sub(r'(\w+)\\\\\\\\?\[Subscript\s+([^\]]+)\]', r'\1_{\2}', text)
    text = re.sub(r'Subscript\[([^,]+),\s*([^\]]+)\]', r'\1_{\2}', text)
    return text


def convert_superscripts(text):
    """Convert Mathematica superscript notation to LaTeX superscripts."""
    text = re.sub(r'Superscript\[([^,]+),\s*([^\]]+)\]', r'\1^{\2}', text)
    text = re.sub(r'Power\[([^,]+),\s*([^\]]+)\]', r'\1^{\2}', text)
    return text


def convert_symbols(text):
    """Convert Mathematica special symbols to LaTeX."""
    for math_symbol, latex_symbol in SYMBOL_MAP.items():
        text = text.replace(math_symbol, latex_symbol)
    
    # Handle \.b2 (subscript 2 notation)
    text = re.sub(r'\\\.b(\d)', r'^{\1}', text)
    
    # Handle special Unicode characters
    text = text.replace('≥', r'\geq ')
    text = text.replace('≤', r'\leq ')
    text = text.replace('±', r'\pm ')
    text = text.replace('×', r'\times ')
    text = text.replace('÷', r'\div ')
    text = text.replace('≠', r'\neq ')
    text = text.replace('∞', r'\infty')
    text = text.replace('∂', r'\partial')
    text = text.replace('∫', r'\int')
    text = text.replace('∑', r'\sum')
    text = text.replace('∏', r'\prod')
    text = text.replace('√', r'\sqrt')
    
    return text


def extract_graphics(text, output_dir):
    """Detect graphics from GraphicsBox structures."""
    graphics = []
    graphics_pattern = r'Cell\[GraphicsData\[|Cell\[.*?GraphicsBox\['
    matches = re.finditer(graphics_pattern, text, re.DOTALL)
    
    graphic_count = 0
    for match in matches:
        graphic_count += 1
        graphics.append(f"figure_{graphic_count}")
    
    return graphics


def extract_gridbox_table(text):
    """Extract table data from a GridBox structure."""
    gridbox_match = re.search(r'GridBox\[\{', text, re.DOTALL)
    if not gridbox_match:
        return None
    
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
    grid_content = re.sub(r'\\\n\s*', '', grid_content)
    
    rows = []
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
                row_content = grid_content[cell_start:i]
                cell_strings = re.findall(r'\\<\\"(.*?)\\"\\>', row_content, re.DOTALL)
                if cell_strings:
                    cells = []
                    for cell in cell_strings:
                        cell = cell.replace('\\n', '\n')
                        cell = cell.replace('\\"', '"')
                        cell = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', cell, flags=re.DOTALL)
                        cells.append(cell)
                    rows.append(cells)
        
        i += 1
    
    return rows if rows else None


def extract_string_content(text):
    """Extract content from string literals in Mathematica cells."""
    results = []
    matches = re.findall(r'\\<\\"(.*?)\\"\\>', text, re.DOTALL)
    for match in matches:
        content = match.replace('\\n', '\n')
        content = content.replace('\\"', '"')
        content = content.replace('\\\\', '\\')
        content = re.sub(r'\\\n\s*', '', content)
        content = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', content, flags=re.DOTALL)
        
        if content.strip() and content.strip() not in ['\\', '\n']:
            results.append(content)
    
    if results:
        return '\n'.join(results)
    
    return ''


def is_math_content(text):
    """Determine if text contains mathematical content that should be in math mode."""
    math_indicators = [
        r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon', r'\theta', 
        r'\lambda', r'\mu', r'\nu', r'\pi', r'\rho', r'\sigma', r'\tau', 
        r'\phi', r'\chi', r'\psi', r'\omega', r'\hbar', r'\times', r'\pm', 
        r'\geq', r'\leq', r'\bullet', r'\checkmark', r'\ddot', '_', '^'
    ]
    return any(indicator in text for indicator in math_indicators)


def fix_math_spacing(text):
    """Fix spacing issues in mathematical expressions."""
    greek_letters = [
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 
        'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi',
        'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 
        'psi', 'omega'
    ]
    
    for letter in greek_letters:
        text = re.sub(rf'(\\{letter})([a-z])', r'\1 \2', text)
    
    text = re.sub(r'\\sqrt([A-Za-z])', r'\\sqrt{\1}', text)
    return text


def clean_formbox_expressions(text):
    """Remove or simplify Mathematica FormBox expressions."""
    text = re.sub(r'\\\\!\\\\\\(\\\\\\*FormBox\[.*?TraditionalForm\]\\\\\\)', '[formula]', text, flags=re.DOTALL)
    text = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', text, flags=re.DOTALL)
    return text


def extract_input_code(cell_text):
    """Extract code from an Input cell."""
    code_parts = []
    matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', cell_text)
    for match in matches:
        if match in ['Input', 'Code', 'Bold', 'Italic'] or match.startswith('FontWeight'):
            continue
        if not match or match.isspace():
            continue
        cleaned = match.replace('\\n', '\n').replace('\\"', '"')
        cleaned = re.sub(r'\[IndentingNewLine\]', '\n', cleaned)
        cleaned = re.sub(r'\[?Continuation\]?', '', cleaned)
        cleaned = cleaned.replace('\\[', '[').replace('\\]', ']')
        cleaned = cleaned.replace('\\(', '(').replace('\\)', ')')
        
        if cleaned.strip():
            code_parts.append(cleaned)
    
    if code_parts:
        result = ' '.join(code_parts)
        result = re.sub(r' +', ' ', result)
        result = re.sub(r' *\n *', '\n', result)
        return result
    return ''


def process_cell_content(cell_text):
    """Process a single cell's content."""
    if '"Input"' in cell_text:
        code = extract_input_code(cell_text)
        if code:
            return ('INPUT', code)
        return ''
    
    if ('TagBox[' in cell_text and 'GraphicsBox[{' in cell_text and 'CompressedData[' in cell_text):
        return ('GRAPHIC', cell_text)
    
    table_data = extract_gridbox_table(cell_text)
    if table_data:
        return ('TABLE', table_data)
    
    content = extract_string_content(cell_text)
    
    if not content or len(content) < 3:
        return ''
    
    content = clean_formbox_expressions(content)
    content = convert_symbols(content)
    content = convert_subscripts(content)
    content = convert_superscripts(content)
    content = fix_math_spacing(content)
    
    content = re.sub(r'\\\$', '', content)
    content = re.sub(r'\\\s*$', '', content)
    content = re.sub(r'\\$', '', content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = re.sub(r'\n\n+', '\n\n', content)
    
    return content.strip()


def extract_cells_from_notebook(notebook_content):
    """Extract cells from a Mathematica notebook."""
    cells = []
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
                cell_content = '\n'.join(cell_lines)
                processed = process_cell_content(cell_content)
                if processed:
                    if isinstance(processed, tuple):
                        cells.append(processed)
                    elif isinstance(processed, str) and len(processed) > 3:
                        cells.append(processed)
                
                in_cell = False
                cell_lines = []
                bracket_count = 0
    
    return cells


def convert_notebook_to_latex(input_file, display_mode='both'):
    """Convert a Mathematica notebook to LaTeX with improved formatting.
    
    Args:
        input_file: Path to the Mathematica notebook file
        display_mode: 'input-only', 'output-only', or 'both' (default: 'both')
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    output_base = Path(input_file).stem
    figures_dir = f"{output_base}_figures"
    
    graphics_list = extract_graphics(content, figures_dir)
    cells = extract_cells_from_notebook(content)
    
    latex_output = []
    
    # Document preamble with better formatting
    latex_output.extend([
        r'\documentclass[11pt]{article}',
        r'\usepackage[margin=1in]{geometry}',
        r'\usepackage{amsmath}',
        r'\usepackage{amssymb}',
        r'\usepackage{graphicx}',
        r'\usepackage{array}',
        r'\usepackage{booktabs}',
        r'\usepackage{float}',
        r'\usepackage{listings}',
        r'\usepackage{xcolor}',
        r'\usepackage{parskip}',  # Better paragraph spacing
        r'\usepackage{titlesec}',  # Better section formatting
        r'',
        r'% Configure listings for Mathematica code',
        r'\lstset{',
        r'  language=Mathematica,',
        r'  basicstyle=\small\ttfamily,',
        r'  keywordstyle=\color{blue},',
        r'  commentstyle=\color{green!60!black},',
        r'  stringstyle=\color{red},',
        r'  numbers=none,',
        r'  frame=single,',
        r'  breaklines=true,',
        r'  backgroundcolor=\color{gray!10},',
        r'  captionpos=b,',
        r'  aboveskip=10pt,',
        r'  belowskip=10pt',
        r'}',
        r'',
        r'% Adjust section spacing',
        r'\titlespacing*{\section}{0pt}{12pt plus 4pt minus 2pt}{6pt plus 2pt minus 2pt}',
        r'\titlespacing*{\subsection}{0pt}{10pt plus 3pt minus 2pt}{4pt plus 2pt minus 2pt}',
        r'',
        r'\begin{document}',
        r''
    ])
    
    filename = Path(input_file).stem
    latex_output.extend([
        r'\title{' + filename.replace('_', r'\_') + '}',
        r'\date{\today}',
        r'\maketitle',
        r'',
        r'\bigskip',
        r''
    ])
    
    graphic_idx = 0
    current_paragraph = []
    section_counter = 0
    
    for cell in cells:
        # Handle input code cells
        if isinstance(cell, tuple) and cell[0] == 'INPUT':
            # Skip input cells if display_mode is 'output-only'
            if display_mode == 'output-only':
                continue
                
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if len(para_text) > 200:
                    # Break into smaller chunks for readability
                    sentences = para_text.split('. ')
                    for sent in sentences:
                        if sent.strip():
                            latex_output.append(sent.strip() + ('.' if not sent.endswith('.') else ''))
                else:
                    latex_output.append(para_text)
                latex_output.append(r'')
                latex_output.append(r'\medskip')
                latex_output.append(r'')
                current_paragraph = []
            
            code = cell[1]
            latex_output.extend([
                r'\noindent\textbf{Input:}',
                r'\begin{lstlisting}',
                code,
                r'\end{lstlisting}',
                r'',
                r'\medskip',
                r''
            ])
            continue
        
        # Handle graphic cells
        if isinstance(cell, tuple) and cell[0] == 'GRAPHIC':
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []
            
            if graphic_idx < len(graphics_list):
                graphic = graphics_list[graphic_idx]
                latex_output.extend([
                    r'\begin{figure}[H]',
                    r'\centering',
                    r'\fbox{\parbox{0.7\textwidth}{\centering\vspace{1cm}\textit{Figure placeholder: Export ' + graphic + r'.png from Mathematica}\vspace{1cm}}}',
                    r'% \includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphic + '.png}',
                    r'\caption{Figure ' + str(graphic_idx + 1) + '}',
                    r'\label{fig:' + str(graphic_idx + 1) + '}',
                    r'\end{figure}',
                    r'',
                    r'\medskip',
                    r''
                ])
                graphic_idx += 1
            continue
        
        # Handle table cells
        if isinstance(cell, tuple) and cell[0] == 'TABLE':
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []
            
            table_data = cell[1]
            if table_data:
                max_cols = max(len(row) for row in table_data)
                col_format = '|' + 'c|' * max_cols
                
                latex_output.extend([
                    r'\begin{table}[H]',
                    r'\centering',
                    r'\begin{tabular}{' + col_format + '}',
                    r'\hline'
                ])
                
                for i, row in enumerate(table_data):
                    converted_row = []
                    for cell_val in row:
                        cell_val = convert_symbols(cell_val)
                        cell_val = convert_subscripts(cell_val)
                        cell_val = convert_superscripts(cell_val)
                        cell_val = fix_math_spacing(cell_val)
                        if is_math_content(cell_val):
                            cell_val = f'${cell_val}$'
                        converted_row.append(cell_val)
                    
                    while len(converted_row) < max_cols:
                        converted_row.append('')
                    
                    latex_output.append(' & '.join(converted_row) + r' \\')
                    latex_output.append(r'\hline')
                
                latex_output.extend([
                    r'\end{tabular}',
                    r'\end{table}',
                    r'',
                    r'\medskip',
                    r''
                ])
            continue
        
        # Skip empty/formatting cells
        if cell in ['\\', '\n', '\\n', '', ' '] or (cell.startswith('\\') and len(cell) <= 2):
            continue
        
        # Skip output cells if display_mode is 'input-only'
        if display_mode == 'input-only':
            continue
        
        # Check if this is a heading
        is_heading = len(cell) < 80 and not any(word in cell.lower() for word in ['equation', 'where', 'using', 'for', 'with', 'the', 'and'])
        
        if is_heading and not is_math_content(cell):
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []
            
            section_counter += 1
            if len(cell) < 40:
                latex_output.extend([
                    r'',
                    r'\subsection*{' + cell + '}',
                    r''
                ])
            else:
                latex_output.extend([
                    r'',
                    r'\noindent\textbf{' + cell + '}',
                    r'',
                    r'\medskip',
                    r''
                ])
        else:
            # Regular content - add to paragraph
            if is_math_content(cell):
                if not (cell.startswith('$') or cell.startswith(r'\[') or '$' in cell):
                    cell = f'${cell}$'
            
            current_paragraph.append(cell)
            
            # Break paragraphs that get too long
            if len(current_paragraph) > 5:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                latex_output.append(r'\medskip')
                latex_output.append(r'')
                current_paragraph = []
    
    # Flush final paragraph
    if current_paragraph:
        latex_output.append(' '.join(current_paragraph))
        latex_output.append(r'')
    
    # Add graphics section if needed
    if len(graphics_list) > graphic_idx:
        latex_output.extend([
            r'',
            r'\section*{Additional Figures}',
            r'',
            r'The notebook contains ' + str(len(graphics_list)) + ' figures total.',
            r'To include them, export the graphics from Mathematica using:',
            r'',
            r'\begin{verbatim}',
            r'Export["figure_N.png", graphicsObject, ImageResolution -> 300]',
            r'\end{verbatim}',
            r'',
            r'Then place the PNG files in the ' + figures_dir + r'/ directory.',
            r''
        ])
        
        for i in range(graphic_idx, len(graphics_list)):
            latex_output.extend([
                r'\begin{figure}[H]',
                r'\centering',
                r'\fbox{\parbox{0.7\textwidth}{\centering\vspace{1cm}\textit{Figure ' + str(i+1) + r' placeholder}\vspace{1cm}}}',
                r'% \includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphics_list[i] + '.png}',
                r'\caption{Figure ' + str(i + 1) + '}',
                r'\label{fig:' + str(i + 1) + '}',
                r'\end{figure}',
                r''
            ])
    
    latex_output.append(r'\end{document}')
    
    return '\n'.join(latex_output)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Convert Mathematica notebook files to LaTeX format with improved structure'
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
    parser.add_argument(
        '--mode',
        choices=['input-only', 'output-only', 'both'],
        default='both',
        help='Display mode: "input-only" (code only), "output-only" (results only), or "both" (default: both)'
    )
    
    args = parser.parse_args()
    
    all_latex = []
    
    for input_file in args.input_files:
        if not Path(input_file).exists():
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Converting {input_file}...")
        latex_content = convert_notebook_to_latex(input_file, display_mode=args.mode)
        all_latex.append(latex_content)
    
    # Combine outputs
    if len(all_latex) > 1:
        combined = all_latex[0]
        for latex in all_latex[1:]:
            content_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', 
                                     latex, re.DOTALL)
            if content_match:
                combined = combined.replace(r'\end{document}', 
                                          '\n\n' + r'\newpage' + '\n\n' + 
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
    print(f"\nTo compile: pdflatex {output_file}")


if __name__ == '__main__':
    main()
