#!/usr/bin/python

import lexer_parser

token = ''
nextToken = ''

def init():
	global token
	global nextToken
	nextToken = lexer_parser.getNextToken()
	token = nextToken[0]
	codigo()
	if(token != '$'):
		syntaxError(set({'$'}))
	print('El analisis sintactico ha finalizado exitosamente.')

def syntaxError(posibles):
	lexema = nextToken[1]
	row = nextToken[2]
	col = nextToken[3]
	posibleList = []
	for posible in posibles:
		if posible in lexer_parser.operators1.values():
			match = list(lexer_parser.operators1.keys())[list(lexer_parser.operators1.values()).index(posible)]
		elif posible in lexer_parser.operators2.values():
			match = list(lexer_parser.operators2.keys())[list(lexer_parser.operators2.values()).index(posible)]
		elif posible == 'id':
			match = 'identificador'
		else:
			match = posible
		posibleList.append("'"+match+"'")
	if(lexema == '$'):
		print(f"<{row}:{col}> Error sintactico: se encontro final de archivo; se esperaba: {', '.join(sorted(posibleList))}.")
	else:
		print(f"<{row}:{col}> Error sintactico: se encontro: '{lexema}'; se esperaba: {', '.join(sorted(posibleList))}.")
	quit()

def emparejar(esperado):
	global token
	global nextToken
	if(token == esperado):
		nextToken = lexer_parser.getNextToken()
		token = nextToken[0]
	else:
		syntaxError(set({esperado}))

def codigo():
	if(token == 'programa' or token == 'inicio' or token == 'const' or token == 'var' or token == 'tipos'):
		nombre()
		declaracion()
		main()
		subrutina_()
	else:
		syntaxError(set({'programa', 'inicio', 'const', 'var', 'tipos'}))


def nombre():
	if(token == 'programa'):
		emparejar('programa')
		emparejar('id')
	elif(token == 'tipos' or token == 'const' or token == 'var' or token == 'inicio'):
		pass
	else:
		syntaxError(set({'programa', 'inicio', 'const', 'var', 'tipos'}))


def declaracion():
	if(token == 'var'):
		emparejar('var')
		declaracion_contenido_var()
		declaracion()
	elif(token == 'tipos'):
		emparejar('tipos')
		declaracion_contenido_tipos()
		declaracion()
	elif(token == 'const'):
		emparejar('const')
		declaracion_contenido_const()
		declaracion()
	elif(token == 'inicio'):
		pass
	else:
		syntaxError(set({'const', 'inicio', 'var', 'tipos'}))


def declaracion_contenido_const():
	if(token == 'id'):
		emparejar('id')
		emparejar('tk_asignacion')
		expresion()
		mas_declaraciones_const()
	else:
		syntaxError(set({'id'}))


def declaracion_contenido_tipos():
	if(token == 'id'):
		emparejar('id')
		emparejar('tk_dos_puntos')
		tipo_dato()
		mas_declaraciones_tipos()
	else:
		syntaxError(set({'id'}))


def declaracion_contenido_var():
	if(token == 'id'):
		emparejar('id')
		otros_id()
		emparejar('tk_dos_puntos')
		tipo_dato()
		mas_declaraciones_var()
	else:
		syntaxError(set({'id'}))


def valor():
	if(token == 'id'):
		emparejar('id')
		valor_aux()
	elif(token == 'tk_numero' or token == 'tk_suma' or token == 'tk_cadena' or token == 'tk_resta' or token == 'TRUE' or token == 'SI' or token == 'NO' or token == 'FALSE'):
		variable()
	else:
		syntaxError(set({'id', 'tk_numero', 'tk_suma', 'tk_cadena', 'tk_resta', 'TRUE', 'SI', 'NO', 'FALSE'}))


