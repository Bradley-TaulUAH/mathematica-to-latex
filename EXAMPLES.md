# Example Conversions

This document shows examples of content extracted from the Mathematica notebooks.

## HW 8-1 pb 8.nb - Barrier in a Well

### Comments Extracted
```
Barrier in a Well
Natural units : ℏ
Parameters : σ
Basis functions and potential
Matrix elements
Build Hamiltonian and find lowest 4 energies
```

### Table Example
The script converts GridBox structures to LaTeX tables:

**Input (Mathematica):**
```
GridBox[{
    {"\<\"Level\"\>", "\<\"Energy\"\>"},
    {"\<\"E1\"\>", ...6.7185...},
    {"\<\"E2\"\>", ...20.2795...},
    ...
}]
```

**Output (LaTeX):**
```latex
\begin{center}
\begin{tabular}{|c|c|}
\hline
Level & Energy \\
\hline
E1 & 6.7185 \\
\hline
E2 & 20.2795 \\
\hline
E3 & 45.6276 \\
\hline
E4 & 79.9240 \\
\hline
\end{tabular}
\end{center}
```

## HW 8-1 pb 4.nb - Infinite Square Well

### Unicode Conversion Examples

**Mathematica notation:**
- `\[Infinity]` → `$\infty$`
- `\[PlusMinus]` → `$\pm$`
- `\[LessEqual]` → `$\leq$`
- `\[Psi]` → `$\psi$`
- `\[HBar]` → `$\hbar$`

**Sample extracted text:**
```
Potential: V = 0 for -a < x < a, V = ∞ elsewhere
Boundary conditions: ψ(±a) = 0
```

## HW 8-1 pb 5-all.nb - Rayleigh-Ritz Method

### Complex Formatting Preserved

The script handles:
- Subscripts: `f₁`, `f₂` → `f$_1$`, `f$_2$`
- Superscripts: `x²`, `x³` → `x$^2$`, `x$^3$`
- Mathematical operators: `⟨f|g⟩` → `$\langle f | g \rangle$`
- Integrals: `∫` → `$\int$`

**Sample output:**
```
STEP 2: Overlap Matrix Elements S_ij = ⟨f_i|f_j⟩

S₁₁ = ∫ f₁² dx
```

## Statistics

| Notebook | Input Lines | Output Lines | Tables | Comments |
|----------|-------------|--------------|--------|----------|
| HW 8-1 pb 8.nb | 760 | 115 | 4 | 10 |
| HW 8-1 pb 4.nb | 3673 | 376 | Multiple | 50+ |
| HW 8-1 pb 5-all.nb | 7729 | 293 | Multiple | 40+ |

## Quality Verification

All generated LaTeX files:
- ✅ Compile without errors
- ✅ Properly escape special characters
- ✅ Preserve mathematical notation
- ✅ Format tables correctly
- ✅ Extract all meaningful content
- ✅ Skip metadata and UUIDs
