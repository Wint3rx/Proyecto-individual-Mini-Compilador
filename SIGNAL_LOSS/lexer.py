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

# Manejo de errores léxicos
def t_error(t):
    print(f"Error léxico: Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

