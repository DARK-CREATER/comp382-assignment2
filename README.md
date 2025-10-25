# CFG to CNF Conversion Project

This project implements a complete pipeline for converting a **Context-Free Grammar (CFG)** into **Chomsky Normal Form (CNF)**. The conversion is carried out through a sequence of structured transformations that preserve the language of the original grammar.


## Overview

Chomsky Normal Form is a standardized representation of CFGs in which every production rule must be in one of the following forms:

- **A → BC**  (two non-terminals)
- **A → a**   (a single terminal)
- **S → ε**   (only permitted if the language includes the empty string)

This normalized form is particularly useful for parsing algorithms such as the **CYK Algorithm**, formal language proofs, and automated syntax analysis.

## Files in the Repository

| File | Description |
|------|-------------|

| **CFG_To_CNF.py** | Python implementation of the conversion algorithm. Includes steps for removing ε-productions, unit productions, and restructuring productions into CNF. |

| **CNF_diagram.png** | Visual programming data-flow diagram illustrating the transformation pipeline from the initial grammar to final CNF output. Useful for understanding step-by-step grammar transitions. |

| **presentation.pptx** | Slide deck summarizing the project, algorithmic steps, diagrams, code explanations, and final results. Intended for academic or in-class presentation. |

## Algorithm Steps

The conversion follows a deterministic four-stage pipeline:

1. **Start Symbol Normalization**  
   Ensures the start symbol does not appear on the right-hand side of any rule.

2. **ε-Production Removal**  
   Identifies nullable variables and systematically removes ε-productions while preserving valid derivations.

3. **Unit Production Removal**  
   Eliminates productions of the form `A → B` by collapsing variable substitution chains.

4. **CNF Structural Conversion**  
   - Introduces new variables to isolate terminals in multi-symbol rules.  
   - Decomposes long right-hand sides into binary productions.

## Running the Code

```bash
python3 CFG_To_CNF.py