def valor_aux():
	if(token == 'tk_parentesis_izquierdo'):
		llamada_subrutina()
	elif(token == 'tk_corchete_izquierdo' or token == 'tk_punto'):
		id_arreglo_registro()
	elif(token == 'tk_suma' or token == 'tk_igual_que' or token == 'caso' or token == 'paso' or token == 'mientras' or token == 'tk_multiplicacion' or token == 'or' or token == 'hasta' or token == 'const' or token == 'var' or token == 'id' or token == 'tk_llave_derecha' or token == 'tk_mayor' or token == 'eval' or token == 'repetir' or token == 'and' or token == 'si' or token == 'tipos' or token == 'tk_llave_izquierda' or token == 'tk_corchete_derecho' or token == 'sino' or token == 'tk_resta' or token == 'fin' or token == 'retorna' or token == 'tk_potenciacion' or token == 'tk_mayor_igual' or token == 'tk_distinto_de' or token == 'tk_menor_igual' or token == 'desde' or token == 'tk_menor' or token == 'tk_parentesis_derecho' or token == 'tk_punto_y_coma' or token == 'inicio' or token == 'tk_division' or token == 'tk_coma' or token == 'tk_modulo'):
		pass
	else:
		syntaxError(set({'tk_suma', 'tk_igual_que', 'caso', 'mientras', 'tk_multiplicacion', 'or', 'tk_corchete_izquierdo', 'hasta', 'const', 'var', 'tk_modulo', 'id', 'tk_llave_derecha', 'tk_mayor', 'eval', 'repetir', 'tk_parentesis_izquierdo', 'and', 'si', 'tipos', 'tk_llave_izquierda', 'tk_corchete_derecho', 'sino', 'tk_resta', 'fin', 'tk_punto', 'retorna', 'tk_potenciacion', 'tk_mayor_igual', 'tk_distinto_de', 'tk_menor_igual', 'desde', 'tk_menor', 'tk_parentesis_derecho', 'tk_punto_y_coma', 'inicio', 'tk_division', 'tk_coma', 'paso'}))


def variable():
	if(token == 'tk_numero'):
		emparejar('tk_numero')
	elif(token == 'tk_cadena'):
		emparejar('tk_cadena')
	elif(token == 'TRUE'):
		emparejar('TRUE')
	elif(token == 'FALSE'):
		emparejar('FALSE')
	elif(token == 'SI'):
		emparejar('SI')
	elif(token == 'NO'):
		emparejar('NO')
	elif(token == 'tk_suma' or token == 'tk_resta'):
		signo()
		variable_aux()
	else:
		syntaxError(set({'tk_numero', 'FALSE', 'tk_suma', 'tk_cadena', 'tk_resta', 'TRUE', 'SI', 'NO'}))


def variable_aux():
	if(token == 'id'):
		emparejar('id')
	elif(token == 'tk_numero'):
		emparejar('tk_numero')
	else:
		syntaxError(set({'id', 'tk_numero'}))


def signo():
	if(token == 'tk_suma'):
		emparejar('tk_suma')
	elif(token == 'tk_resta'):
		emparejar('tk_resta')
	else:
		syntaxError(set({'tk_suma', 'tk_resta'}))


def otros_id():
	if(token == 'tk_coma'):
		emparejar('tk_coma')
		emparejar('id')
		otros_id()
	elif(token == 'tk_dos_puntos'):
		pass
	else:
		syntaxError(set({'tk_coma', 'tk_dos_puntos'}))


def tipo_dato():
	if(token == 'id'):
		emparejar('id')
	elif(token == 'cadena'):
		emparejar('cadena')
	elif(token == 'logico'):
		emparejar('logico')
	elif(token == 'numerico'):
		emparejar('numerico')
	elif(token == 'registro'):
		emparejar('registro')
		emparejar('tk_llave_izquierda')
		declaracion_contenido_var()
		emparejar('tk_llave_derecha')
	elif(token == 'vector'):
		emparejar('vector')
		emparejar('tk_corchete_izquierdo')
		tamano_arreglo()
		emparejar('tk_corchete_derecho')
		tipo_dato()
	elif(token == 'matriz'):
		emparejar('matriz')
		emparejar('tk_corchete_izquierdo')
		tamano_arreglo()
		mas_tamano_arreglo()
		emparejar('tk_corchete_derecho')
		tipo_dato()
	else:
		syntaxError(set({'id', 'cadena', 'matriz', 'logico', 'numerico', 'registro', 'vector'}))


def tamano_arreglo():
	if(token == 'tk_numero'):
		emparejar('tk_numero')
	elif(token == 'tk_multiplicacion'):
		emparejar('tk_multiplicacion')
	elif(token == 'id'):
		emparejar('id')
	else:
		syntaxError(set({'tk_numero', 'tk_multiplicacion', 'id'}))


