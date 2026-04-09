import ply.lex as lex

# Lista de tokens obligatorios
tokens = [
    'ID', 'NUMBER', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'EQUALS',
    'GREATER', 'LESS'
]

# Diccionario de palabras reservadas
reserved = {
    'RECORD': 'RECORD', 'STOP': 'STOP', 'FREQ': 'FREQ',
    'DISTORT': 'DISTORT', 'VHS': 'VHS', 'PULSE': 'PULSE',
    'PLAYBACK': 'PLAYBACK', 'INTERCEPT': 'INTERCEPT',
    'MANDELA': 'MANDELA', 'ALTERNATE': 'ALTERNATE',
    'LOOP_TAPE': 'LOOP_TAPE', 'STATIC': 'STATIC',
    'ENCRYPT': 'ENCRYPT', 'REWIND': 'REWIND', 'ARCHIVE': 'ARCHIVE'
}

tokens += list(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_EQUALS    = r'='
t_GREATER   = r'>'
t_LESS      = r'<'

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# Números (Diferenciando Flotantes de Enteros)
def t_FLOAT_VAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Cadenas de texto (VHS)
def t_STRING_VAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1] # Quita las comillas
    return t

# Rastreo de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para calcular la columna
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# 5. Manejo de Errores Léxicos
error_list = []

def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    error_info = {
        "tipo": "Léxico",
        "linea": t.lexer.lineno,
        "columna": col,
        "descripcion": f"Carácter ilegal '{t.value[0]}'",
        "causa": "Símbolo no reconocido por el lenguaje SIGNAL_LOSS"
    }
    error_list.append(error_info)
    t.lexer.skip(1)

# Constructor del lexer
lexer = lex.lex()