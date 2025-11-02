#!/usr/bin/env python3
"""
Mathematica Notebook to LaTeX Converter

This script converts Mathematica notebook files (.nb) to LaTeX documents
based on user-specified display preferences in a configuration file.
"""

import os
import sys
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotebookParser:
    """Parse Mathematica notebook files and extract cells."""
    
    def __init__(self, notebook_path: str):
        self.notebook_path = notebook_path
        self.content = None
        self.cells = []
        
    def read_notebook(self):
        """Read the notebook file content."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            logger.info(f"Successfully read notebook: {self.notebook_path}")
        except Exception as e:
            logger.error(f"Error reading notebook {self.notebook_path}: {e}")
            raise
    
    def extract_cells(self):
        """Extract cells from the notebook content."""
        if not self.content:
            self.read_notebook()
        
        # Split content to focus only on the actual notebook content, not metadata
        metadata_start = self.content.find('(* Internal cache information *)')
        if metadata_start > 0:
            content_to_parse = self.content[:metadata_start]
        else:
            content_to_parse = self.content
        
        # Use regex to find all Cell declarations with types
        # This pattern matches: Cell[...content..., "Type", ...otherparams...]
        # We look for the type parameter which comes after the main content
        cells = []
        
        # Find all occurrences where we have a cell type marker
        # The pattern looks for: , "TYPE" where TYPE is Input, Output, Print, etc.
        cell_type_pattern = r',\s*"(Input|Output|Text|Print|Code)"'
        
        for match in re.finditer(cell_type_pattern, content_to_parse):
            cell_type = match.group(1)
            
            # Now we need to find the start of this Cell[
            # Work backwards from the match position to find Cell[
            pos = match.start()
            depth = 0
            cell_start = -1
            
            # Go backwards to find the matching Cell[
            for i in range(pos, -1, -1):
                if content_to_parse[i] == ']':
                    depth += 1
                elif content_to_parse[i] == '[':
                    depth -= 1
                    if depth == -1:
                        # Found the opening bracket
                        # Check if it's preceded by "Cell"
                        if i >= 4 and content_to_parse[i-4:i] == 'Cell':
                            cell_start = i - 4
                            break
            
            if cell_start == -1:
                continue
            
            # Now find the end of this cell by going forward
            depth = 0
            cell_end = -1
            for i in range(cell_start + 5, len(content_to_parse)):
                if content_to_parse[i] == '[':
                    depth += 1
                elif content_to_parse[i] == ']':
                    depth -= 1
                    if depth == -1:
                        cell_end = i + 1
                        break
            
            if cell_end > cell_start:
                cell_content = content_to_parse[cell_start:cell_end]
                # Avoid duplicates - check if we already have this cell
                if not any(c['raw'] == cell_content for c in cells):
                    cells.append({
                        'type': cell_type,
                        'content': cell_content,
                        'raw': cell_content
                    })
        
        self.cells = cells
        logger.info(f"Extracted {len(self.cells)} cells from notebook")
        return self.cells
    
    def get_cells_by_type(self, cell_type: str) -> List[Dict]:
        """Get all cells of a specific type."""
        return [cell for cell in self.cells if cell['type'] == cell_type]


class LatexConverter:
    """Convert Mathematica expressions to LaTeX."""
    
    def __init__(self):
        self.figure_counter = 0
        
    def clean_mathematica_code(self, code: str) -> str:
        """Clean up Mathematica code for display."""
        # Remove Cell wrapper and BoxData
        code = re.sub(r'Cell\[BoxData\[(.*)\],\s*"[^"]*".*\]', r'\1', code, flags=re.DOTALL)
        code = re.sub(r'Cell\[(.*),\s*"[^"]*".*\]', r'\1', code, flags=re.DOTALL)
        
        # Remove RowBox and other Box structures
        code = re.sub(r'RowBox\[\{(.*?)\}\]', r'\1', code)
        code = re.sub(r'BoxData\[(.*?)\]', r'\1', code)
        
        # Clean up quotes and escapes
        code = re.sub(r'\\"', '"', code)
        code = code.replace('\\n', '\n')
        
        # Remove excessive whitespace
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        code = '\n'.join(lines)
        
        return code
    
    def extract_output_text(self, cell_content: str) -> str:
        """Extract readable output text from a cell."""
        # Extract text from Mathematica string format: \<"text"\>
        # This is the common format in Print cells
        string_pattern = r'\\<\\"([^"\\]+)\\"\\>'
        text_matches = re.findall(string_pattern, cell_content)
        if text_matches:
            # Clean up unicode escapes and special characters
            cleaned_texts = []
            for text in text_matches:
                # Replace common Mathematica special characters
                text = text.replace('\\[HBar]', '\\hbar')
                text = text.replace('\\[Pi]', '\\pi')
                text = text.replace('\\[Infinity]', '\\infty')
                text = text.replace('\\n', ' ')
                text = text.replace('\\[InvisibleSpace]', ' ')
                # Skip empty or very short strings
                if len(text.strip()) > 2:
                    cleaned_texts.append(text)
            if cleaned_texts:
                return ' '.join(cleaned_texts)
        
        # Alternative: look for quoted strings in a simpler format
        simple_quotes = re.findall(r'"([^"]{3,})"', cell_content)
        if simple_quotes:
            # Filter out common Mathematica keywords and metadata
            filtered = [t for t in simple_quotes 
                       if t not in ['Input', 'Output', 'Text', 'Print', 'Code', 'During evaluation of']
                       and not t.startswith('ExpressionUUID')
                       and not t.startswith('In[')
                       and not any(skip in t for skip in ['RowBox', 'SuperscriptBox', 'FractionBox', 'SqrtBox'])
                       and len(t) > 2]
            if filtered:
                return ' '.join(filtered[:3])  # Limit to first 3 to avoid too much noise
        
        # Try to extract from BoxData if it contains readable content
        # Look for RowBox with text
        if 'RowBox' in cell_content or 'SuperscriptBox' in cell_content or 'FractionBox' in cell_content:
            # This likely contains code or mathematical expressions that we can't easily convert
            return ''
        
        return ''
    
    def convert_to_latex_math(self, expr: str) -> str:
        """Convert Mathematica expression to LaTeX math notation."""
        # Basic conversions
        latex = expr
        
        # Function replacements
        replacements = {
            r'Sqrt\[(.*?)\]': r'\\sqrt{\1}',
            r'Pi': r'\\pi',
            r'Infinity': r'\\infty',
            r'\^': '^',
            r'->': r'\\to',
            r'<=': r'\\leq',
            r'>=': r'\\geq',
            r'!=': r'\\neq',
            r'Integrate\[(.*?),\s*\{(.*?),\s*(.*?),\s*(.*?)\}\]': r'\\int_{\3}^{\4} \1 \, d\2',
            r'Sum\[(.*?),\s*\{(.*?),\s*(.*?),\s*(.*?)\}\]': r'\\sum_{\2=\3}^{\4} \1',
        }
        
        for pattern, replacement in replacements.items():
            latex = re.sub(pattern, replacement, latex)
        
        return latex
    
    def cell_to_latex(self, cell: Dict, display_mode: str) -> str:
        """Convert a cell to LaTeX based on display mode."""
        cell_type = cell['type']
        content = cell['content']
        
        latex_output = []
        
        if cell_type == 'Input':
            if display_mode in ['input-output', 'full']:
                # Show input code
                cleaned_code = self.clean_mathematica_code(content)
                if cleaned_code and len(cleaned_code.strip()) > 10:
                    latex_output.append("\\begin{lstlisting}")
                    latex_output.append(cleaned_code)
                    latex_output.append("\\end{lstlisting}")
                    latex_output.append("")
        
        elif cell_type in ['Output', 'Print']:
            if display_mode in ['output-only', 'input-output', 'full']:
                # Show output
                output_text = self.extract_output_text(content)
                if output_text and len(output_text.strip()) > 5:
                    # Filter out metadata-like content and Box structures
                    skip_patterns = ['CellChangeTimes', 'CellLabel', 'ExpressionUUID', 
                                   'StripOnInput', 'RowBox', 'SuperscriptBox', 
                                   'FractionBox', 'SqrtBox', '[InvisibleSpace]']
                    if any(skip in output_text for skip in skip_patterns):
                        return ''
                    
                    # Check if it looks like a heading (short text, possibly bold)
                    if len(output_text) < 100 and not any(char in output_text for char in ['=', '{', '}']):
                        # Treat as text/heading
                        latex_output.append(f"\\textbf{{{output_text}}}")
                        latex_output.append("")
                    # Check if it looks like math
                    elif any(char in output_text for char in ['=', '+', '-', '*', '/']):
                        latex_math = self.convert_to_latex_math(output_text)
                        latex_output.append("\\begin{equation}")
                        latex_output.append(latex_math)
                        latex_output.append("\\end{equation}")
                        latex_output.append("")
                    else:
                        latex_output.append(output_text)
                        latex_output.append("")
        
        elif cell_type == 'Text':
            # Always include text cells
            text_content = self.extract_output_text(content)
            if text_content and len(text_content.strip()) > 5:
                # Filter out Box structures
                if not any(skip in text_content for skip in ['RowBox', 'SuperscriptBox', 'FractionBox']):
                    latex_output.append(text_content)
                    latex_output.append("")
        
        return '\n'.join(latex_output)


class LatexDocumentGenerator:
    """Generate complete LaTeX documents."""
    
    def __init__(self, config: Dict, homework_dir: str):
        self.config = config
        self.homework_dir = homework_dir
        self.converter = LatexConverter()
        
    def generate_problem_section(self, problem: Dict, problem_num: int) -> str:
        """Generate LaTeX for a single problem."""
        logger.info(f"Processing {problem['name']}: {problem['file']}")
        
        # Parse the notebook
        notebook_path = os.path.join(self.homework_dir, 'notebooks', problem['file'])
        parser = NotebookParser(notebook_path)
        parser.extract_cells()
        
        # Start problem section
        latex_parts = []
        latex_parts.append(f"\\section{{{problem['name']}}}")
        latex_parts.append("")
        
        if 'description' in problem:
            latex_parts.append(f"\\textbf{{Description:}} {problem['description']}")
            latex_parts.append("")
        
        # Convert cells based on display mode
        display_mode = problem.get('display', 'output-only')
        
        for cell in parser.cells:
            cell_latex = self.converter.cell_to_latex(cell, display_mode)
            if cell_latex.strip():
                latex_parts.append(cell_latex)
        
        latex_parts.append("")
        latex_parts.append("\\clearpage")
        latex_parts.append("")
        
        return '\n'.join(latex_parts)
    
    def generate_document(self) -> str:
        """Generate the complete LaTeX document."""
        logger.info("Generating LaTeX document...")
        
        # Read template
        template_path = os.path.join(self.homework_dir, 'latex', 'main.tex')
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Generate content for all problems
        content_parts = []
        for i, problem in enumerate(self.config['problems'], 1):
            try:
                problem_latex = self.generate_problem_section(problem, i)
                content_parts.append(problem_latex)
            except Exception as e:
                logger.error(f"Error processing problem {i}: {e}")
                content_parts.append(f"\\section{{Problem {i}}}\n\nError processing this problem.\n\n")
        
        generated_content = '\n'.join(content_parts)
        
        # Replace placeholders in template
        homework_info = self.config['homework']
        document = template.replace('HOMEWORK_NAME', homework_info['name'])
        document = document.replace('HOMEWORK_TITLE', homework_info['title'])
        document = document.replace('HOMEWORK_AUTHOR', homework_info['author'])
        document = document.replace('GENERATED_CONTENT', generated_content)
        
        return document
    
    def save_document(self, output_path: str):
        """Generate and save the LaTeX document."""
        document = self.generate_document()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(document)
        
        logger.info(f"LaTeX document saved to: {output_path}")


def parse_config(config_path: str) -> Dict:
    """Parse the configuration YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from: {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error parsing config file: {e}")
        raise


def main():
    """Main entry point for the conversion script."""
    if len(sys.argv) < 2:
        print("Usage: python convert.py <homework-directory>")
        print("Example: python convert.py homework-8-1")
        sys.exit(1)
    
    homework_dir = sys.argv[1]
    
    # Validate directory
    if not os.path.isdir(homework_dir):
        logger.error(f"Directory not found: {homework_dir}")
        sys.exit(1)
    
    # Load configuration
    config_path = os.path.join(homework_dir, 'config.yaml')
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    
    config = parse_config(config_path)
    
    # Generate LaTeX document
    generator = LatexDocumentGenerator(config, homework_dir)
    output_path = os.path.join(homework_dir, 'latex', 'generated.tex')
    generator.save_document(output_path)
    
    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"Output file: {output_path}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
