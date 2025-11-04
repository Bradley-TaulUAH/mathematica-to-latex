#!/usr/bin/env python3
"""
<<<<<<< HEAD
Convert Mathematica notebooks (.nb files) to LaTeX format.

This script parses Mathematica notebook files and extracts:
- Comments from (* ... *) blocks
- Input code cells
- Print output cells with tables
- Text cells

It properly escapes LaTeX special characters and formats tables.
"""

import re
import sys
import os
from typing import List, Tuple, Optional, Dict


class MathematicaToLatexConverter:
    """Converter for Mathematica notebooks to LaTeX."""

    # Mapping of Mathematica Greek letters to LaTeX
    GREEK_LETTERS = {
        r'\[Alpha]': r'$\alpha$',
        r'\[Beta]': r'$\beta$',
        r'\[Gamma]': r'$\gamma$',
        r'\[Delta]': r'$\delta$',
        r'\[Epsilon]': r'$\epsilon$',
        r'\[Zeta]': r'$\zeta$',
        r'\[Eta]': r'$\eta$',
        r'\[Theta]': r'$\theta$',
        r'\[Iota]': r'$\iota$',
        r'\[Kappa]': r'$\kappa$',
        r'\[Lambda]': r'$\lambda$',
        r'\[Mu]': r'$\mu$',
        r'\[Nu]': r'$\nu$',
        r'\[Xi]': r'$\xi$',
        r'\[Omicron]': r'$o$',
        r'\[Pi]': r'$\pi$',
        r'\[Rho]': r'$\rho$',
        r'\[Sigma]': r'$\sigma$',
        r'\[Tau]': r'$\tau$',
        r'\[Upsilon]': r'$\upsilon$',
        r'\[Phi]': r'$\phi$',
        r'\[Chi]': r'$\chi$',
        r'\[Psi]': r'$\psi$',
        r'\[Omega]': r'$\omega$',
        r'\[HBar]': r'$\hbar$',
        r'\[Times]': r'$\times$',
    }

    # Unicode escapes
    UNICODE_ESCAPES = {
        '\u2080': r'$_0$',  # subscript 0
        '\u2081': r'$_1$',
        '\u2082': r'$_2$',
        '\u00b2': r'$^2$',  # superscript 2
        '\u00b3': r'$^3$',  # superscript 3
        '\u207a': r'$^+$',  # superscript plus
        '\u207b': r'$^-$',  # superscript minus
    }

    def __init__(self):
        pass

    def escape_latex_chars(self, text: str) -> str:
        """Escape special LaTeX characters."""
        # Don't escape if already in math mode
        if text.startswith('$') and text.endswith('$'):
            return text

        replacements = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
            ('^', r'\textasciicircum{}'),
        ]

        result = text
        for char, replacement in replacements:
            result = result.replace(char, replacement)
        return result

    def convert_greek_letters(self, text: str) -> str:
        """Convert Mathematica Greek letters to LaTeX."""
        result = text
        for math_letter, latex_letter in self.GREEK_LETTERS.items():
            result = result.replace(math_letter, latex_letter)
        return result

    def convert_unicode_escapes(self, text: str) -> str:
        """Convert Unicode characters and Mathematica unicode escapes to LaTeX."""
        result = text

        # Handle actual Unicode characters
        for unicode_char, latex_equiv in self.UNICODE_ESCAPES.items():
            result = result.replace(unicode_char, latex_equiv)

        # Handle Mathematica's \:XXXX format (hexadecimal Unicode escapes)
        # Common subscripts
        result = re.sub(r'\\:2080', r'$_0$', result)  # subscript 0
        result = re.sub(r'\\:2081', r'$_1$', result)  # subscript 1
        result = re.sub(r'\\:2082', r'$_2$', result)  # subscript 2
        result = re.sub(r'\\:2083', r'$_3$', result)  # subscript 3
        result = re.sub(r'\\:2084', r'$_4$', result)  # subscript 4

        # Common superscripts
        result = re.sub(r'\\:00b2', r'$^2$', result)  # superscript 2
        result = re.sub(r'\\:00b3', r'$^3$', result)  # superscript 3

        # Special brackets and symbols
        result = re.sub(r'\\:27e8', r'$\\langle$', result)  # left angle bracket
        result = re.sub(r'\\:27e9', r'$\\rangle$', result)  # right angle bracket
        result = re.sub(r'\\:1d62', r'$i$', result)  # mathematical italic i
        result = re.sub(r'\\:2c7c', r'$j$', result)  # mathematical italic j
        result = re.sub(r'\\\.bd', r'$\\hbar^2$', result)  # hbar squared
        result = re.sub(r'\\\.b2', r'$^2$', result)  # superscript 2

        # Center dot
        result = re.sub(r'\\\[CenterDot\]', r'$\\cdot$', result)
        result = re.sub(r'\\:22c5', r'$\\cdot$', result)

        # Arrows and other symbols
        result = re.sub(r'\\\[RightArrow\]', r'$\\rightarrow$', result)
        result = re.sub(r'\\:2192', r'$\\rightarrow$', result)

        # Integral sign
        result = re.sub(r'\\\[Integral\]', r'$\\int$', result)
        result = re.sub(r'\\:222b', r'$\\int$', result)

        # Infinity
        result = re.sub(r'\\\[Infinity\]', r'$\\infty$', result)

        # Plus/Minus
        result = re.sub(r'\\\[PlusMinus\]', r'$\\pm$', result)

        # Comparison operators
        result = re.sub(r'\\\[LessEqual\]', r'$\\leq$', result)
        result = re.sub(r'\\\[GreaterEqual\]', r'$\\geq$', result)
        result = re.sub(r'\\\[NotEqual\]', r'$\\neq$', result)
        result = re.sub(r'\\\[Equal\]', r'$=$', result)

        # Square root
        result = re.sub(r'\\\[Sqrt\]', r'$\\sqrt{}$', result)

        return result

    def extract_string_content(self, text: str) -> str:
        """Extract content from quoted strings in various Mathematica formats."""
        # The file contains patterns like "\\<content\\>" or "\<"content"\>"

        # Pattern 1: "\\<content\\>" (escaped backslashes in file)
        match = re.search(r'"\\\\<([^>]+)\\\\>"', text)
        if match:
            content = match.group(1)
            # Clean up any remaining escapes
            content = content.strip('"').strip('\\')
            return content

        # Pattern 2: "\<\"content\"\>" (with quotes inside)
        match = re.search(r'\\<\\"([^"]+)\\"\\>', text)
        if match:
            return match.group(1)

        # Pattern 3: Simple quoted string with possible inner backslash patterns
        match = re.search(r'"([^"]+)"', text)
        if match:
            content = match.group(1)
            # Try to clean up \< and \> if present
            content = re.sub(r'\\<\\', '', content)
            content = re.sub(r'\\\\>', '', content)
            content = re.sub(r'\\>', '', content)
            content = re.sub(r'\\<', '', content)
            content = content.strip('"').strip('\\')
            if content:
                return content

        return ""

    def clean_rowbox_content(self, content: str) -> str:
        """Extract readable text from RowBox structures."""
        # Extract text from quoted strings first
        strings = re.findall(r'"([^"]*)"', content)
        if strings:
            # Join strings with spaces, filtering out just separator markers
            filtered_strings = []
            for s in strings:
                # Skip pure separator strings
                if s.strip() in ['===', '=', '-', '*']:
                    continue
                filtered_strings.append(s)

            result = ' '.join(filtered_strings)
            return result

        # If no quoted strings, try to clean up the structure
        # Remove RowBox, brackets, etc.
        result = content
        result = re.sub(r'RowBox\[', '', result)
        result = re.sub(r'[{}\[\]]', ' ', result)
        result = re.sub(r',\s*', ' ', result)
        result = re.sub(r'\s+', ' ', result)
        result = result.strip()

        return result

    def extract_comments(self, content: str) -> List[str]:
        """Extract comments from (* ... *) blocks within RowBox structures."""
        comments = []

        # Find RowBox[{"(*", RowBox[{...}], "*)"}] patterns
        # Use a more flexible approach - find the comment markers and extract content between them

        # Split by "(*" and "*)" markers
        parts = content.split('"(*"')

        for i in range(1, len(parts)):  # Skip first part (before first comment)
            # Find the matching "*)"
            end_marker_pos = parts[i].find('"*)"')
            if end_marker_pos != -1:
                # Extract content between "(*" and "*)"
                comment_content = parts[i][:end_marker_pos]

                # Look for RowBox structure within this
                rowbox_match = re.search(r'RowBox\[\{(.*?)\}\]', comment_content, re.DOTALL)
                if rowbox_match:
                    comment_text = self.clean_rowbox_content(rowbox_match.group(1))
                else:
                    comment_text = self.clean_rowbox_content(comment_content)

                if comment_text and comment_text.strip():
                    # Convert Greek letters
                    comment_text = self.convert_greek_letters(comment_text)
                    comment_text = self.convert_unicode_escapes(comment_text)
                    comment_text = comment_text.strip()
                    if comment_text:
                        comments.append(comment_text)

        return comments

    def parse_grid_box(self, grid_content: str) -> List[List[str]]:
        """Parse GridBox content to extract table data."""
        rows = []

        # Find the main content between GridBox[{ ... }]
        grid_match = re.search(r'GridBox\[\{(.*?)\n   \},', grid_content, re.DOTALL)
        if not grid_match:
            grid_match = re.search(r'GridBox\[\{(.*?)\}\]', grid_content, re.DOTALL)
        if not grid_match:
            return rows

        grid_inner = grid_match.group(1)

        # Find rows - they start with { and can contain nested structures
        # Use a stack-based approach to find matching braces
        i = 0
        while i < len(grid_inner):
            if grid_inner[i] == '{':
                # Start of a row
                brace_count = 1
                row_start = i + 1
                i += 1

                while i < len(grid_inner) and brace_count > 0:
                    if grid_inner[i] == '{':
                        brace_count += 1
                    elif grid_inner[i] == '}':
                        brace_count -= 1
                    i += 1

                if brace_count == 0:
                    row_content = grid_inner[row_start:i-1]

                    # Extract cells from this row
                    cells = []

                    # Look for patterns like "\<\"content\"\>"
                    # Pattern: \<\"...\"\> extracts content between the escaped quotes
                    # Updated pattern handles escaped characters within cell content
                    string_matches = re.findall(r'\\<\\"((?:[^"\\]|\\.)*)\\"', row_content)
                    if string_matches:
                        cells.extend(string_matches)

                    if cells:
                        rows.append(cells)
            else:
                i += 1

        return rows

    def extract_table_from_grid(self, content: str) -> Optional[str]:
        """Extract and format table from Grid/GridBox output."""
        # Look for GridBox structures
        if 'GridBox[{' not in content:
            return None

        # Parse the grid
        rows = self.parse_grid_box(content)

        if not rows or len(rows) < 2:  # Need at least header and one data row
            return None

        # Determine number of columns
        num_cols = max(len(row) for row in rows)

        # Create LaTeX table
        latex_lines = []
        latex_lines.append(r'\begin{center}')
        latex_lines.append(r'\begin{tabular}{' + '|c' * num_cols + '|}')
        latex_lines.append(r'\hline')

        for i, row in enumerate(rows):
            # Pad row if needed
            while len(row) < num_cols:
                row.append('')

            # Escape and convert each cell
            escaped_cells = []
            for cell in row:
                cell = self.convert_greek_letters(cell)
                cell = self.convert_unicode_escapes(cell)
                # Don't escape if it looks like a number
                if not re.match(r'^[\d.]+$', cell):
                    cell = self.escape_latex_chars(cell)
                escaped_cells.append(cell)

            # Join cells with &
            row_str = ' & '.join(escaped_cells) + r' \\'
            latex_lines.append(row_str)
            latex_lines.append(r'\hline')

        latex_lines.append(r'\end{tabular}')
        latex_lines.append(r'\end{center}')

        return '\n'.join(latex_lines)

    def parse_cell(self, cell_content: str) -> Optional[Dict]:
        """Parse a Cell[...] expression."""
        # Determine cell type
        cell_type = None
        if '"Input"' in cell_content:
            cell_type = 'Input'
        elif '"Print"' in cell_content:
            cell_type = 'Print'
        elif '"Output"' in cell_content:
            cell_type = 'Output'
        elif '"Text"' in cell_content:
            cell_type = 'Text'
        else:
            # Check for CellGroupData (contains nested cells)
            if 'CellGroupData' in cell_content:
                return {'type': 'CellGroupData', 'content': cell_content}
            return None

        # Skip if it contains metadata markers
        if 'ExpressionUUID' in cell_content or 'CellChangeTimes' in cell_content:
            # Still process, but we'll extract the actual content
            pass

        return {'type': cell_type, 'content': cell_content}

    # Font size constants for styling detection
    FONT_SIZE_BOLD_THRESHOLD = 14
    FONT_SIZE_TITLE = 16

    def is_bold_or_title(self, content: str) -> bool:
        """Check if content should be formatted as bold based on font styling."""
        return ('FontWeight->Bold' in content or
                f'FontSize->{self.FONT_SIZE_BOLD_THRESHOLD}' in content or
                f'FontSize->{self.FONT_SIZE_TITLE}' in content)

    def is_italic(self, content: str) -> bool:
        """Check if content should be formatted as italic."""
        return 'FontSlant->Italic' in content

    def extract_cell_content(self, cell: Dict) -> Optional[str]:
        """Extract meaningful content from a parsed cell."""
        cell_type = cell['type']
        content = cell['content']

        if cell_type == 'Input':
            # Extract comments from input cells
            comments = self.extract_comments(content)
            if comments:
                # Format comments as LaTeX text
                result = []
                for comment in comments:
                    result.append(comment)
                return '\n\n'.join(result)

            # Code extraction not currently implemented
            return None

        elif cell_type == 'Print':
            # Extract print output

            # Check for GridBox (tables)
            if 'GridBox[{' in content:
                table_latex = self.extract_table_from_grid(content)
                if table_latex:
                    return table_latex

            # Check for InterpretationBox (complex formatted output)
            if 'InterpretationBox' in content and 'StyleBox' in content:
                # Extract from StyleBox within InterpretationBox
                stylebox_match = re.search(r'StyleBox\[([^\]]+)\]', content)
                if stylebox_match:
                    stylebox_content = stylebox_match.group(1)
                    string_content = self.extract_string_content(stylebox_content)
                    if string_content:
                        result = self.convert_greek_letters(string_content)
                        result = self.convert_unicode_escapes(result)
                        # Apply styling
                        if self.is_bold_or_title(stylebox_content):
                            result = r'\textbf{' + result + '}'
                        elif self.is_italic(stylebox_content):
                            result = r'\textit{' + result + '}'
                        return result

            # Extract string content
            string_content = self.extract_string_content(content)
            if string_content:
                # Process the string
                result = self.convert_greek_letters(string_content)
                result = self.convert_unicode_escapes(result)
                # Clean up special sequences like \.b2.
                # In Mathematica's internal string representation, sequences like \.b2 represent Unicode characters
                # using a backslash, dot, and two hex digits (here, 'b2' = U+00B2, superscript 2).
                # These are sometimes left in exported notebook text. We remove them here because Unicode
                # superscripts are already handled by convert_unicode_escapes().
                result = re.sub(r'\\\.b2', '', result)
                result = result.replace('\n', '')
                # Apply styling
                if self.is_bold_or_title(content):
                    result = r'\textbf{' + result + '}'
                elif self.is_italic(content):
                    result = r'\textit{' + result + '}'
                return result

            return None

        elif cell_type == 'Output':
            # Handle output cells (similar to Print)
            return None

        elif cell_type == 'Text':
            # Extract text content
            string_content = self.extract_string_content(content)
            if string_content:
                result = self.convert_greek_letters(string_content)
                result = self.convert_unicode_escapes(result)
                result = self.escape_latex_chars(result)
                return result
            return None

        return None

    def parse_notebook(self, filepath: str) -> List[Dict]:
        """Parse a Mathematica notebook file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except (IOError, OSError) as e:
            print(f"Error reading file {filepath}: {e}")
            return []

        # Find all Cell[...] expressions
        # We need to handle nested brackets carefully
        cells = []

        # Split by Cell[ and then find matching brackets
        parts = content.split('Cell[')

        for part in parts[1:]:  # Skip first part (header)
            # Find the matching closing bracket
            bracket_count = 1
            end_pos = 0

            for i, char in enumerate(part):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_pos = i
                        break

            if end_pos > 0:
                cell_content = 'Cell[' + part[:end_pos + 1]
                parsed_cell = self.parse_cell(cell_content)
                if parsed_cell:
                    cells.append(parsed_cell)

        return cells

    def convert_to_latex(self, notebook_path: str, output_path: Optional[str] = None) -> str:
        """Convert a Mathematica notebook to LaTeX."""
        if output_path is None:
            output_path = os.path.splitext(notebook_path)[0] + '.tex'

        # Parse the notebook
        cells = self.parse_notebook(notebook_path)

        # Generate LaTeX document
        latex_lines = []
        latex_lines.append(r'\documentclass{article}')
        latex_lines.append(r'\usepackage[utf8]{inputenc}')
        latex_lines.append(r'\usepackage{amsmath}')
        latex_lines.append(r'\usepackage{amssymb}')
        latex_lines.append(r'\usepackage{listings}')
        latex_lines.append(r'\usepackage{graphicx}')
        latex_lines.append(r'\usepackage{float}')
        latex_lines.append(r'')
        latex_lines.append(r'\title{' + self.escape_latex_chars(os.path.basename(notebook_path)) + '}')
        latex_lines.append(r'\date{}')
        latex_lines.append(r'')
        latex_lines.append(r'\begin{document}')
        latex_lines.append(r'\maketitle')
        latex_lines.append(r'')

        # Process cells
        for cell in cells:
            content = self.extract_cell_content(cell)
            if content and content.strip() and content.strip() != 'Print':
                latex_lines.append(content)
                latex_lines.append(r'')

        latex_lines.append(r'\end{document}')

        # Write output
        latex_content = '\n'.join(latex_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        print(f"Converted {notebook_path} to {output_path}")
        return output_path

    def convert_multiple_to_latex(self, notebook_paths: List[str], output_path: str) -> str:
        """Convert multiple Mathematica notebooks to a single LaTeX document."""
        # Generate LaTeX document with all notebooks
        latex_lines = []
        latex_lines.append(r'\documentclass{article}')
        latex_lines.append(r'\usepackage[utf8]{inputenc}')
        latex_lines.append(r'\usepackage{amsmath}')
        latex_lines.append(r'\usepackage{amssymb}')
        latex_lines.append(r'\usepackage{listings}')
        latex_lines.append(r'\usepackage{graphicx}')
        latex_lines.append(r'\usepackage{float}')
        latex_lines.append(r'')
        latex_lines.append(r'\title{Combined Homework Problems}')
        latex_lines.append(r'\date{}')
        latex_lines.append(r'')
        latex_lines.append(r'\begin{document}')
        latex_lines.append(r'\maketitle')
        latex_lines.append(r'')

        # Process each notebook
        for notebook_path in notebook_paths:
            if not os.path.exists(notebook_path):
                print(f"Warning: File not found: {notebook_path}")
                continue

            # Add section for this notebook
            notebook_name = self.escape_latex_chars(os.path.basename(notebook_path))
            latex_lines.append(r'\section{' + notebook_name + '}')
            latex_lines.append(r'')

            # Parse the notebook
            cells = self.parse_notebook(notebook_path)

            # Process cells
            for cell in cells:
                content = self.extract_cell_content(cell)
                if content and content.strip() and content.strip() != 'Print':
                    latex_lines.append(content)
                    latex_lines.append(r'')

            latex_lines.append(r'')
            print(f"Processed {notebook_path}")

        latex_lines.append(r'\end{document}')

        # Write output
        latex_content = '\n'.join(latex_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        print(f"Combined {len(notebook_paths)} notebooks into {output_path}")
        return output_path


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python mathematica_to_latex.py <notebook1.nb> [notebook2.nb ...] [-o output.tex]")
        print("\nExamples:")
        print("  Single notebook:  python mathematica_to_latex.py notebook.nb")
        print("  Multiple notebooks: python mathematica_to_latex.py nb1.nb nb2.nb nb3.nb -o combined.tex")
        sys.exit(1)

    converter = MathematicaToLatexConverter()

    # Parse arguments
    notebook_paths = []
    output_path = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '-o' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        else:
            notebook_paths.append(arg)
            i += 1

    # Check if files exist
    for notebook_path in notebook_paths:
        if not os.path.exists(notebook_path):
            print(f"Error: File not found: {notebook_path}")
            sys.exit(1)

    # Convert based on number of notebooks
    if len(notebook_paths) == 1:
        # Single notebook conversion
        converter.convert_to_latex(notebook_paths[0], output_path)
    else:
        # Multiple notebook conversion
        if output_path is None:
            output_path = "combined.tex"
        converter.convert_multiple_to_latex(notebook_paths, output_path)
=======
Mathematica to LaTeX Converter

Converts Mathematica notebook files (.nb) to LaTeX format with proper formatting.
"""

