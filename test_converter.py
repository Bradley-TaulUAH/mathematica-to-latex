#!/usr/bin/env python3
"""
Simple test script for the Mathematica converter
"""

import os
import tempfile
from mathematica_converter import MathematicaConverter


def test_converter():
    """Test the converter with example files"""
    print("Testing Mathematica to LaTeX/Markdown Converter")
    print("=" * 60)
    
    # Find all .nb files in current directory
    nb_files = [f for f in os.listdir('.') if f.endswith('.nb')]
    
    if not nb_files:
        print("No .nb files found in current directory")
        return False
    
    print(f"Found {len(nb_files)} notebook files to test\n")
    
    # Create temporary output directory
    output_dir = tempfile.mkdtemp()
    print(f"Output directory: {output_dir}\n")
    
    converter = MathematicaConverter()
    all_passed = True
    
    for nb_file in nb_files:
        print(f"Testing: {nb_file}")
        print("-" * 60)
        
        # Test conversion
        success, message = converter.convert_file(
            nb_file,
            output_format='both',
            output_dir=output_dir
        )
        
        if success:
            print(f"✓ SUCCESS: {nb_file}")
            print(f"  {message}")
            
            # Check if output files exist
            base_name = os.path.splitext(nb_file)[0]
            latex_file = os.path.join(output_dir, f"{base_name}.tex")
            markdown_file = os.path.join(output_dir, f"{base_name}.md")
            
            if os.path.exists(latex_file):
                size = os.path.getsize(latex_file)
                print(f"  LaTeX file created: {size} bytes")
            else:
                print(f"  ✗ LaTeX file not found")
                all_passed = False
                
            if os.path.exists(markdown_file):
                size = os.path.getsize(markdown_file)
                print(f"  Markdown file created: {size} bytes")
            else:
                print(f"  ✗ Markdown file not found")
                all_passed = False
        else:
            print(f"✗ FAILED: {nb_file}")
            print(f"  Error: {message}")
            all_passed = False
        
        print()
    
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed")
        return False


if __name__ == "__main__":
    import sys
    success = test_converter()
    sys.exit(0 if success else 1)
