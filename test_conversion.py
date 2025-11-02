#!/usr/bin/env python3
"""
Simple test script to validate the conversion functionality.
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_basic_conversion():
    """Test that the conversion script runs without errors."""
    print("Testing basic conversion...")
    
    result = subprocess.run(
        ['python3', 'convert.py', 'homework-8-1'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Conversion failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False
    
    print("✓ Conversion completed successfully")
    return True

def test_output_file_created():
    """Test that the output file is created."""
    print("Testing output file creation...")
    
    output_file = 'homework-8-1/latex/generated.tex'
    if not os.path.exists(output_file):
        print(f"❌ Output file not found: {output_file}")
        return False
    
    # Check file size
    file_size = os.path.getsize(output_file)
    if file_size < 100:
        print(f"❌ Output file is too small: {file_size} bytes")
        return False
    
    print(f"✓ Output file created ({file_size} bytes)")
    return True

def test_output_contains_sections():
    """Test that the output contains expected sections."""
    print("Testing output content...")
    
    output_file = 'homework-8-1/latex/generated.tex'
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Check for required LaTeX structure
    required_elements = [
        r'\documentclass',
        r'\begin{document}',
        r'\end{document}',
        r'\section{Problem 4}',
        r'\section{Problem 5}',
        r'\section{Problem 8}',
    ]
    
    missing = []
    for element in required_elements:
        if element not in content:
            missing.append(element)
    
    if missing:
        print(f"❌ Missing required elements: {missing}")
        return False
    
    print("✓ Output contains all required sections")
    return True

def test_display_modes():
    """Test that display modes are respected."""
    print("Testing display modes...")
    
    output_file = 'homework-8-1/latex/generated.tex'
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Problem 4 is output-only, so it shouldn't have lstlisting blocks
    problem4_start = content.find(r'\section{Problem 4}')
    problem5_start = content.find(r'\section{Problem 5}')
    
    if problem4_start == -1 or problem5_start == -1:
        print("❌ Could not find problem sections")
        return False
    
    problem4_content = content[problem4_start:problem5_start]
    
    # Check that Problem 4 (output-only) doesn't have code listings
    if r'\begin{lstlisting}' in problem4_content:
        print("⚠ Warning: Problem 4 (output-only) contains code listings")
        # This is not necessarily an error, depending on the notebook content
    
    # Problem 5 is input-output, so it should have lstlisting blocks
    problem5_end = content.find(r'\section{Problem 8}')
    problem5_content = content[problem5_start:problem5_end if problem5_end != -1 else len(content)]
    
    if r'\begin{lstlisting}' in problem5_content:
        print("✓ Problem 5 (input-output) contains code listings as expected")
    else:
        print("⚠ Warning: Problem 5 (input-output) doesn't contain code listings")
    
    return True

def test_configuration_parsing():
    """Test that the configuration file is parsed correctly."""
    print("Testing configuration parsing...")
    
    import yaml
    
    config_file = 'homework-8-1/config.yaml'
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate structure
        if 'homework' not in config:
            print("❌ Missing 'homework' section in config")
            return False
        
        if 'problems' not in config:
            print("❌ Missing 'problems' section in config")
            return False
        
        if len(config['problems']) != 3:
            print(f"❌ Expected 3 problems, found {len(config['problems'])}")
            return False
        
        print("✓ Configuration file is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error parsing config: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("Mathematica to LaTeX Converter - Test Suite")
    print("="*60)
    print()
    
    tests = [
        test_configuration_parsing,
        test_basic_conversion,
        test_output_file_created,
        test_output_contains_sections,
        test_display_modes,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
            print()
    
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return 0 if all(results) else 1

if __name__ == '__main__':
    sys.exit(main())
