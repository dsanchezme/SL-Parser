import json
from predictions import *

# grammar = json.load(open("grammar07.json"))
# grammar = json.load(open("grammar01.json"))
# grammar = json.load(open("grammar00.json"))
grammar = json.load(open("SL-Grammar.json"))

grammar = noLeftRecursion(grammar)
# initSymbol = "A"
# initSymbol = "S"
initSymbol = "codigo"

file = open("main.py", "w")
    
file.write("#!/usr/bin/python\n\n")
file.write("import lexer_parser\n\n")
file.write("token = ''\n")
file.write("nextToken = ''\n\n")

file.write("def init():\n")
file.write("\tglobal token\n")
file.write("\tglobal nextToken\n")
file.write("\tnextToken = lexer_parser.getNextToken()\n")
# file.write("\ttoken = nextToken[1:-1].split(',')[0]\n")
file.write("\ttoken = nextToken[0]\n")
file.write(f"\t{initSymbol}()\n")
file.write("\tif(token != '$'):\n")
file.write("\t\tsyntaxError(set({'$'}))\n")
file.write("\tprint('El analisis sintactico ha finalizado exitosamente.')\n\n")

file.write("def syntaxError(posibles):\n")
# file.write("\tprint(nextToken)\n")
# file.write("\tlexema = nextToken[1:-1].split(',')[1]\n")
file.write("\tlexema = nextToken[1]\n")
# file.write("\trow = nextToken[1:-1].split(',')[2]\n")
file.write("\trow = nextToken[2]\n")
# file.write("\tcol = nextToken[1:-1].split(',')[3]\n")
file.write("\tcol = nextToken[3]\n")
file.write("\tposibleList = []\n")
# file.write("\tprint(posibles)\n")
file.write("\tfor posible in posibles:\n")
file.write("\t\tif posible in lexer_parser.operators1.values():\n")
file.write("\t\t\tmatch = list(lexer_parser.operators1.keys())[list(lexer_parser.operators1.values()).index(posible)]\n")
file.write("\t\telif posible in lexer_parser.operators2.values():\n")
file.write("\t\t\tmatch = list(lexer_parser.operators2.keys())[list(lexer_parser.operators2.values()).index(posible)]\n")
file.write("\t\telif posible == 'id':\n")
file.write("\t\t\tmatch = 'identificador'\n")
file.write("\t\telse:\n")
file.write("\t\t\tmatch = posible\n")
file.write("\t\tposibleList.append(\"'\"+match+\"'\")\n")
file.write("\tif(lexema == '$'):\n")
file.write("\t\tprint(f\"<{row}:{col}> Error sintactico: se encontro final de archivo; se esperaba: {', '.join(sorted(posibleList))}.\")\n")
file.write("\telse:\n")
file.write("\t\tprint(f\"<{row}:{col}> Error sintactico: se encontro: '{lexema}'; se esperaba: {', '.join(sorted(posibleList))}.\")\n")
file.write("\tquit()\n\n")

file.write("def emparejar(esperado):\n")
file.write("\tglobal token\n")
file.write("\tglobal nextToken\n")
file.write("\tif(token == esperado):\n")
file.write("\t\tnextToken = lexer_parser.getNextToken()\n")
# file.write("\t\ttoken = nextToken[1:-1].split(',')[0]\n")
file.write("\t\ttoken = nextToken[0]\n")
file.write("\telse:\n")
file.write("\t\tsyntaxError(set({esperado}))\n\n")


for X in grammar.keys():
    file.write(f"def {X}():\n")        
    # file.write(f"\tprint(f'{X}')\n")
    # file.write(f"\tprint(token+' \\n')\n")
    allPosible = set()
    for i,right in enumerate(grammar[X]):
        posible = pred(grammar, X, initSymbol, right)
        allPosible = allPosible.union(posible)
        if(i == 0):
            file.write("\tif(")
        else:
            file.write("\telif(")
        
        for j, posibleSymbol in enumerate(posible):
            file.write(f"token == '{posibleSymbol}'")
            if len(posible) > 1 and j < len(posible)-1:
                file.write(" or ")
            if j == len(posible)-1:
                file.write("):\n")
        # file.write(f"\t\tprint('{X}', \"{posible}\")\n")
        for symbol in right:
            if symbol in grammar.keys():
                file.write(f"\t\t{symbol}()\n")
            else:
                if symbol == 'EPSILON':
                    file.write(f"\t\tpass\n")
                else:
                    file.write(f"\t\temparejar('{symbol}')\n")
    # if ["EPSILON"] not in grammar[X]:
    file.write("\telse:\n")
    # file.write(f"\t\tprint('{X}')\n")
    file.write(f"\t\tsyntaxError(set({allPosible}))\n\n")

    file.write("\n")
    
file.write("init()\n")

file.close()