#!/usr/bin/env python3.6

operators1 = dict()
operators1[','] = "tk_coma"
operators1[']'] = "tk_corchete_derecho"
operators1['['] = "tk_corchete_izquierdo"
operators1[':'] = "tk_dos_puntos"
operators1['}'] = "tk_llave_derecha"
operators1['{'] = "tk_llave_izquierda"
operators1['%'] = "tk_modulo"
operators1['*'] = "tk_multiplicacion"
operators1[')'] = "tk_parentesis_derecho"
operators1['('] = "tk_parentesis_izquierdo"
operators1['^'] = "tk_potenciacion"
operators1['.'] = "tk_punto"
operators1[';'] = "tk_punto_y_coma"
operators1['-'] = "tk_resta"
operators1['+'] = "tk_suma"

operators2 = dict()
operators2['='] = "tk_asignacion"
operators2['=='] = "tk_igual_que"
operators2['<'] = "tk_menor"
operators2['<>'] = "tk_distinto_de"
operators2['<='] = "tk_menor_igual"
operators2['>'] = "tk_mayor"
operators2['>='] = "tk_mayor_igual"
operators2['/'] = "tk_division"


reservedWords = ["and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo", "desde",
                 "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib", "not", "programa", 
                 "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables", "mem",
                 "TRUE", "FALSE", "SI", "NO", "NUL",
                 "cadena", "logico", "numerico",
                #  "abs", "arctan", "cos", "exp", "int", "log", "sin", "sqrt", "tan",
                #  "ascii", "lower", "ord", "pos", "strdup", "strlen", "substr", "upper",
                #  "beep", "cls", "imprimir", "leer", "eof", "get_color", "get_curpos", "get_ifs", "get_ofs", "get_scrsize",
                #  "readkey", "set_color", "set_curpos", "set_ifs", "set_ofs", "set_stdin", "set_stdout",
                #  "str", "val", "alen", "dim", "dec", "ifval", "inc", "intercambiar", "max", "min", "paramval", "pcount",
                #  "random", "runcmd", "sec", "swap", "terminar",
                #  "salir", "sub"
                 ]

alphabet = "abcdefghijklmnñopqrstuvwxyz_"

