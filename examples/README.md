# Example Mathematica Notebooks

This directory contains generic example notebooks to demonstrate the converter's capabilities.

## Included Examples

### 1. simple_calculus.nb
Basic calculus operations:
- Differentiation: `D[x^2, x]` → `2x`
- Integration: `∫x² dx` → `x³/3`
- Solving equations: `x² - 4 = 0` → `x = ±2`

### 2. physics_example.nb
Physics example featuring quantum harmonic oscillator:
- Energy level formula: `Eₙ = ℏω(n + 1/2)`
- Wave function with exponential decay
- Numerical calculations

### 3. symbolic_math.nb
Symbolic mathematics demonstrations:
- Trigonometric identities and expansions
- Matrix operations (determinants, eigenvalues)
- Simplification of expressions

## Using Your Own Files

**To convert your own Mathematica notebooks:**

1. Place your `.nb` files anywhere on your computer
2. Launch the GUI: `python mathematica_gui.py`
3. Click "Add Files..." and select your notebooks
4. Choose output settings and click "Convert to LaTeX"

**Important:** These example files are for demonstration only. Replace them with your own notebooks for actual work.

## Privacy Note

**These examples are generic and public.** If you're working on homework, research, or proprietary content:
- Keep your `.nb` files in a separate private location
- Don't commit sensitive notebooks to public repositories
- The converter works on any `.nb` file regardless of location
