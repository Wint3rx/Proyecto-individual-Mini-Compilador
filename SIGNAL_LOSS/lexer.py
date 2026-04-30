import ply.lex as lex
 
#  SIGNAL_LOSS — Lexer v2.0
#  Bugs corregidos:
#    • FLOAT_VAL y STRING_VAL ahora están en tokens
#    • FLOAT_VAL va ANTES que NUMBER (PLY usa orden de definición)
#    • STRING_VAL renombrado a STRING para coincidir con la lista
#    • t_COMMENT retorna None explícitamente (más limpio)
#    • error_list se reinicia correctamente desde visuals.py
 
# Palabras reservadas
reserved = {
    'RECORD':    'RECORD',      # Inicio del bloque principal
    'STOP':      'STOP',        # Fin del bloque principal
    'FREQ':      'FREQ',        # Tipo numérico  (int/float)
    'VHS':       'VHS',         # Tipo cadena    (string)
    'PULSE':     'PULSE',       # Tipo booleano
    'DISTORT':   'DISTORT',     # Función de salida / print
    'PLAYBACK':  'PLAYBACK',    # Función de entrada / input
    'INTERCEPT': 'INTERCEPT',   # Declaración de función
    'MANDELA':   'MANDELA',     # if
    'ALTERNATE': 'ALTERNATE',   # else
    'LOOP_TAPE': 'LOOP_TAPE',   # while
    'STATIC':    'STATIC',      # constante
    'ENCRYPT':   'ENCRYPT',     # operación especial / cast
    'REWIND':    'REWIND',      # return
    'ARCHIVE':   'ARCHIVE',     # declaración de función
}
 
# Lista de tokens
tokens = [
    # Literales
    'ID', 'NUMBER', 'FLOAT_VAL', 'STRING',
    # Operadores aritméticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # Operadores relacionales
    'EQUALS', 'GREATER', 'LESS',
    'GREATER_EQ', 'LESS_EQ', 'NOT_EQ', 'DOUBLE_EQ',
    # Delimitadores
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA',
] + list(reserved.values())
 
# Reglas simples (orden importa: más específicas primero) ─
t_DOUBLE_EQ  = r'=='
t_NOT_EQ     = r'!='
t_GREATER_EQ = r'>='
t_LESS_EQ    = r'<='
t_GREATER    = r'>'
t_LESS       = r'<'
t_EQUALS     = r'='
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_ignore     = ' \t'
 
# Comentarios (se descartan) 
def t_COMMENT(t):
    r'//.*'
    return None
 
# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t
 
# FLOAT_VAL debe ir ANTES que NUMBER
#  PLY prioriza funciones por longitud de regex;
#  definirlo primero garantiza que 3.14 no se lea como NUMBER "3" + PUNTO + NUMBER "14"
def t_FLOAT_VAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
 
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
 
# Cadenas de texto
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]   # Elimina las comillas externas
    return t
 
# Rastreo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
# Columna de un token
def find_column(source, token):
    line_start = source.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
 
# Manejo de errores léxicos
error_list = []
 
def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    error_list.append({
        "tipo":        "Léxico",
        "linea":       t.lexer.lineno,
        "columna":     col,
        "descripcion": f"Carácter ilegal '{t.value[0]}'",
        "causa":       "Símbolo no reconocido por el lenguaje SIGNAL_LOSS",
    })
    t.lexer.skip(1)
 
# Constructor
lexer = lex.lex()