import re
import argparse
import sys
import base64
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

# Regex patterns for subscript conversion
# These handle various levels of escaping that can appear in Mathematica notebook files
SUBSCRIPT_DOUBLE_BACKSLASH = r'\\\\?\[Subscript\s+([^\]]+)\]'  # Matches \\[Subscript x] or \[Subscript x]
SUBSCRIPT_WITH_BASE = r'(\w+)\\\\\\\\?\[Subscript\s+([^\]]+)\]'  # Matches var\\[Subscript x] or var\\\\[Subscript x]
SUBSCRIPT_FUNCTION = r'Subscript\[([^,]+),\s*([^\]]+)\]'  # Matches Subscript[base, sub]


def convert_subscripts(text):
    r"""Convert Mathematica subscript notation to LaTeX subscripts.

    Handles multiple escaping levels that appear in .nb files:
    - \\[Subscript x] or \[Subscript x] -> _{x}
    - var\\\\[Subscript x] -> var_{x}
    - Subscript[base, sub] -> base_{sub}
    """
    text = re.sub(SUBSCRIPT_DOUBLE_BACKSLASH, r'_{\1}', text)
    text = re.sub(SUBSCRIPT_WITH_BASE, r'\1_{\2}', text)
    text = re.sub(SUBSCRIPT_FUNCTION, r'\1_{\2}', text)

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
        # Add space after operator symbols to avoid concatenation issues
        if math_symbol in [r'\[PlusMinus]', r'\[MinusPlus]', r'\[Times]',
                          r'\[LessEqual]', r'\[GreaterEqual]', r'\[NotEqual]']:
            text = text.replace(math_symbol, latex_symbol + ' ')
        else:
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

    # Look for GraphicsBox structures - count them for placeholders
    graphics_pattern = r'Cell\[GraphicsData\[|Cell\[.*?GraphicsBox\['
    matches = re.finditer(graphics_pattern, text, re.DOTALL)

    graphic_count = 0
    for match in matches:
        graphic_count += 1
        # Add placeholder - actual graphics need to be exported from Mathematica
        graphics.append(f"figure_{graphic_count}")

    return graphics


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

    # Remove line continuation characters (backslash followed by newline)
    # These are part of the file format, not the content
    grid_content = re.sub(r'\\\n\s*', '', grid_content)

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
                        # Remove FormBox expressions
                        cell = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', cell, flags=re.DOTALL)
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
        content = re.sub(r'\\\n\s*', '', content)

        # Remove FormBox expressions early (they can span lines)
        # These are complex formatted expressions that we can't convert properly
        content = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', content, flags=re.DOTALL)

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
        r'\bullet', r'\checkmark', r'\ddot', r'\dot',
        '_', '^'
    ]

    return any(indicator in text for indicator in math_indicators)


