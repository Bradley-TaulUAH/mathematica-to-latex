#!/usr/bin/env python3
"""
Mathematica to LaTeX Converter

Converts Mathematica notebook files (.nb) to LaTeX format with improved document structure and formatting.
"""

import re
import argparse
import sys
import os
import subprocess
import shutil
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
    r'\[Superset]': r'\superset',
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


def check_wolfram_engine():
    """Check if Wolfram Engine is available on the system."""
    try:
        result = subprocess.run(['wolframscript', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def extract_graphics_with_wolfram(notebook_path, output_dir):
    """Extract graphics from a Mathematica notebook using Wolfram Engine.
    
    Args:
        notebook_path: Path to the .nb file
        output_dir: Directory to save extracted graphics
        
    Returns:
        List of extracted graphic filenames
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a Wolfram script to extract only top-level graphics from output cells
    # This avoids extracting intermediate graphics primitives
    wolfram_script = f'''
    nb = Import["{notebook_path}", "NB"];
    
    (* Method 1: Extract Output cells containing Graphics or GraphicsBox *)
    outputCells = Cases[nb, 
        Cell[BoxData[g_], "Output", ___] :> g, 
        Infinity
    ];
    
    (* Convert GraphicsBox to Graphics if needed *)
    graphics = {{}}; 
    Do[
        Which[
            MatchQ[cell, _Graphics | _Graphics3D],
                AppendTo[graphics, cell],
            MatchQ[cell, _GraphicsBox | _Graphics3DBox],
                Module[{{g = Quiet[ToExpression[cell]]}},
                    If[MatchQ[g, _Graphics | _Graphics3D], AppendTo[graphics, g]]
                ],
            True,
                (* Check if nested inside RowBox or other box structures *)
                Module[{{nested = Cases[cell, _Graphics | _Graphics3D, {{1, 2}}]}},
                    If[Length[nested] > 0, AppendTo[graphics, nested[[1]]]]
                ]
        ],
        {{cell, outputCells}}
    ];
    
    (* Filter to ensure we have valid, complete Graphics objects *)
    graphics = Select[graphics, 
        MatchQ[#, _Graphics | _Graphics3D] && 
        Length[#] > 1 &&  (* Ensure it's not just an empty Graphics object *)
        !FreeQ[#, _GraphicsComplex | _Line | _Point | _Polygon | _Circle] &  (* Has actual content *)
    ];
    
    (* Remove duplicates based on visual similarity (same dimensions/structure) *)
    graphics = DeleteDuplicatesBy[graphics, 
        Dimensions[#] &
    ];
    
    (* Export each graphic *)
    extracted = Table[
        Export[
            "{output_dir}/figure_" <> ToString[i] <> ".png",
            graphics[[i]],
            ImageResolution -> 300
        ],
        {{i, Length[graphics]}}
    ];
    
    Print["EXTRACTED:" <> ToString[Length[graphics]]];
    '''
    
    try:
        result = subprocess.run(
            ['wolframscript', '-code', wolfram_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Parse output to see how many graphics were extracted
        if result.returncode == 0:
            match = re.search(r'EXTRACTED:(\d+)', result.stdout)
            if match:
                count = int(match.group(1))
                return [f"figure_{i+1}.png" for i in range(count)]
        
        print(f"Warning: Wolfram Engine extraction failed: {result.stderr}", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("Warning: Wolfram Engine extraction timed out", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Warning: Error during graphics extraction: {e}", file=sys.stderr)
        return []


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
    """Extract code from an Input cell and escape for LaTeX listings."""
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
        
        # Remove Mathematica string delimiters like \< and \>
        cleaned = re.sub(r'\\<', '', cleaned)
        cleaned = re.sub(r'\\>', '', cleaned)
        
        # Clean up other Mathematica-specific escape sequences
        cleaned = cleaned.replace('\\`', '`')
        
        # Handle Unicode escape sequences like \:2080 (subscript 0 -> V_0)
        # Remove or convert these as they can cause LaTeX compilation issues
        # \:2080-\:2089 are subscript digits 0-9
        cleaned = re.sub(r'\\:2080', '_0', cleaned)  # subscript 0
        cleaned = re.sub(r'\\:2081', '_1', cleaned)  # subscript 1
        cleaned = re.sub(r'\\:2082', '_2', cleaned)  # subscript 2
        cleaned = re.sub(r'\\:2083', '_3', cleaned)  # subscript 3
        cleaned = re.sub(r'\\:2084', '_4', cleaned)  # subscript 4
        cleaned = re.sub(r'\\:2085', '_5', cleaned)  # subscript 5
        cleaned = re.sub(r'\\:2086', '_6', cleaned)  # subscript 6
        cleaned = re.sub(r'\\:2087', '_7', cleaned)  # subscript 7
        cleaned = re.sub(r'\\:2088', '_8', cleaned)  # subscript 8
        cleaned = re.sub(r'\\:2089', '_9', cleaned)  # subscript 9
        # Remove any other Unicode escapes that might cause issues
        cleaned = re.sub(r'\\:[0-9a-fA-F]{4}', '', cleaned)
        
        if cleaned.strip():
            code_parts.append(cleaned)
    
    if code_parts:
        result = ' '.join(code_parts)
        result = re.sub(r' +', ' ', result)
        result = re.sub(r' *\n *', '\n', result)
        
        # Final cleanup for listings environment
        # listings package handles most special chars, but we need to clean up the string markers
        result = re.sub(r'"\s*\+\s*"', '', result)  # Remove string concatenation markers
        
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


def convert_notebook_to_latex(input_file, display_mode='both', auto_extract_graphics=False):
    """Convert a Mathematica notebook to LaTeX with improved formatting.
    
    Args:
        input_file: Path to the Mathematica notebook file
        display_mode: 'input-only', 'output-only', or 'both' (default: 'both')
        auto_extract_graphics: If True, attempt to extract graphics using Wolfram Engine
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    output_base = Path(input_file).stem
    figures_dir = f"{output_base}_figures"
    
    graphics_list = extract_graphics(content, figures_dir)
    
    # Try to auto-extract graphics if requested and Wolfram Engine is available
    extracted_graphics = []
    if auto_extract_graphics and graphics_list:
        if check_wolfram_engine():
            print(f"  Extracting {len(graphics_list)} graphics using Wolfram Engine...")
            extracted_graphics = extract_graphics_with_wolfram(input_file, figures_dir)
            if extracted_graphics:
                print(f"  Successfully extracted {len(extracted_graphics)} graphics to {figures_dir}/")
        else:
            print("  Warning: Wolfram Engine not found. Graphics will be placeholders.", file=sys.stderr)
    
    cells = extract_cells_from_notebook(content)
    
    latex_output = []
    
    # Document preamble with enhanced packages for better visual presentation
    latex_output.extend([
        r'\documentclass[letterpaper,12pt]{article}',
        r'\usepackage{tabularx} % extra features for tabular environment',
        r'\usepackage{amsmath,amssymb,amsthm}  % improve math presentation',
        r'\usepackage{graphicx} % takes care of graphic including machinery',
        r'\usepackage[margin=1in,letterpaper]{geometry} % decreases margins',
        r'\usepackage{cite} % takes care of citations',
        r'\usepackage[final]{hyperref} % adds hyper links inside the generated pdf file',
        r'\hypersetup{',
        r'colorlinks=true,       % false: boxed links; true: colored links',
        r'linkcolor=blue,        % color of internal links',
        r'citecolor=blue,        % color of links to bibliography',
        r'filecolor=magenta,     % color of file links',
        r'urlcolor=blue',
        r'}',
        r'\usepackage{bm}',
        r'\usepackage{float}',
        r'\usepackage{listings}',
        r'\usepackage{xcolor}',
        r'\usepackage{booktabs} % professional quality tables',
        r'\usepackage{array} % improved array and tabular environments',
        r'\usepackage{fancyvrb} % fancy verbatim for better output display',
        r'\usepackage[most]{tcolorbox} % colored boxes for better output presentation',
        r'',
        r'%++++++++++++++++++++++++++++++++++++++++',
        r'% Custom styling for better visual appearance',
        r'%++++++++++++++++++++++++++++++++++++++++',
        r'',
        r'% Configure listings for Mathematica code with enhanced styling',
        r'\lstset{',
        r'  language=Mathematica,',
        r'  basicstyle=\small\ttfamily,',
        r'  keywordstyle=\color{blue}\bfseries,',
        r'  commentstyle=\color{green!60!black}\itshape,',
        r'  stringstyle=\color{red},',
        r'  numbers=none,',
        r'  frame=lines,',
        r'  framesep=3mm,',
        r'  breaklines=true,',
        r'  backgroundcolor=\color{blue!3},',
        r'  captionpos=b,',
        r'  aboveskip=12pt,',
        r'  belowskip=8pt,',
        r'  xleftmargin=8pt,',
        r'  xrightmargin=8pt',
        r'}',
        r'',
        r'% Define a custom environment for Mathematica output',
        r'\newtcolorbox{outputbox}{',
        r'  colback=yellow!5!white,',
        r'  colframe=orange!75!black,',
        r'  fonttitle=\bfseries,',
        r'  title=Output:,',
        r'  boxrule=0.5pt,',
        r'  arc=2mm,',
        r'  boxsep=3pt,',
        r'  left=6pt,',
        r'  right=6pt,',
        r'  top=6pt,',
        r'  bottom=6pt',
        r'}',
        r'',
        r'% Define environment for mathematical results',
        r'\newtcolorbox{resultbox}{',
        r'  colback=green!5!white,',
        r'  colframe=green!50!black,',
        r'  fonttitle=\bfseries,',
        r'  title=Result:,',
        r'  boxrule=0.5pt,',
        r'  arc=2mm,',
        r'  boxsep=3pt,',
        r'  left=6pt,',
        r'  right=6pt,',
        r'  top=6pt,',
        r'  bottom=6pt',
        r'}',
        r'',
        r'\begin{document}',
        r''
    ])
    
    filename = Path(input_file).stem
    latex_output.extend([
        r'\title{\textbf{' + filename.replace('_', r'\_') + '}}',
        r'\author{\textit{Generated from Mathematica Notebook}}',
        r'\date{}',
        r'',
        r'\maketitle',
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
                r'\vspace{6pt}',
                r'\noindent\textbf{\textcolor{blue!70!black}{Input:}}',
                r'\begin{lstlisting}',
                code,
                r'\end{lstlisting}',
                r'\vspace{4pt}',
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
                
                # Check if graphic was actually extracted
                graphic_file = Path(figures_dir) / f"{graphic}.png"
                if graphic_file.exists() or (graphic_idx < len(extracted_graphics)):
                    # Use actual extracted graphic
                    latex_output.extend([
                        r'\begin{figure}[H]',
                        r'\centering',
                        r'\includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphic + '.png}',
                        r'\caption{Figure ' + str(graphic_idx + 1) + '}',
                        r'\label{fig:' + str(graphic_idx + 1) + '}',
                        r'\end{figure}',
                        r'',
                        r'\medskip',
                        r''
                    ])
                else:
                    # Use placeholder
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
                col_format = 'c' * max_cols  # No vertical lines for booktabs style
                
                latex_output.extend([
                    r'\begin{table}[H]',
                    r'\centering',
                    r'\begin{tabular}{' + col_format + '}',
                    r'\toprule'  # Top rule from booktabs
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
                    # Add midrule after first row (header) only
                    if i == 0:
                        latex_output.append(r'\midrule')
                
                latex_output.extend([
                    r'\bottomrule',  # Bottom rule from booktabs
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
            # Determine section level based on content and position
            cell_lower = cell.lower()
            
            # Check if it's a major section (contains "problem", "part", etc.)
            is_major_section = any(keyword in cell_lower for keyword in ['problem', 'statement', 'lowest', 'comparison', 'analysis'])
            
            # Check if it's a subsection (contains (a), (b), (c), or part indicators)
            is_subsection = any(pattern in cell for pattern in ['(a)', '(b)', '(c)', '(d)', '(e)', '(i)', '(ii)', '(iii)']) or \
                           any(keyword in cell_lower for keyword in ['case', 'step', 'trial function', 'normalization', 'kinetic energy'])
            
            if len(cell) < 60:
                if is_subsection:
                    latex_output.extend([
                        r'\subsection{' + cell + '}',
                        r''
                    ])
                elif is_major_section and section_counter == 1:
                    # First major heading - make it unnumbered
                    latex_output.extend([
                        r'\section*{' + cell + '}',
                        r''
                    ])
                else:
                    latex_output.extend([
                        r'\section{' + cell + '}',
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
            # Regular content - wrap output in nice boxes
            if is_math_content(cell):
                # Mathematical output - use resultbox
                if not (cell.startswith('$') or cell.startswith(r'\[') or '$' in cell):
                    cell = f'${cell}$'
                
                # Flush any pending paragraph before adding result box
                if current_paragraph:
                    latex_output.append(' '.join(current_paragraph))
                    latex_output.append(r'')
                    latex_output.append(r'\medskip')
                    latex_output.append(r'')
                    current_paragraph = []
                
                latex_output.extend([
                    r'\begin{resultbox}',
                    cell,
                    r'\end{resultbox}',
                    r''
                ])
            else:
                # Text output - use outputbox for longer text, or just add to paragraph for short text
                if len(cell) > 50:  # Longer output gets a box
                    # Flush any pending paragraph
                    if current_paragraph:
                        latex_output.append(' '.join(current_paragraph))
                        latex_output.append(r'')
                        latex_output.append(r'\medskip')
                        latex_output.append(r'')
                        current_paragraph = []
                    
                    latex_output.extend([
                        r'\begin{outputbox}',
                        cell,
                        r'\end{outputbox}',
                        r''
                    ])
                else:
                    # Short text can be part of paragraph
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
        latex_output.append(r'\medskip')
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
            graphic_file = Path(figures_dir) / f"{graphics_list[i]}.png"
            if graphic_file.exists() or (i < len(extracted_graphics)):
                # Use actual extracted graphic
                latex_output.extend([
                    r'\begin{figure}[H]',
                    r'\centering',
                    r'\includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphics_list[i] + '.png}',
                    r'\caption{Figure ' + str(i + 1) + '}',
                    r'\label{fig:' + str(i + 1) + '}',
                    r'\end{figure}',
                    r''
                ])
            else:
                # Use placeholder
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
    parser.add_argument(
        '--auto-extract-graphics',
        action='store_true',
        help='Automatically extract graphics using Wolfram Engine (if available)'
    )
    
    args = parser.parse_args()
    
    all_latex = []
    
    for input_file in args.input_files:
        if not Path(input_file).exists():
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Converting {input_file}...")
        latex_content = convert_notebook_to_latex(
            input_file, 
            display_mode=args.mode,
            auto_extract_graphics=args.auto_extract_graphics
        )
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
