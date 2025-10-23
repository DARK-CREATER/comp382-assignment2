#convert context free grammar to cnf
#requires all productions to be in one of these forms:
#- A -> BC (two variables)
#- A -> a (single terminal)
#- S -> ε (only for start symbol, if language includes empty string)

def toCnf(grammar, start='S'):
    #initial step: formatting of input grammar
    
    #counter for generating unique variable names
    varCounter = [0]
    
    #makes new var name thats unused
    def newVar():
        varCounter[0] += 1
        return f'V{varCounter[0]}'
    
    #check if a symbol is a terminal by lowercase or special character
    def isTerminal(symbol):
        return not symbol.isupper()
    
    #make a copy of the grammar to work with
    #turns format into list of productions
    rules = {var: list(prods) for var, prods in grammar.items()}
    
    #step 0: eliminate start symbol from rhs
    #check if start symbol appears on right side of any production
    startOnRhs = False
    for var, prods in rules.items():
        for prod in prods:
            if start in prod:
                startOnRhs = True
                break
        if startOnRhs:
            break
    
    #create new start symbol if needed
    if startOnRhs:
        newStart = 'S0'
        #make sure new start symbol doesnt already exist
        while newStart in rules:
            newStart = newVar()
        #add new start production
        rules[newStart] = [start]
        #update start symbol
        start = newStart
    
    #step 1: get rid of ε productions
    #find all nullable variables and store in set
    nullable = set()
    
    #find variables with direct ε productions and add to nullable set
    for var, prods in rules.items():
        if 'ε' in prods:
            nullable.add(var)
    
    #find variables that can produce only nullable variables
    #iterate until no new nullable variables found
    changed = True
    while changed:
        changed = False
        for var, prods in rules.items():
            if var in nullable:
                continue
            for prod in prods:
                if prod != 'ε' and all(sym in nullable for sym in prod):
                    nullable.add(var)
                    changed = True
                    break
    
    #generate new productions with nullable symbols removed
    #iterate through all productions and create combinations
    newRules = {}
    for var, prods in rules.items():
        newRules[var] = []
        for prod in prods:
            if prod == 'ε':
                continue
            
            #create all combinations by including/excluding nullable symbols
            prodList = list(prod)
            nullablePositions = []
            for i, sym in enumerate(prodList):
                if sym in nullable:
                    nullablePositions.append(i)
            
            #try all nullable combinations, 2^n, where n = number of nullable symbols
            numCombinations = 2 ** len(nullablePositions)
            for combination in range(numCombinations):
                #create new production based on this combination
                newProd = []
                for i, sym in enumerate(prodList):
                    #check if this position should be included
                    if i in nullablePositions:
                        posIndex = nullablePositions.index(i)
                        #check if bit at posIndex is set in combination
                        if combination & (1 << posIndex):
                            newProd.append(sym)
                    else:
                        newProd.append(sym)
                
                #add non empty unique productions
                newProdStr = ''.join(newProd)
                if newProdStr and newProdStr not in newRules[var]:
                    newRules[var].append(newProdStr)
    
    #add ε back for start symbol if nullable
    if start in nullable:
        newRules[start].append('ε')
    
    rules = newRules
    
    #step 2: eliminate unit productions
    #find all variables that are reachable via unit productions
    newRules = {}
    for var in rules:
        reachable = {var}
        toCheck = [var]
        
        #bfs to find all reachable variables
        while toCheck:
            current = toCheck.pop()
            for prod in rules.get(current, []):
                #unit production with single variable on right side
                if len(prod) == 1 and prod.isupper() and prod not in reachable:
                    reachable.add(prod)
                    toCheck.append(prod)
        
        #copy all non unit productions from reachable variables
        newRules[var] = []
        for reachableVar in reachable:
            for prod in rules.get(reachableVar, []):
                #skips unit productions
                isUnit = len(prod) == 1 and prod.isupper()
                if not isUnit and prod not in newRules[var]:
                    newRules[var].append(prod)
    
    rules = newRules
    
    #step 3: convert to cnf form
    #map each terminal to a variable
    newRules = {}
    terminalVars = {}
    
    #iterate through all productions and convert to cnf
    for var, prods in rules.items():
        if var not in newRules:
            newRules[var] = []
        
        #iterate each production
        for prod in prods:
            #already in cnf, ε, single terminal, or two variables
            if prod == 'ε':
                newRules[var].append(prod)
                continue
            
            #if single symbol and terminal
            if len(prod) == 1 and isTerminal(prod):
                newRules[var].append(prod)
                continue
            
            #if two symbols and both variables
            if len(prod) == 2 and all(not isTerminal(s) for s in prod):
                newRules[var].append(prod)
                continue
            
            #replace all terminals with variables
            prodVars = []
            #iterate each symbol in production
            for symbol in prod:
                if isTerminal(symbol):
                    #replace terminal with variable
                    if symbol not in terminalVars:
                        terminalVars[symbol] = newVar()
                        newRules[terminalVars[symbol]] = [symbol]
                    prodVars.append(terminalVars[symbol])
                #else keep variable as is
                else:
                    prodVars.append(symbol)
            
            #break long productions into binary ones
            if len(prodVars) == 2:
                newRules[var].append(''.join(prodVars))
            else:
                #create chain of binary productions
                currentVar = var
                #iterate through all but last two symbols
                for i in range(len(prodVars) - 2):
                    nextVar = newVar()
                    newRules[currentVar].append(prodVars[i] + nextVar)
                    currentVar = nextVar
                    if currentVar not in newRules:
                        newRules[currentVar] = []
                
                #final production with last two symbols
                newRules[currentVar].append(prodVars[-2] + prodVars[-1])
    
    return newRules

