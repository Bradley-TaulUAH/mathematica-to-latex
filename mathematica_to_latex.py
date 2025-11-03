#!/usr/bin/env python3
"""
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
        r'\[Omicron]': r'$\omicron$',
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
                    string_matches = re.findall(r'\\<\\"([^"\\\\]+)\\"', row_content)
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
                # Clean up special sequences like \.b2 (which is a unicode marker)
                result = re.sub(r'\\\.b2', '', result)
                result = re.sub(r'\\n', '', result)
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
        latex_lines.append(r'\title{' + os.path.basename(notebook_path).replace('_', r'\_') + '}')
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


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python mathematica_to_latex.py <notebook.nb> [output.tex]")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(notebook_path):
        print(f"Error: File not found: {notebook_path}")
        sys.exit(1)
    
    converter = MathematicaToLatexConverter()
    converter.convert_to_latex(notebook_path, output_path)


if __name__ == '__main__':
    main()