def mas_tamano_arreglo():
	if(token == 'tk_coma'):
		emparejar('tk_coma')
		tamano_arreglo()
		mas_tamano_arreglo()
	elif(token == 'tk_corchete_derecho'):
		pass
	else:
		syntaxError(set({'tk_corchete_derecho', 'tk_coma'}))


def mas_declaraciones_var():
	if(token == 'id' or token == 'tk_punto_y_coma'):
		punto_y_coma_opcional()
		declaracion_contenido_var()
	elif(token == 'tk_llave_derecha' or token == 'inicio' or token == 'const' or token == 'var' or token == 'tipos'):
		pass
	else:
		syntaxError(set({'id', 'tk_punto_y_coma', 'inicio', 'const', 'tk_llave_derecha', 'var', 'tipos'}))


def mas_declaraciones_tipos():
	if(token == 'id' or token == 'tk_punto_y_coma'):
		punto_y_coma_opcional()
		declaracion_contenido_tipos()
	elif(token == 'const' or token == 'inicio' or token == 'var' or token == 'tipos'):
		pass
	else:
		syntaxError(set({'id', 'tk_punto_y_coma', 'inicio', 'const', 'var', 'tipos'}))


def mas_declaraciones_const():
	if(token == 'id' or token == 'tk_punto_y_coma'):
		punto_y_coma_opcional()
		declaracion_contenido_const()
	elif(token == 'const' or token == 'inicio' or token == 'var' or token == 'tipos'):
		pass
	else:
		syntaxError(set({'id', 'tk_punto_y_coma', 'inicio', 'const', 'var', 'tipos'}))


def main():
	if(token == 'inicio'):
		emparejar('inicio')
		sentencias()
		emparejar('fin')
	else:
		syntaxError(set({'inicio'}))


def sentencias():
	if(token == 'id' or token == 'eval' or token == 'mientras' or token == 'desde' or token == 'repetir' or token == 'si'):
		sentencia()
		sentencias_aux()
	elif(token == 'fin'):
		pass
	else:
		syntaxError(set({'id', 'mientras', 'desde', 'repetir', 'eval', 'si', 'fin'}))


def sentencias_aux():
	if(token == 'id' or token == 'mientras' or token == 'tk_punto_y_coma' or token == 'desde' or token == 'repetir' or token == 'eval' or token == 'si' or token == 'fin'):
		punto_y_coma_opcional()
		sentencias()
	elif(token == 'fin' or token == 'retorna'):
		sentencia_retorna_main()
	else:
		syntaxError(set({'id', 'tk_punto_y_coma', 'eval', 'fin', 'mientras', 'retorna', 'desde', 'repetir', 'si'}))


def sentencia():
	if(token == 'id'):
		emparejar('id')
		id_casos()
	elif(token == 'si'):
		condicional()
	elif(token == 'mientras'):
		ciclo_mientras()
	elif(token == 'eval'):
		sentencia_eval()
	elif(token == 'desde'):
		ciclo_desde()
	elif(token == 'repetir'):
		ciclo_repetir()
	else:
		syntaxError(set({'id', 'mientras', 'desde', 'repetir', 'eval', 'si'}))


def sentencias_internas():
	if(token == 'id' or token == 'eval' or token == 'mientras' or token == 'desde' or token == 'repetir' or token == 'si'):
		sentencia_interna()
		punto_y_coma_opcional()
		sentencias_internas()
	elif(token == 'hasta' or token == 'caso' or token == 'tk_llave_derecha' or token == 'sino'):
		pass
	else:
		syntaxError(set({'id', 'caso', 'sino', 'tk_llave_derecha', 'eval', 'mientras', 'desde', 'repetir', 'hasta', 'si'}))


def sentencia_interna():
	if(token == 'id'):
		emparejar('id')
		id_casos()
	elif(token == 'si'):
		condicional()
	elif(token == 'mientras'):
		ciclo_mientras()
	elif(token == 'eval'):
		sentencia_eval()
	elif(token == 'desde'):
		ciclo_desde()
	elif(token == 'repetir'):
		ciclo_repetir()
	else:
		syntaxError(set({'id', 'mientras', 'desde', 'repetir', 'eval', 'si'}))