#parse production string into indivudal symbols, vars can be multichar, terminals lowercase
def parseSymbols(production):
    symbols = []
    i = 0
    #iterate through production string
    while i < len(production):
        #if uppercase, start of variable, collect full variable name
        if production[i].isupper():
            var = production[i]
            i += 1
            while i < len(production) and production[i].isdigit():
                var += production[i]
                i += 1
            symbols.append(var)
        else:
            #terminal symbol
            symbols.append(production[i])
            i += 1
    return symbols

#helper function to display grammar
def displayGrammar(grammar, title):
    print(title)
    for var in sorted(grammar.keys()):
        print(f"  {var} -> {' | '.join(grammar[var])}")

#test 1: multiple nullable symbols
g1 = {
    'S': ['ABC'],
    'A': ['ε', 'a'],
    'B': ['ε', 'b'],
    'C': ['c']
}
displayGrammar(g1, "Test 1 - Multiple nullable symbols (Initial CFG):")
result1 = toCnf(g1)
displayGrammar(result1, "Test 1 - Multiple nullable symbols (CNF):")

#test 2: long production
g2 = {
    'S': ['ABCDE'],
    'A': ['a'],
    'B': ['b'],
    'C': ['c'],
    'D': ['d'],
    'E': ['e']
}
print()
displayGrammar(g2, "Test 2 - Long production (Initial CFG):")
result2 = toCnf(g2)
displayGrammar(result2, "Test 2 - Long production (CNF):")

#test 3: unit productions chain
g3 = {
    'S': ['A', 'a'],
    'A': ['B', 'b'],
    'B': ['C', 'c'],
    'C': ['d']
}
print()
displayGrammar(g3, "Test 3 - Unit productions chain (Initial CFG):")
result3 = toCnf(g3)
displayGrammar(result3, "Test 3 - Unit productions chain (CNF):")


#test 4: start symbol on rhs
g4 = {
    'S': ['aSb', 'A'],
    'A': ['S', 'a']
}
print()
displayGrammar(g4, "Test 4 - Start symbol on RHS (Initial CFG):")
result4 = toCnf(g4)
displayGrammar(result4, "Test 4 - Start symbol on RHS (CNF):")