def fix_math_spacing(text):
    """Fix spacing issues in mathematical expressions."""
    # Add space after Greek letters when followed by a letter (not a special char)
    # Example: \alphax -> \alpha x
    greek_letters = [
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta',
        'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi',
        'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi',
        'psi', 'omega'
    ]

    for letter in greek_letters:
        # Match \letter followed by a lowercase letter (variable name)
        text = re.sub(rf'(\\{letter})([a-z])', r'\1 \2', text)

    # Fix common patterns like \sqrtN -> \sqrt{N}
    text = re.sub(r'\\sqrt([A-Za-z])', r'\\sqrt{\1}', text)

    return text


def clean_formbox_expressions(text):
    """Remove or simplify Mathematica FormBox expressions."""
    # Remove FormBox wrapper - these are complex formatted expressions
    # The pattern can appear with different levels of escaping:
    # 1. \\!\\(\\*FormBox[...]\\) - in tables/StyleBox
    # 2. \!\(\*FormBox[...]\) - in simple cells

    # Handle heavily escaped version (in tables)
    text = re.sub(r'\\\\!\\\\\\(\\\\\\*FormBox\[.*?TraditionalForm\]\\\\\\)', '[formula]', text, flags=re.DOTALL)

    # Handle lightly escaped version (in regular cells)
    text = re.sub(r'\\!\\\\?\(\\\\?\*FormBox\[.*?TraditionalForm\]\\\\?\)', '[formula]', text, flags=re.DOTALL)

    return text