def id_casos():
	if(token == 'tk_asignacion'):
		asignacion()
	elif(token == 'tk_parentesis_izquierdo'):
		llamada_subrutina()
	elif(token == 'tk_corchete_izquierdo' or token == 'tk_punto'):
		id_arreglo_registro()
		asignacion()
	else:
		syntaxError(set({'tk_parentesis_izquierdo', 'tk_asignacion', 'tk_corchete_izquierdo', 'tk_punto'}))


def punto_y_coma_opcional():
	if(token == 'tk_punto_y_coma'):
		emparejar('tk_punto_y_coma')
	elif(token == 'id' or token == 'caso' or token == 'sino' or token == 'tk_llave_derecha' or token == 'eval' or token == 'fin' or token == 'mientras' or token == 'desde' or token == 'repetir' or token == 'hasta' or token == 'si'):
		pass
	else:
		syntaxError(set({'id', 'tk_punto_y_coma', 'caso', 'sino', 'tk_llave_derecha', 'eval', 'fin', 'mientras', 'desde', 'repetir', 'hasta', 'si'}))


def expresion():
	if(token == 'tk_numero' or token == 'tk_suma' or token == 'tk_cadena' or token == 'tk_resta' or token == 'TRUE' or token == 'SI' or token == 'NO' or token == 'FALSE'):
		variable()
		expresion_aux()
	elif(token == 'tk_parentesis_izquierdo'):
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		expresion_aux()
	elif(token == 'not'):
		emparejar('not')
		expresion()
		expresion_aux()
	elif(token == 'id'):
		emparejar('id')
		valor_aux()
		expresion_aux()
	elif(token == 'tk_llave_izquierda'):
		valores_vector()
		expresion_aux()
	else:
		syntaxError(set({'tk_numero', 'tk_suma', 'not', 'id', 'tk_llave_izquierda', 'tk_cadena', 'tk_resta', 'TRUE', 'SI', 'NO', 'FALSE', 'tk_parentesis_izquierdo'}))


def expresion_aux():
	if(token == 'tk_suma' or token == 'tk_menor' or token == 'tk_igual_que' or token == 'tk_resta' or token == 'tk_mayor' or token == 'tk_multiplicacion' or token == 'tk_menor_igual' or token == 'or' or token == 'tk_potenciacion' or token == 'tk_mayor_igual' or token == 'tk_distinto_de' or token == 'tk_division' or token == 'and' or token == 'tk_modulo'):
		operador()
		expresion()
	elif(token == 'tk_suma' or token == 'tk_igual_que' or token == 'caso' or token == 'paso' or token == 'mientras' or token == 'tk_multiplicacion' or token == 'or' or token == 'hasta' or token == 'const' or token == 'var' or token == 'id' or token == 'tk_mayor' or token == 'tk_llave_derecha' or token == 'eval' or token == 'repetir' or token == 'and' or token == 'si' or token == 'tipos' or token == 'tk_llave_izquierda' or token == 'tk_corchete_derecho' or token == 'sino' or token == 'tk_resta' or token == 'fin' or token == 'retorna' or token == 'tk_potenciacion' or token == 'tk_mayor_igual' or token == 'tk_distinto_de' or token == 'tk_menor_igual' or token == 'desde' or token == 'tk_parentesis_derecho' or token == 'tk_menor' or token == 'tk_punto_y_coma' or token == 'inicio' or token == 'tk_division' or token == 'tk_coma' or token == 'tk_modulo'):
		pass
	else:
		syntaxError(set({'tk_suma', 'tk_igual_que', 'caso', 'paso', 'mientras', 'tk_multiplicacion', 'or', 'hasta', 'const', 'var', 'id', 'tk_mayor', 'tk_llave_derecha', 'eval', 'repetir', 'and', 'si', 'tipos', 'tk_llave_izquierda', 'tk_corchete_derecho', 'sino', 'tk_resta', 'fin', 'retorna', 'tk_potenciacion', 'tk_mayor_igual', 'tk_menor_igual', 'tk_distinto_de', 'desde', 'tk_menor', 'tk_parentesis_derecho', 'tk_punto_y_coma', 'inicio', 'tk_division', 'tk_coma', 'tk_modulo'}))


