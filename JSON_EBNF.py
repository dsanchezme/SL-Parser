import json

# grammar = json.load(open("grammar07.json"))
# grammar = json.load(open("grammar01.json"))
# grammar = json.load(open("grammar00.json"))
grammar = json.load(open("SL-Grammar.json"))

file = open("grammar.txt", "w")

for noTerminal in grammar.keys():
    file.write(f"{noTerminal} -> ")
    for i,rule in enumerate(grammar[noTerminal]):
        for symbol in rule:
            file.write(f"{symbol} ")
        if len(grammar[noTerminal]) > 1 and i < len(grammar[noTerminal])-1:
            file.write("| ")
    file.write("\n")

file.close()