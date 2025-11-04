"""
Mathematica to LaTeX/Markdown Converter
Converts Mathematica notebook files (.nb) to LaTeX and Markdown formats
"""

import re
import os
from typing import Dict, List, Tuple


class MathematicaConverter:
    """Converts Mathematica notebook content to LaTeX and Markdown"""
    
    def __init__(self):
        self.content = ""
        self.cells = []
        
    def read_notebook(self, filepath: str) -> bool:
        """Read a Mathematica notebook file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()
            return True
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def parse_cells(self):
        """Extract cells from the notebook"""
        # This is a simplified parser for Mathematica notebooks
        # Real notebooks use a complex nested structure
        self.cells = []
        
        # Extract string literals which contain the actual content
        # Pattern to find quoted strings
        string_pattern = r'"([^"\\]*(\\.[^"\\]*)*)"'
        
        matches = re.findall(string_pattern, self.content)
        for match in matches:
            text = match[0] if isinstance(match, tuple) else match
            # Filter out short strings and metadata
            if text and len(text.strip()) > 5 and not text.startswith('\\['):
                # Skip if it's just formatting/metadata
                if any(keyword in text for keyword in ['CellGroupData', 'CellFrame', 'StyleData']):
                    continue
                self.cells.append(text)
    
    def convert_to_latex(self) -> str:
        """Convert parsed content to LaTeX format"""
        latex_output = []
        latex_output.append("\\documentclass{article}")
        latex_output.append("\\usepackage{amsmath}")
        latex_output.append("\\usepackage{amssymb}")
        latex_output.append("\\begin{document}")
        latex_output.append("")
        
        self.parse_cells()
        
        for cell in self.cells:
            # Clean up the cell content
            cleaned = self._clean_mathematica_syntax(cell)
            if cleaned:
                # Try to detect if it's a title/section
                if any(keyword in cell.lower() for keyword in ['part', 'section', 'problem']):
                    latex_output.append(f"\\section{{{cleaned}}}")
                else:
                    # Check if it contains math symbols
                    if self._contains_math(cleaned):
                        latex_output.append("\\[")
                        latex_output.append(cleaned)
                        latex_output.append("\\]")
                    else:
                        latex_output.append(cleaned)
                latex_output.append("")
        
        latex_output.append("\\end{document}")
        return "\n".join(latex_output)
    
    def convert_to_markdown(self) -> str:
        """Convert parsed content to Markdown format"""
        markdown_output = []
        markdown_output.append("# Mathematica Notebook Conversion")
        markdown_output.append("")
        
        self.parse_cells()
        
        for cell in self.cells:
            # Clean up the cell content
            cleaned = self._clean_mathematica_syntax(cell)
            if cleaned:
                # Try to detect if it's a title/section
                if any(keyword in cell.lower() for keyword in ['part', 'section', 'problem']):
                    markdown_output.append(f"## {cleaned}")
                else:
                    # Check if it contains math symbols
                    if self._contains_math(cleaned):
                        markdown_output.append(f"$${cleaned}$$")
                    else:
                        markdown_output.append(cleaned)
                markdown_output.append("")
        
        return "\n".join(markdown_output)
    
    def _clean_mathematica_syntax(self, text: str) -> str:
        """Clean Mathematica syntax and convert to LaTeX/Unicode"""
        # Remove extra quotes and escape sequences
        text = text.replace('\\"', '"')
        text = text.replace('\\n', ' ')
        text = text.replace('\\t', ' ')
        
        # Convert common Mathematica symbols to LaTeX
        replacements = {
            '\\[Alpha]': '\\alpha',
            '\\[Beta]': '\\beta',
            '\\[Gamma]': '\\gamma',
            '\\[Delta]': '\\delta',
            '\\[Epsilon]': '\\epsilon',
            '\\[Pi]': '\\pi',
            '\\[Sigma]': '\\sigma',
            '\\[Theta]': '\\theta',
            '\\[Lambda]': '\\lambda',
            '\\[Mu]': '\\mu',
            '\\[Nu]': '\\nu',
            '\\[Rho]': '\\rho',
            '\\[Tau]': '\\tau',
            '\\[Phi]': '\\phi',
            '\\[Chi]': '\\chi',
            '\\[Psi]': '\\psi',
            '\\[Omega]': '\\omega',
            '\\[Infinity]': '\\infty',
            '\\[Integral]': '\\int',
            '\\[LessEqual]': '\\leq',
            '\\[GreaterEqual]': '\\geq',
            '\\[NotEqual]': '\\neq',
            '\\[PlusMinus]': '\\pm',
            '\\[Rule]': '\\rightarrow',
            '\\[IndentingNewLine]': '\n',
        }
        
        for mathematica_sym, latex_sym in replacements.items():
            text = text.replace(mathematica_sym, latex_sym)
        
        # Remove remaining special markers
        text = re.sub(r'\\[A-Z][a-z]+', '', text)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _contains_math(self, text: str) -> bool:
        """Check if text contains mathematical symbols"""
        math_indicators = ['\\', '=', '^', '_', 'int', 'sum', 'frac', 
                          'alpha', 'beta', 'gamma', 'delta', 'pi']
        return any(indicator in text.lower() for indicator in math_indicators)
    
    def convert_file(self, input_path: str, output_format: str = 'both', 
                    output_dir: str = None) -> Tuple[bool, str]:
        """
        Convert a Mathematica notebook file to specified format
        
        Args:
            input_path: Path to input .nb file
            output_format: 'latex', 'markdown', or 'both'
            output_dir: Output directory (default: same as input)
            
        Returns:
            Tuple of (success, message)
        """
        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"
        
        if not self.read_notebook(input_path):
            return False, "Failed to read notebook file"
        
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(input_path)
        
        # Get base filename
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        results = []
        
        # Convert to LaTeX
        if output_format in ['latex', 'both']:
            latex_content = self.convert_to_latex()
            latex_path = os.path.join(output_dir, f"{base_name}.tex")
            try:
                with open(latex_path, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                results.append(f"LaTeX: {latex_path}")
            except Exception as e:
                return False, f"Failed to write LaTeX file: {e}"
        
        # Convert to Markdown
        if output_format in ['markdown', 'both']:
            markdown_content = self.convert_to_markdown()
            markdown_path = os.path.join(output_dir, f"{base_name}.md")
            try:
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                results.append(f"Markdown: {markdown_path}")
            except Exception as e:
                return False, f"Failed to write Markdown file: {e}"
        
        return True, "Conversion successful!\n" + "\n".join(results)


if __name__ == "__main__":
    # Simple command-line interface
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mathematica_converter.py <input.nb> [output_format] [output_dir]")
        print("  output_format: latex, markdown, or both (default: both)")
        print("  output_dir: output directory (default: same as input)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'both'
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    converter = MathematicaConverter()
    success, message = converter.convert_file(input_file, output_format, output_dir)
    
    print(message)
    sys.exit(0 if success else 1)