def valores_vector():
	if(token == 'tk_llave_izquierda'):
		emparejar('tk_llave_izquierda')
		posibles_valores_vector()
		mas_valores_vector()
		emparejar('tk_llave_derecha')
	else:
		syntaxError(set({'tk_llave_izquierda'}))


def posibles_valores_vector():
	if(token == 'id' or token == 'tk_numero' or token == 'tk_suma' or token == 'tk_cadena' or token == 'tk_resta' or token == 'TRUE' or token == 'SI' or token == 'NO' or token == 'FALSE'):
		valor()
	elif(token == 'tk_llave_izquierda'):
		valores_vector()
	elif(token == 'tk_llave_derecha' or token == 'tk_coma'):
		pass
	else:
		syntaxError(set({'id', 'tk_numero', 'tk_suma', 'tk_llave_izquierda', 'tk_cadena', 'tk_resta', 'tk_llave_derecha', 'TRUE', 'SI', 'NO', 'FALSE', 'tk_coma'}))


def mas_valores_vector():
	if(token == 'tk_coma'):
		emparejar('tk_coma')
		posibles_valores_vector()
		mas_valores_vector()
	elif(token == 'tk_llave_derecha'):
		pass
	else:
		syntaxError(set({'tk_llave_derecha', 'tk_coma'}))


def id_arreglo_registro():
	if(token == 'tk_corchete_izquierdo'):
		emparejar('tk_corchete_izquierdo')
		expresion()
		mas_parametros()
		emparejar('tk_corchete_derecho')
		mas_pos_valor()
	elif(token == 'tk_punto'):
		emparejar('tk_punto')
		emparejar('id')
		mas_pos_valor()
	else:
		syntaxError(set({'tk_corchete_izquierdo', 'tk_punto'}))


def mas_pos_valor():
	if(token == 'tk_corchete_izquierdo' or token == 'tk_punto'):
		id_arreglo_registro()
	elif(token == 'tk_suma' or token == 'tk_igual_que' or token == 'caso' or token == 'paso' or token == 'mientras' or token == 'tk_multiplicacion' or token == 'or' or token == 'hasta' or token == 'const' or token == 'tk_asignacion' or token == 'var' or token == 'id' or token == 'tk_llave_derecha' or token == 'tk_mayor' or token == 'eval' or token == 'repetir' or token == 'and' or token == 'si' or token == 'tipos' or token == 'tk_llave_izquierda' or token == 'tk_corchete_derecho' or token == 'sino' or token == 'tk_resta' or token == 'fin' or token == 'retorna' or token == 'tk_potenciacion' or token == 'tk_mayor_igual' or token == 'tk_distinto_de' or token == 'tk_menor_igual' or token == 'desde' or token == 'tk_menor' or token == 'tk_parentesis_derecho' or token == 'tk_punto_y_coma' or token == 'inicio' or token == 'tk_division' or token == 'tk_coma' or token == 'tk_modulo'):
		pass
	else:
		syntaxError(set({'tk_suma', 'tk_igual_que', 'caso', 'mientras', 'tk_multiplicacion', 'or', 'tk_corchete_izquierdo', 'hasta', 'const', 'tk_asignacion', 'var', 'tk_modulo', 'id', 'tk_llave_derecha', 'tk_mayor', 'eval', 'repetir', 'and', 'si', 'tipos', 'tk_llave_izquierda', 'tk_corchete_derecho', 'sino', 'tk_resta', 'fin', 'tk_punto', 'retorna', 'tk_potenciacion', 'tk_mayor_igual', 'tk_distinto_de', 'tk_menor_igual', 'desde', 'tk_menor', 'tk_parentesis_derecho', 'tk_punto_y_coma', 'inicio', 'tk_division', 'tk_coma', 'paso'}))