def extract_input_code(cell_text):
    """Extract code from an Input cell."""
    # Look for RowBox patterns which contain the actual code
    # Pattern: RowBox[{"code", "parts", ...}]
    code_parts = []

    # Find all string literals in RowBox
    matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', cell_text)
    for match in matches:
        # Skip style markers and metadata
        if match in ['Input', 'Code', 'Bold', 'Italic'] or match.startswith('FontWeight'):
            continue
        # Skip empty or whitespace-only strings
        if not match or match.isspace():
            continue
        # Clean up the code
        cleaned = match.replace('\\n', '\n')
        cleaned = cleaned.replace('\\"', '"')

        # Replace Mathematica formatting codes with spaces
        cleaned = re.sub(r'\[IndentingNewLine\]', '\n', cleaned)
        cleaned = re.sub(r'\[?Continuation\]?', '', cleaned)

        # Convert bracket notations to actual brackets
        cleaned = cleaned.replace('\\[', '[')
        cleaned = cleaned.replace('\\]', ']')
        cleaned = cleaned.replace('\\(', '(')
        cleaned = cleaned.replace('\\)', ')')

        if cleaned.strip():
            code_parts.append(cleaned)

    if code_parts:
        # Join with spaces, but preserve newlines
        result = ' '.join(code_parts)
        # Clean up multiple spaces
        result = re.sub(r' +', ' ', result)
        # Clean up spacing around newlines
        result = re.sub(r' *\n *', '\n', result)
        return result
    return ''


