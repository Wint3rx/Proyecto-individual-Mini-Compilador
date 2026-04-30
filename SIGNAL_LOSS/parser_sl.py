import ply.yacc as yacc
from lexer import tokens, lexer, error_list, find_column

#  SIGNAL_LOSS — Parser v1.0
#  Implementa ply.yacc con árbol de derivación (nodos dict)
#
#  Nodo estándar: {"tipo": str, "linea": int, "hijos": [...]}
#  Los nodos hoja añaden "valor" en lugar de "hijos"

# ══════════════════════════════════════════════════════════════
#  LISTA DE ERRORES SINTÁCTICOS
# ══════════════════════════════════════════════════════════════

syntax_error_list = []

def _nodo(tipo, linea, **kwargs):
    """Crea un nodo del árbol de derivación."""
    n = {"tipo": tipo, "linea": linea}
    n.update(kwargs)
    return n


# ══════════════════════════════════════════════════════════════
#  PRECEDENCIA DE OPERADORES
# ══════════════════════════════════════════════════════════════

precedence = (
    ('left',  'DOUBLE_EQ', 'NOT_EQ'),
    ('left',  'GREATER', 'LESS', 'GREATER_EQ', 'LESS_EQ'),
    ('left',  'PLUS', 'MINUS'),
    ('left',  'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


# ══════════════════════════════════════════════════════════════
#  REGLAS DE GRAMÁTICA — BNF
# ══════════════════════════════════════════════════════════════

# ── programa ─────────────────────────────────────────────────
# programa → RECORD { lista_sentencias } STOP
def p_programa(p):
    '''programa : lista_funciones_globales RECORD LBRACE lista_sentencias RBRACE STOP
               | lista_funciones_globales RECORD LBRACE lista_sentencias RBRACE
               | RECORD LBRACE lista_sentencias RBRACE STOP
               | RECORD LBRACE lista_sentencias RBRACE'''
    # Si hay funciones globales antes de RECORD, p[1] es la lista; sino p[1]=RECORD
    if p[1] == 'RECORD':
        funciones = []
        cuerpo = p[3]
    else:
        funciones = p[1]
        cuerpo = p[4]
    p[0] = _nodo("PROGRAMA", p.lineno(1), funciones=funciones, cuerpo=cuerpo)

def p_lista_funciones_globales_vacia(p):
    '''lista_funciones_globales : '''
    p[0] = []

def p_lista_funciones_globales(p):
    '''lista_funciones_globales : lista_funciones_globales def_funcion'''
    p[0] = p[1] + [p[2]]

# ── lista de sentencias ──────────────────────────────────────
def p_lista_sentencias_vacia(p):
    '''lista_sentencias : '''
    p[0] = []

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia'''
    p[0] = p[1] + [p[2]]


# ══════════════════════════════════════════════════════════════
#  SENTENCIAS
# ══════════════════════════════════════════════════════════════

def p_sentencia(p):
    '''sentencia : declaracion
                 | asignacion
                 | condicional
                 | bucle_while
                 | def_funcion
                 | llamada_playback
                 | llamada_intercept
                 | retorno
                 | llamada_funcion_stmt'''
    p[0] = p[1]


def p_sentencia_error(p):
    '''sentencia : error SEMICOLON'''
    p[0] = None


def p_lista_sentencias_error(p):
    '''lista_sentencias : lista_sentencias error SEMICOLON'''
    p[0] = p[1]


# ── Declaración de variable ──────────────────────────────────
# TIPO ID = expresion ;
def p_declaracion(p):
    '''declaracion : FREQ    ID EQUALS expresion SEMICOLON
                   | DISTORT ID EQUALS expresion SEMICOLON
                   | VHS     ID EQUALS expresion SEMICOLON
                   | PULSE   ID EQUALS expresion SEMICOLON
                   | ENCRYPT ID EQUALS expresion SEMICOLON
                   | STATIC  ID EQUALS expresion SEMICOLON'''
    p[0] = _nodo("DECLARACION", p.lineno(1),
                 tipo_dato=p[1], nombre=p[2], valor=p[4])


# ── Asignación ───────────────────────────────────────────────
# ID = expresion ;
def p_asignacion(p):
    '''asignacion : ID EQUALS expresion SEMICOLON'''
    p[0] = _nodo("ASIGNACION", p.lineno(1), nombre=p[1], valor=p[3])


# ── REWIND: resetear variable ────────────────────────────────
# REWIND ID ;
def p_retorno(p):
    '''retorno : REWIND expresion SEMICOLON'''
    p[0] = _nodo("RETORNO", p.lineno(1), valor=p[2])


# ── Condicional ──────────────────────────────────────────────
# MANDELA ( expresion ) { lista_sentencias }
# MANDELA ( expresion ) { lista_sentencias } ALTERNATE { lista_sentencias }
def p_condicional_if(p):
    '''condicional : MANDELA LPAREN expresion RPAREN LBRACE lista_sentencias RBRACE'''
    p[0] = _nodo("CONDICIONAL", p.lineno(1),
                 condicion=p[3], cuerpo_then=p[6], cuerpo_else=[])

def p_condicional_if_else(p):
    '''condicional : MANDELA LPAREN expresion RPAREN LBRACE lista_sentencias RBRACE ALTERNATE LBRACE lista_sentencias RBRACE'''
    p[0] = _nodo("CONDICIONAL", p.lineno(1),
                 condicion=p[3], cuerpo_then=p[6], cuerpo_else=p[10])


# ── Bucle LOOP_TAPE (while) ──────────────────────────────────
# LOOP_TAPE ( expresion ) { lista_sentencias }
def p_bucle_while(p):
    '''bucle_while : LOOP_TAPE LPAREN expresion RPAREN LBRACE lista_sentencias RBRACE'''
    p[0] = _nodo("BUCLE", p.lineno(1), condicion=p[3], cuerpo=p[6])


# ── Definición de función (ARCHIVE) ──────────────────────────
# ARCHIVE ID ( params ) { lista_sentencias }
def p_def_funcion(p):
    '''def_funcion : ARCHIVE ID LPAREN lista_params RPAREN LBRACE lista_sentencias RBRACE'''
    p[0] = _nodo("DEF_FUNCION", p.lineno(1),
                 nombre=p[2], parametros=p[4], cuerpo=p[7])


# ── Parámetros de función ────────────────────────────────────
def p_lista_params_vacia(p):
    '''lista_params : '''
    p[0] = []

def p_lista_params_uno(p):
    '''lista_params : ID'''
    p[0] = [p[1]]

def p_lista_params_varios(p):
    '''lista_params : lista_params COMMA ID'''
    p[0] = p[1] + [p[3]]


# ── PLAYBACK (salida / print) ────────────────────────────────
# PLAYBACK ( expresion ) ;
def p_llamada_playback(p):
    '''llamada_playback : PLAYBACK LPAREN expresion RPAREN SEMICOLON'''
    p[0] = _nodo("PLAYBACK", p.lineno(1), argumento=p[3])


# ── INTERCEPT (entrada / input) ──────────────────────────────
# INTERCEPT ( ID ) ;
def p_llamada_intercept(p):
    '''llamada_intercept : INTERCEPT LPAREN ID RPAREN SEMICOLON'''
    p[0] = _nodo("INTERCEPT", p.lineno(1), variable=p[3])


# ── Llamada a función como sentencia ─────────────────────────
# ID ( argumentos ) ;
def p_llamada_funcion_stmt(p):
    '''llamada_funcion_stmt : ID LPAREN lista_args RPAREN SEMICOLON'''
    p[0] = _nodo("LLAMADA_FUNCION", p.lineno(1),
                 nombre=p[1], argumentos=p[3])


# ── Argumentos de llamada ─────────────────────────────────────
def p_lista_args_vacia(p):
    '''lista_args : '''
    p[0] = []

def p_lista_args_uno(p):
    '''lista_args : expresion'''
    p[0] = [p[1]]

def p_lista_args_varios(p):
    '''lista_args : lista_args COMMA expresion'''
    p[0] = p[1] + [p[3]]


# ══════════════════════════════════════════════════════════════
#  EXPRESIONES
# ══════════════════════════════════════════════════════════════

# ── Operaciones binarias ──────────────────────────────────────
def p_expresion_binaria(p):
    '''expresion : expresion PLUS      expresion
                 | expresion MINUS     expresion
                 | expresion TIMES     expresion
                 | expresion DIVIDE    expresion
                 | expresion GREATER   expresion
                 | expresion LESS      expresion
                 | expresion GREATER_EQ expresion
                 | expresion LESS_EQ   expresion
                 | expresion DOUBLE_EQ expresion
                 | expresion NOT_EQ    expresion'''
    p[0] = _nodo("OPERACION", p.lineno(2),
                 operador=p[2], izquierda=p[1], derecha=p[3])

# ── Negación unaria ───────────────────────────────────────────
def p_expresion_uminus(p):
    '''expresion : MINUS expresion %prec UMINUS'''
    p[0] = _nodo("NEGACION", p.lineno(1), operando=p[2])

# ── Agrupación con paréntesis ─────────────────────────────────
def p_expresion_grupo(p):
    '''expresion : LPAREN expresion RPAREN'''
    p[0] = p[2]

# ── Llamada a función como expresión ─────────────────────────
def p_expresion_llamada(p):
    '''expresion : ID LPAREN lista_args RPAREN'''
    p[0] = _nodo("LLAMADA_FUNCION", p.lineno(1),
                 nombre=p[1], argumentos=p[3])

# ── Literales y variables ─────────────────────────────────────
def p_expresion_numero(p):
    '''expresion : NUMBER'''
    p[0] = _nodo("LITERAL", p.lineno(1), tipo_dato="FREQ", valor=p[1])

def p_expresion_float(p):
    '''expresion : FLOAT_VAL'''
    p[0] = _nodo("LITERAL", p.lineno(1), tipo_dato="DISTORT", valor=p[1])

def p_expresion_string(p):
    '''expresion : STRING'''
    p[0] = _nodo("LITERAL", p.lineno(1), tipo_dato="VHS", valor=p[1])

def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = _nodo("VARIABLE", p.lineno(1), nombre=p[1])


# ══════════════════════════════════════════════════════════════
#  MANEJO DE ERRORES SINTÁCTICOS
# ══════════════════════════════════════════════════════════════

def p_error(p):
    if p:
        col = find_column(p.lexer.lexdata, p)
        syntax_error_list.append({
            "tipo":        "Sintáctico",
            "linea":       p.lineno,
            "columna":     col,
            "descripcion": f"Token inesperado '{p.value}' (tipo: {p.type})",
            "causa":       "La estructura del código no cumple con la gramática de SIGNAL_LOSS",
        })
    else:
        syntax_error_list.append({
            "tipo":        "Sintáctico",
            "linea":       "?",
            "columna":     "?",
            "descripcion": "Fin de archivo inesperado",
            "causa":       "El programa está incompleto o le falta cerrar un bloque",
        })


# ══════════════════════════════════════════════════════════════
#  ÁRBOL DE DERIVACIÓN — UTILIDADES
# ══════════════════════════════════════════════════════════════

def arbol_a_texto(nodo, prefijo="", es_ultimo=True):
    """Convierte el árbol a texto con ramas tipo 'tree' para mostrar en la GUI."""
    if nodo is None:
        return ""

    lineas = []
    conector = "└─ " if es_ultimo else "├─ "
    tipo = nodo.get("tipo", "?")
    linea = nodo.get("linea", "")

    # Etiqueta del nodo
    extra = ""
    if tipo == "DECLARACION":
        extra = f" [{nodo.get('tipo_dato')} {nodo.get('nombre')}]"
    elif tipo == "ASIGNACION":
        extra = f" [{nodo.get('nombre')}]"
    elif tipo == "LITERAL":
        extra = f" = {nodo.get('valor')}"
    elif tipo == "VARIABLE":
        extra = f" [{nodo.get('nombre')}]"
    elif tipo == "OPERACION":
        extra = f" [{nodo.get('operador')}]"
    elif tipo in ("DEF_FUNCION", "LLAMADA_FUNCION"):
        extra = f" [{nodo.get('nombre')}]"
    elif tipo == "INTERCEPT":
        extra = f" [{nodo.get('variable')}]"

    lineas.append(f"{prefijo}{conector}{tipo}{extra}  (L:{linea})")

    # Recolectar hijos
    hijos = []
    for campo in ["condicion", "cuerpo_then", "cuerpo_else", "cuerpo",
                  "valor", "argumento", "operando", "izquierda", "derecha",
                  "parametros", "argumentos"]:
        val = nodo.get(campo)
        if val is None:
            continue
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    hijos.append((campo, item))
                # strings (nombres de parámetros)
        elif isinstance(val, dict):
            hijos.append((campo, val))

    extension = "   " if es_ultimo else "│  "
    for i, (_, hijo) in enumerate(hijos):
        ultimo = (i == len(hijos) - 1)
        lineas.append(arbol_a_texto(hijo, prefijo + extension, ultimo))

    return "\n".join(filter(None, lineas))


def arbol_completo_texto(ast):
    """Devuelve el árbol completo como string."""
    if ast is None:
        return "(árbol vacío — hubo errores sintácticos)"
    return arbol_a_texto(ast, "", True)


# ══════════════════════════════════════════════════════════════
#  CONSTRUCTOR DEL PARSER
# ══════════════════════════════════════════════════════════════

parser = yacc.yacc(debug=False, write_tables=False)


# ══════════════════════════════════════════════════════════════
#  FUNCIÓN PÚBLICA
# ══════════════════════════════════════════════════════════════

def parse(codigo):
    """
    Analiza el código fuente y devuelve (ast, errores_sintacticos).
    Reinicia el estado del lexer y la lista de errores antes de parsear.
    """
    from lexer import error_list
    syntax_error_list.clear()
    error_list.clear()
    lexer.lineno = 1
    lexer.input(codigo)
    ast = parser.parse(codigo, lexer=lexer)
    return ast, syntax_error_list