def operador():
	if(token == 'tk_modulo'):
		emparejar('tk_modulo')
	elif(token == 'tk_multiplicacion'):
		emparejar('tk_multiplicacion')
	elif(token == 'tk_potenciacion'):
		emparejar('tk_potenciacion')
	elif(token == 'tk_resta'):
		emparejar('tk_resta')
	elif(token == 'tk_suma'):
		emparejar('tk_suma')
	elif(token == 'tk_division'):
		emparejar('tk_division')
	elif(token == 'tk_igual_que'):
		emparejar('tk_igual_que')
	elif(token == 'tk_menor'):
		emparejar('tk_menor')
	elif(token == 'tk_distinto_de'):
		emparejar('tk_distinto_de')
	elif(token == 'tk_menor_igual'):
		emparejar('tk_menor_igual')
	elif(token == 'tk_mayor'):
		emparejar('tk_mayor')
	elif(token == 'tk_mayor_igual'):
		emparejar('tk_mayor_igual')
	elif(token == 'and'):
		emparejar('and')
	elif(token == 'or'):
		emparejar('or')
	else:
		syntaxError(set({'tk_suma', 'tk_menor', 'tk_igual_que', 'tk_resta', 'tk_mayor', 'tk_multiplicacion', 'tk_menor_igual', 'or', 'tk_potenciacion', 'tk_mayor_igual', 'tk_distinto_de', 'tk_division', 'and', 'tk_modulo'}))


def asignacion():
	if(token == 'tk_asignacion'):
		emparejar('tk_asignacion')
		expresion()
	else:
		syntaxError(set({'tk_asignacion'}))


def condicional():
	if(token == 'si'):
		emparejar('si')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		emparejar('tk_llave_izquierda')
		sentencias_internas()
		mas_condicionales()
		emparejar('tk_llave_derecha')
	else:
		syntaxError(set({'si'}))


def mas_condicionales():
	if(token == 'sino'):
		emparejar('sino')
		condicional_()
	elif(token == 'tk_llave_derecha'):
		pass
	else:
		syntaxError(set({'sino', 'tk_llave_derecha'}))


def condicional_():
	if(token == 'si'):
		emparejar('si')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		sentencias_internas()
		mas_condicionales()
	elif(token == 'id' or token == 'mientras' or token == 'desde' or token == 'repetir' or token == 'tk_llave_derecha' or token == 'eval' or token == 'si'):
		sentencias_internas()
	elif(token == 'tk_llave_derecha'):
		pass
	else:
		syntaxError(set({'id', 'mientras', 'desde', 'repetir', 'tk_llave_derecha', 'eval', 'si'}))


def ciclo_mientras():
	if(token == 'mientras'):
		emparejar('mientras')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		emparejar('tk_llave_izquierda')
		sentencias_internas()
		emparejar('tk_llave_derecha')
	else:
		syntaxError(set({'mientras'}))


def sentencia_eval():
	if(token == 'eval'):
		emparejar('eval')
		emparejar('tk_llave_izquierda')
		emparejar('caso')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		sentencias_internas()
		mas_casos_eval()
		emparejar('tk_llave_derecha')
	else:
		syntaxError(set({'eval'}))


def mas_casos_eval():
	if(token == 'caso'):
		emparejar('caso')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
		sentencias_internas()
		mas_casos_eval()
	elif(token == 'sino'):
		emparejar('sino')
		sentencias_internas()
	elif(token == 'tk_llave_derecha'):
		pass
	else:
		syntaxError(set({'caso', 'sino', 'tk_llave_derecha'}))


def ciclo_desde():
	if(token == 'desde'):
		emparejar('desde')
		emparejar('id')
		emparejar('tk_asignacion')
		expresion()
		emparejar('hasta')
		expresion()
		paso_opt()
		emparejar('tk_llave_izquierda')
		sentencias_internas()
		emparejar('tk_llave_derecha')
	else:
		syntaxError(set({'desde'}))


def paso_opt():
	if(token == 'paso'):
		emparejar('paso')
		expresion()
	elif(token == 'tk_llave_izquierda'):
		pass
	else:
		syntaxError(set({'tk_llave_izquierda', 'paso'}))


def llamada_subrutina():
	if(token == 'tk_parentesis_izquierdo'):
		emparejar('tk_parentesis_izquierdo')
		parametros()
		emparejar('tk_parentesis_derecho')
	else:
		syntaxError(set({'tk_parentesis_izquierdo'}))


def parametros():
	if(token == 'tk_numero' or token == 'tk_suma' or token == 'not' or token == 'id' or token == 'tk_llave_izquierda' or token == 'tk_cadena' or token == 'tk_resta' or token == 'TRUE' or token == 'SI' or token == 'NO' or token == 'FALSE' or token == 'tk_parentesis_izquierdo'):
		expresion()
		mas_parametros()
	elif(token == 'tk_parentesis_derecho'):
		pass
	else:
		syntaxError(set({'tk_numero', 'tk_suma', 'not', 'id', 'tk_llave_izquierda', 'tk_parentesis_derecho', 'tk_cadena', 'tk_resta', 'TRUE', 'SI', 'NO', 'FALSE', 'tk_parentesis_izquierdo'}))