def lexer(lines, curRow, curCol):
  
  valid = False
  comment = False
  commentEnd = False
  row = 1

  for line in lines:
    # line = line.rstrip()
    # print("LINE: ", line)
    col = 1
    tempChr = ""
    chr = line[0] if len(line) > 0 else ''
    while True:      
      if(col >= len(line)):
        break
      chr = line[col-1]
      
      if(chr == "*" and comment):
        if(col < len(line)):
          if(line[col] == "/"):
            comment = False
            col += 2
            continue
        else:
          break

      if comment:
        col += 1
        continue

      # Single or double character operators (operators2)
      if(chr in operators2.keys()):
        tempChr = chr
        if(col < len(line)):
          if line[col-1]+line[col] == '//':
            curCol = 0
            break
          elif line[col-1]+line[col] == '/*':
            comment = True
            commentEnd = False
            if('*/' not in line[col:]):
              for commentLine in lines[row+1:]:
                if('*/' in commentLine):
                  commentEnd = True
            else:
              commentEnd = True

            if(not commentEnd):
              comment = False

          if(line[col-1]+line[col] in operators2.keys()):
            tempChr = line[col-1]+line[col]
        if not comment:
          # print(f"<{operators2[tempChr]},{row},{col}>")
          return operators2[tempChr], list(operators2.keys())[list(operators2.values()).index(operators2[tempChr])], curRow+row, curCol+col
          # col += len(tempChr)-1
      # Single character operators (operators1)
      elif(chr in operators1.keys()):
        # print(f"<{operators1[chr]},{row},{col}>")
        return operators1[chr], list(operators1.keys())[list(operators1.values()).index(operators1[chr])], curRow+row, curCol+col
      
      # Strings delimited by '' or ""
      elif((chr == "'" or chr == '"' or chr == '“')):
        i = col
        tempChr = chr
        while(i < len(line)):
          tempChr += line[i]

          if(line[i] == "\\"):
            if(i+1 < len(line)):
              tempChr += line[i+1]
              i += 2
          elif(((line[i] != "'" and chr == "'") or (line[i] != '"' and chr == '"') or (line[i] != '”' and chr == '“'))):
            if(i+1 >= len(line)):
              print(f">>> Error lexico(linea:{curRow+row},posicion:{curCol+col})")
              quit()
            i += 1
          else:
            valid = True
            # print(f"<tk_cadena,{tempChr},{row},{col}>")
            return "tk_cadena", tempChr, curRow+row, curCol+col
            # if(('\\"' in line) or ("\\'" in line)):
            #   col += len(tempChr)-1  
            # else:
            #   col += len(tempChr)-1
            
            # break
          
        if(not valid):
          print(f">>> Error lexico(linea:{curRow+row},posicion:{curCol+col})")
          quit()
      # Identifiers
      elif(chr in alphabet or chr in alphabet.upper()):
        i = col
        tempChr = chr
        while(i < len(line)):
          if(line[i].isnumeric() or line[i] in alphabet or line[i] in alphabet.upper()):
            tempChr += line[i]
          else:
            break
          i += 1

        if((tempChr not in reservedWords) or len(tempChr) == 32):
          # print(f"<id,{tempChr},{row},{col}>")
          # return "id", tempChr, curRow+row, curCol+col
          return "id", tempChr, curRow+row, curCol+col
        else:
          # print(f"<{tempChr},{row},{col}>")
          return tempChr, tempChr, curRow+row, curCol+col
        # col += len(tempChr)-1
      # Numbers and Exponential notation
      elif(chr.isdigit()):
        i = col
        tempChr = chr
        while(i < len(line)):
          if(line[i].isdigit()):
            tempChr += line[i]
          elif(line[i] == "."):
            if(("." not in tempChr) and ("e" not in tempChr) and ("E" not in tempChr) and (i+1 < len(line))):
              if(line[i+1].isdigit()):
                tempChr += line[i]
              else:
                break
            else:
              break
          elif(line[i] == "e" or line[i] == "E"):
            if(("e" not in tempChr) and ("E" not in tempChr)):
              if(i+1 < len(line)):
                if((line[i+1] == "+" or line[i+1] == "-")):
                  if(line[i+2].isdigit()):
                    tempChr += line[i]+line[i+1]+line[i+2]
                    i += 2
                  else:
                    break
                elif(line[i+1].isdigit()):
                  tempChr += line[i]+line[i+1]
                  i += 1
                else:
                  break
            else:
              break
          else:
            break
          i += 1
        # print(f"<tk_numero,{tempChr},{row},{col}>")
        return "tk_numero", tempChr, curRow+row, curCol+col
        # col += len(tempChr)-1
      elif(chr in [" ", "\n", "\t"]):
        pass
      elif(chr == "$"):
        # print("HOLLAAAA")
        return "$", "$", curRow+row, curCol+col
      else:
        print(">>>",chr)
        print(f">>> Error lexico(linea:{curRow+row},posicion:{curCol+col})")
        quit()
      
      col += 1
    row += 1



import sys

codeLines = []

if len(sys.argv) > 1:
  filename = sys.argv[1]
  file = open(filename, "r")
  lines = file.readlines()
else:
  lines =  sys.stdin.readlines()

for i,line in enumerate(lines):
  if i == len(lines)-1:
    codeLines.append(line.rstrip(' '))
  else:
    codeLines.append(line.rstrip() + ' ')

# print("###########")
# print(codeLines)
# print("###########")

if(codeLines[-1][-1] == "\n"):
  codeLines.append("$ ")
else:
  codeLines[-1] = codeLines[-1]+"$ "

codeLines.append(" ")


# codeLines = ["$"]
curRow = 0
curCol = 0

def getNextToken():
  global curRow
  global curCol

  lines = [codeLines[curRow][curCol:]] + codeLines[curRow+1:]
  ans = lexer(lines, curRow, curCol)
  if not ans:
    # print("NOPE", lines)
    quit() 
  token, value, curRow, curCol = ans
  # print("token",token)
  # if ((value not in reservedWords) and (value not in operators1.keys()) and (value not in operators2.keys())):
  #   print(f"<{token},{value},{curRow},{curCol}>")
  # else:
  #   print(f"<{token},{curRow},{curCol}>")
  
  # result = f"<{token},{value},{curRow},{curCol}>"
  result = [token,value,curRow,curCol]

  curRow -= 1
  curCol += len(value)-1

  if curRow == len(codeLines)-1 and curCol+1 == len(codeLines[curRow]):
    quit()

  if(curCol+1 == len(codeLines[curRow])):
    curCol = 0
    curRow += 1
  
  return result

# print(getNextToken())