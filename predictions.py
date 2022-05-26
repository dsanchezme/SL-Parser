from lib2to3.pgen2 import grammar


recursiveCalls = 0

def noLeftRecursion(grammar):
    noTerminals = grammar.keys()
    auxGrammar = dict()
    newName = "_new"
    toUpdate = set()
    for X in noTerminals:    
        auxGrammar[X+newName] = []
        auxGrammar[X] = []
        for right in grammar[X]:
            if(right[0] == X):
                auxGrammar[X+newName].append(right[1:]+[X+newName])                
                if ["EPSILON"] not in auxGrammar[X+newName]:
                    auxGrammar[X+newName].append(["EPSILON"])
                toUpdate.add(X)
                toUpdate.add(X+newName)
            else:
                if right != ["EPSILON"]:
                    auxGrammar[X].append(right + [X+newName])          
                else:
                    auxGrammar[X].append([X+newName])          
    for X in toUpdate:
        grammar.update({X:auxGrammar[X]})
    
    return grammar

def primerosInternos(grammar, a):
    
    noTerminals = grammar.keys()

    firstSet = set()

    if a == ["EPSILON"]:
        return set({"EPSILON"})
    
    if ((a[0] not in noTerminals) and (a[0] != "EPSILON")):
        return set({a[0]})

    if (a[0] in noTerminals):
        for right in grammar[a[0]]:
            auxPrimeros = primerosInternos(grammar, right)
            firstSet = (firstSet | auxPrimeros) - set({"EPSILON"})
            if "EPSILON" in auxPrimeros:
                if len(a) == 1:
                    firstSet.add("EPSILON")
                else:
                    firstSet = (firstSet | primerosInternos(grammar, a[1:]))
    return firstSet


def primeros(grammar, A):
    firstSet = set()
    for rigth in grammar[A]:
        firstSet = firstSet | primerosInternos(grammar, rigth)
    return firstSet

def leftFactoring(grammar):
    auxGrammar = grammar
    for X in grammar.keys():
        longer = 0
        for right in grammar[X]:
            if longer < len(right):
                longer = len(right)
        factors = {}
        factorized = []
        for commonlenght in range(longer, 0, -1):            
            for i, right in enumerate(grammar[X]):
                for j in range(i+1, len(grammar[X]), 1):
                    if(right[:commonlenght] == grammar[X][j][:commonlenght]):
                        if(i not in factorized and j not in factorized):
                            if commonlenght not in factors.keys():
                                factors[commonlenght] = set({})
                            factors[commonlenght] = factors[commonlenght] | set({i,j})
                            factorized = factorized + [i,j]
            commonlenght += 1
        
        for lenght in factors.keys():
            for i in lenght:
                auxGrammar[X].append([])

visited = []
def siguientes(grammar, A, initSymbol):

    followSet = set()
    noTerminals = grammar.keys()
    if A == initSymbol:
        followSet.add("$")
    
    for X in noTerminals:
        for right in grammar[X]:
            for i,symbol in enumerate(right):
                if symbol == A:
                    beta = right[i+1:] if len(right[i+1:])>0 else ["EPSILON"]
                    primerosBeta = primerosInternos(grammar, beta)
                    # print(beta, primerosBeta)
                    followSet = followSet.union(primerosBeta.difference(set({"EPSILON"})))
                    if("EPSILON" in primerosBeta):
                        if (X,beta) not in visited:
                            visited.append((X,beta))
                            followSet = followSet.union(siguientes(grammar, X, initSymbol))
                        # print(visited)
    return followSet


def pred(grammar, A, initSymbol, right):
    global visited
    visited = []
    prediccion = primerosInternos(grammar, right)
    if("EPSILON" in prediccion):
        # print("############## -", follow(grammar, A, initSymbol))        
        return prediccion.difference(set({"EPSILON"})).union(siguientes(grammar, A, initSymbol))
    return prediccion


import json

grammar = json.load(open("SL-Grammar.json"))
# grammar = json.load(open("grammar00.json"))

grammar = noLeftRecursion(grammar)
initSymbol = "codigo"
# initSymbol = "A"

# for X in grammar.keys():
#     for right in grammar[X]:
#         print(f"{X:<2} -> {' '.join(right)}")
# print(" ") 


# for X in grammar.keys():
#     for right in grammar[X]:
#         print(f"{X:<8} -> {' '.join(right):<20} {str(pred(grammar, X, initSymbol,right))}")

# for X in grammar.keys():
#     print(f"Primeros({X}) = {primeros(grammar, X)}")

# print(" ") 

# for X in grammar.keys():
#     visited = []
#     print(f"Siguientes({X}) = {siguientes(grammar, X, initSymbol)}")

# print(primerosInternos(grammar, ["declaracion"]))
# print(siguientes(grammar, 'declaracion_contenido', initSymbol))

# X = 'sentencia'
# print(f"Siguientes({X}) = {follow(grammar, X, initSymbol)}")

# print(pred(grammar, 'expresion_', 'codigo', ["EPSILON"]))

# X = "mas_declaraciones"
# for right in grammar[X]:
#         print(f"{X:<8} -> {' '.join(right):<20} {str(pred(grammar, X, initSymbol,right))}")