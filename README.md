# comp382-assignment2

# Code Creation
### William Craske created the code to convert a CFG to CNF python code. 
Initial steps covered before iteration - Remove Null, Unit, and Useless Productions, Replace Terminals in Mixed Productions, Reduce Productions with More Than Two Non-Terminals. Sahil pointed out that the step "Eliminate the Start Symbol from RHS" was missing. This will be added in the next iteration along with a test case.

### indepth explanation of code:
The conversion is broken down into 4 steps, eliminating the start symbol from the right side, removing null and unit productions, replacing terminals in mixed productions, and  breaking down long productions into binary forms.

The code also handles nullable symbols, ε-productions, chains of unit productions, and recursive grammars where the start symbol references itself.

Four test cases display functionality for each aspect of the process.
 