def process_cell_content(cell_text):
    """Process a single cell's content."""
    # Check if this is a code cell (Input) - now we include these
    if '"Input"' in cell_text:
        code = extract_input_code(cell_text)
        if code:
            return ('INPUT', code)
        return ''

    # Check if this cell contains a GraphicsBox (but not inside GridBox for legends)
    # Only treat as graphic if it's a primary GraphicsBox with plot data
    if ('TagBox[' in cell_text and 'GraphicsBox[{' in cell_text and 'CompressedData[' in cell_text):
        return ('GRAPHIC', cell_text)

    # Check if this cell contains a GridBox (table)
    table_data = extract_gridbox_table(cell_text)
    if table_data:
        return ('TABLE', table_data)

    # Extract string content from Print cells and TextData cells
    content = extract_string_content(cell_text)

    if not content or len(content) < 3:
        return ''

    # Clean up FormBox expressions before other conversions
    content = clean_formbox_expressions(content)

    # Convert symbols
    content = convert_symbols(content)

    # Convert subscripts and superscripts
    content = convert_subscripts(content)
    content = convert_superscripts(content)

    # Fix math spacing issues
    content = fix_math_spacing(content)

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
                    # Could be a string or a tuple ('TABLE', data) or ('INPUT', code) or ('GRAPHIC', data)
                    if isinstance(processed, tuple):
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

    # Create output directory for figures
    output_base = Path(input_file).stem
    figures_dir = f"{output_base}_figures"

    # Extract graphics
    graphics_list = extract_graphics(content, figures_dir)

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
    latex_output.append(r'\usepackage{float}')
    latex_output.append(r'\usepackage{listings}')
    latex_output.append(r'\usepackage{xcolor}')
    latex_output.append(r'')
    latex_output.append(r'% Configure listings for Mathematica code')
    latex_output.append(r'\lstset{')
    latex_output.append(r'  language=Mathematica,')
    latex_output.append(r'  basicstyle=\small\ttfamily,')
    latex_output.append(r'  keywordstyle=\color{blue},')
    latex_output.append(r'  commentstyle=\color{green!60!black},')
    latex_output.append(r'  stringstyle=\color{red},')
    latex_output.append(r'  numbers=none,')
    latex_output.append(r'  frame=single,')
    latex_output.append(r'  breaklines=true,')
    latex_output.append(r'  backgroundcolor=\color{gray!10},')
    latex_output.append(r'  captionpos=b')
    latex_output.append(r'}')
    latex_output.append(r'')
    latex_output.append(r'\begin{document}')
    latex_output.append(r'')

    # Add title
    filename = Path(input_file).stem
    latex_output.append(r'\title{' + filename + '}')
    latex_output.append(r'\maketitle')
    latex_output.append(r'')

    # Track graphics index
    graphic_idx = 0

    # Group content for better flow
    current_paragraph = []

    # Add cells
    for cell in cells:
        # Handle input code cells
        if isinstance(cell, tuple) and cell[0] == 'INPUT':
            # Flush current paragraph
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []

            # Add code block
            code = cell[1]
            latex_output.append(r'\begin{lstlisting}')
            latex_output.append(code)
            latex_output.append(r'\end{lstlisting}')
            latex_output.append(r'')
            continue

        # Handle graphic cells
        if isinstance(cell, tuple) and cell[0] == 'GRAPHIC':
            # Flush current paragraph
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []

            # Add figure placeholder
            if graphic_idx < len(graphics_list):
                graphic = graphics_list[graphic_idx]
                latex_output.append(r'\begin{figure}[H]')
                latex_output.append(r'\centering')
                latex_output.append(r'% TODO: Export ' + graphic + '.png from Mathematica and place in ' + figures_dir + '/')
                latex_output.append(r'\includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphic + '.png}')
                latex_output.append(r'\caption{Figure ' + str(graphic_idx + 1) + '}')
                latex_output.append(r'\end{figure}')
                latex_output.append(r'')
                graphic_idx += 1
            continue

        # Handle table cells
        if isinstance(cell, tuple) and cell[0] == 'TABLE':
            # Flush current paragraph
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []

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
                        cell_val = fix_math_spacing(cell_val)
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

        # Check if this is a heading/title (short, possibly bold text)
        is_heading = len(cell) < 80 and not any(word in cell.lower() for word in ['equation', 'where', 'using', 'for', 'with'])

        # Regular text or math content
        if is_heading and not is_math_content(cell):
            # Flush current paragraph
            if current_paragraph:
                latex_output.append(' '.join(current_paragraph))
                latex_output.append(r'')
                current_paragraph = []

            # Add as section or subsection
            if len(cell) < 40:
                latex_output.append(r'\subsection*{' + cell + '}')
            else:
                latex_output.append(r'\textbf{' + cell + '}')
            latex_output.append(r'')
        else:
            # Regular content - add to paragraph
            if is_math_content(cell):
                # Wrap in math mode if not already and contains inline math
                if not (cell.startswith('$') or cell.startswith(r'\[') or '$' in cell):
                    cell = f'${cell}$'

            # Add to current paragraph
            current_paragraph.append(cell)

    # Flush final paragraph
    if current_paragraph:
        latex_output.append(' '.join(current_paragraph))
        latex_output.append(r'')

    # Add graphics placeholders if any were found but not inserted
    if len(graphics_list) > graphic_idx:
        latex_output.append(r'\section*{Figures}')
        latex_output.append(r'')
        latex_output.append(r'% The notebook contains ' + str(len(graphics_list)) + ' figures.')
        latex_output.append(r'% To include them, export the graphics from Mathematica using:')
        latex_output.append(r'%   Export["figure_N.png", graphicsObject]')
        latex_output.append(r'% Then place the PNG files in the ' + figures_dir + '/ directory.')
        latex_output.append(r'')

        for i in range(len(graphics_list)):
            latex_output.append(r'\begin{figure}[H]')
            latex_output.append(r'\centering')
            latex_output.append(r'% TODO: Export figure from Mathematica')
            latex_output.append(r'\includegraphics[width=0.7\textwidth]{' + figures_dir + '/' + graphics_list[i] + '.png}')
            latex_output.append(r'\caption{Figure ' + str(i + 1) + '}')
            latex_output.append(r'\label{fig:' + str(i + 1) + '}')
            latex_output.append(r'\end{figure}')
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
>>>>>>> origin/main


if __name__ == '__main__':
    main()