def mas_parametros():
	if(token == 'tk_coma'):
		emparejar('tk_coma')
		expresion()
		mas_parametros()
	elif(token == 'tk_parentesis_derecho' or token == 'tk_corchete_derecho'):
		pass
	else:
		syntaxError(set({'tk_parentesis_derecho', 'tk_coma', 'tk_corchete_derecho'}))


def sentencia_retorna_subrutina():
	if(token == 'retorna'):
		emparejar('retorna')
		valor_retorno()
	elif(token == 'tipos' or token == 'const' or token == 'var' or token == 'inicio'):
		pass
	else:
		syntaxError(set({'retorna', 'inicio', 'const', 'var', 'tipos'}))


def sentencia_retorna_main():
	if(token == 'retorna'):
		emparejar('retorna')
		valor_retorno()
	elif(token == 'fin'):
		pass
	else:
		syntaxError(set({'fin', 'retorna'}))


def valor_retorno():
	if(token == 'tk_parentesis_izquierdo'):
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
	elif(token == 'tk_numero' or token == 'tk_suma' or token == 'not' or token == 'id' or token == 'tk_llave_izquierda' or token == 'tk_cadena' or token == 'tk_resta' or token == 'TRUE' or token == 'SI' or token == 'NO' or token == 'FALSE' or token == 'tk_parentesis_izquierdo'):
		expresion()
	elif(token == 'id' or token == 'matriz' or token == 'logico' or token == 'numerico' or token == 'registro' or token == 'cadena' or token == 'vector'):
		tipo_dato()
	else:
		syntaxError(set({'tk_numero', 'tk_suma', 'tk_llave_izquierda', 'matriz', 'logico', 'tk_cadena', 'tk_resta', 'numerico', 'SI', 'FALSE', 'id', 'not', 'registro', 'TRUE', 'NO', 'cadena', 'vector', 'tk_parentesis_izquierdo'}))


def ciclo_repetir():
	if(token == 'repetir'):
		emparejar('repetir')
		sentencias_internas()
		emparejar('hasta')
		emparejar('tk_parentesis_izquierdo')
		expresion()
		emparejar('tk_parentesis_derecho')
	else:
		syntaxError(set({'repetir'}))


def subrutina_():
	if(token == 'subrutina'):
		emparejar('subrutina')
		emparejar('id')
		emparejar('tk_parentesis_izquierdo')
		param_subrutina()
		emparejar('tk_parentesis_derecho')
		sentencia_retorna_subrutina()
		declaracion()
		main()
		subrutina_()
	elif(token == '$'):
		pass
	else:
		syntaxError(set({'subrutina', '$'}))


def param_subrutina():
	if(token == 'id' or token == 'ref'):
		param_ref()
		emparejar('id')
		otros_id()
		emparejar('tk_dos_puntos')
		tipo_dato()
		mas_param_subrutina()
	elif(token == 'tk_parentesis_derecho'):
		pass
	else:
		syntaxError(set({'id', 'tk_parentesis_derecho', 'ref'}))


def mas_param_subrutina():
	if(token == 'tk_parentesis_derecho' or token == 'tk_punto_y_coma'):
		punto_y_coma_opcional_subrutina()
	else:
		syntaxError(set({'tk_parentesis_derecho', 'tk_punto_y_coma'}))


def punto_y_coma_opcional_subrutina():
	if(token == 'tk_punto_y_coma'):
		emparejar('tk_punto_y_coma')
		param_ref()
		emparejar('id')
		otros_id()
		emparejar('tk_dos_puntos')
		tipo_dato()
		mas_param_subrutina()
	elif(token == 'tk_parentesis_derecho'):
		pass
	else:
		syntaxError(set({'tk_parentesis_derecho', 'tk_punto_y_coma'}))


def param_ref():
	if(token == 'ref'):
		emparejar('ref')
	elif(token == 'id'):
		pass
	else:
		syntaxError(set({'id', 'ref'}))


init()
