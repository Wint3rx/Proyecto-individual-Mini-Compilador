# SIGNAL_LOSS
### *A compiler that listens to dead frequencies.*

> *"You are not debugging code. You are recovering a signal that something tried to erase."*

---

## ¿Qué es SIGNAL_LOSS?

SIGNAL_LOSS es un mini-compilador construido desde cero como proyecto individual para el curso de **Compiladores** de la Universidad Mariano Gálvez de Guatemala (2026). Implementa un lenguaje de programación propio con analizador léxico, analizador sintáctico, árbol de derivación y una interfaz gráfica con estética de terminal CRT.

El compilador fue desarrollado en **Python 3** utilizando **PLY** (Python Lex-Yacc) para los analizadores y **CustomTkinter** para la interfaz gráfica.

---

## La Temática: Terror Analógico

La elección de esta temática no fue arbitraria.

El **terror analógico** (*analog horror*) es un subgénero de horror moderno que usa la estética de tecnología obsoleta — cintas VHS, señales de televisión corrompidas, monitores CRT, grabaciones de seguridad — para construir una atmósfera de inquietud y misterio. Obras como **The Mandela Catalogue**, **The Backrooms** y diversas series de found footage en internet son su expresión más reconocida.

La conexión con un compilador es directa y poética: **compilar código es recuperar señal del ruido**. El programador no escribe instrucciones — *intercepta frecuencias*. Los errores no son bugs — *son interferencia estática*. El árbol de derivación no es una estructura de datos — *es la señal decodificada*.

Esta metáfora guió cada decisión de diseño del lenguaje:

| Keyword en SIGNAL_LOSS | Equivalente real | Origen de la metáfora |
|---|---|---|
| `RECORD` / `STOP` | inicio / fin del programa | grabar y detener una VHS |
| `FREQ` | variable entera | frecuencia de señal |
| `DISTORT` | variable decimal | distorsión de la señal |
| `VHS` | variable string | formato de cinta magnética |
| `PULSE` | variable booleana | pulso de señal (on/off) |
| `STATIC` | constante | interferencia estática |
| `ENCRYPT` | variable de solo lectura | señal codificada |
| `MANDELA` | if | Efecto Mandela / realidades alternas |
| `ALTERNATE` | else | la realidad alternativa |
| `LOOP_TAPE` | while | rebobinar y repetir la cinta |
| `ARCHIVE` | función | archivar una grabación |
| `REWIND` | return | rebobinar al punto de origen |
| `PLAYBACK` | print / salida | reproducir la grabación |
| `INTERCEPT` | input / entrada | interceptar una señal externa |

La interfaz gráfica refuerza esta narrativa: fondo negro, texto verde neón, fuente monoespaciada, mensajes de sistema como `SIGNAL DECODED. TREE GENERATED.` y `ANOMALY DETECTED IN SIGNAL.`

---

## Estructura del Proyecto

```
SIGNAL_LOSS/
│
├── lexer.py          # Analizador léxico (ply.lex)
├── parser_sl.py      # Analizador sintáctico (ply.yacc) + árbol de derivación
├── visuals.py        # Interfaz gráfica (CustomTkinter)
│
├── tapes/            # Programas de prueba (.sl)
│   ├── TAPE_01_valido.sl       # Contador regresivo
│   ├── TAPE_02_valido.sl       # Clasificador de señal
│   ├── TAPE_03_valido.sl       # Función de amplificación
│   ├── TAPE_04_valido.sl       # Monitor de interferencia
│   ├── TAPE_05_valido.sl       # Sistema de decodificación completo
│   ├── ERROR_01_lexico.sl      # Errores léxicos puros
│   ├── ERROR_02_sintactico.sl  # Errores sintácticos puros
│   ├── ERROR_03_mixto.sl       # Mezcla de errores
│   ├── ERROR_04_sintactico.sl  # Estructura de bloques rota
│   └── ERROR_05_caos.sl        # Múltiples errores combinados
│
└── README.md
```

---

## Instalación y Ejecución

### Requisitos

- Python 3.10 o superior
- pip

### Instalar dependencias

```bash
pip install ply customtkinter
```

### Ejecutar el compilador

```bash
python visuals.py
```

> No se requiere configuración adicional. El lexer y el parser se inicializan automáticamente al arrancar la GUI.

---

## Cómo usar la interfaz

```
┌─────────────────────────────────────────────────────────┐
│  [ SIGNAL_LOSS v2.0 ]  [ RECORD ] [ EJECT ] [ OPEN ]   │
│                        [ SAVE ] [ EXPORT ] [ SYNTAX ]   │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  -- TAPES -- │         EDITOR DE CÓDIGO                 │
│              │                                          │
│  (archivos   │  Escribe o carga tu programa .sl aquí   │
│   abiertos)  │                                          │
│              ├──────────────────────────────────────────┤
│  -- STATS -- │  [TERMINAL][TOKENS][SYMBOLS][ERRORS][ÁRBOL] │
│  Tokens:  —  │                                          │
│  Symbols: —  │         PANEL DE RESULTADOS              │
│  Errors:  —  │                                          │
└──────────────┴──────────────────────────────────────────┘
```

### Botones

| Botón | Función |
|---|---|
| `[ RECORD ]` | Ejecuta análisis léxico + sintáctico completo |
| `[ EJECT ]` | Limpia el editor y todas las tablas |
| `[ OPEN ]` | Abre un archivo `.sl` desde disco |
| `[ SAVE ]` | Guarda el código actual en disco |
| `[ EXPORT ]` | Exporta las tablas de tokens, símbolos y errores a `.txt` |
| `[ SYNTAX ]` | Ejecuta solo el análisis sintáctico |

### Pestañas de resultados

| Pestaña | Contenido |
|---|---|
| `TERMINAL` | Log de eventos del sistema |
| `TOKENS` | Lista numerada de todos los tokens reconocidos |
| `SYMBOLS` | Tabla de símbolos: nombre, tipo, línea |
| `ERRORS` | Errores léxicos y sintácticos con línea y columna |
| `ÁRBOL` | Árbol de derivación sintáctico en texto |

---

## El Lenguaje SIGNAL_LOSS

### Estructura de un programa

```
RECORD {
    // tu código aquí
}
STOP
```

### Declaración de variables

```
FREQ    canal   = 432;          // entero
DISTORT nivel   = 3.14;         // decimal
VHS     mensaje = "LOST";       // string
PULSE   activo  = 1;            // booleano
STATIC  limite  = 999;          // constante
ENCRYPT clave   = 42;           // solo lectura
```

### Condicional

```
MANDELA (canal > 100) {
    PLAYBACK(canal);
}
ALTERNATE {
    PLAYBACK(mensaje);
}
```

### Ciclo

```
LOOP_TAPE (canal > 0) {
    canal = canal - 1;
}
```

### Funciones

```
ARCHIVE amplificar(senal, factor) {
    DISTORT resultado = senal * factor;
    REWIND resultado;
}
```

### Entrada y salida

```
PLAYBACK(canal);        // imprime en pantalla
INTERCEPT(variable);    // captura entrada del usuario
```

### Comentarios

```
// esto es un comentario de línea
```

### Operadores

```
// Aritméticos
+ - * /

// Comparación
== != > < >= <=

// Asignación
=
```

---

## Arquitectura del Compilador

```
Código fuente (.sl)
        │
        ▼
┌───────────────┐
│   lexer.py    │  ← ply.lex
│               │    tokenización
│   tokens +    │    tabla de símbolos
│   error_list  │    errores léxicos
└───────┬───────┘
        │ flujo de tokens
        ▼
┌───────────────┐
│  parser_sl.py │  ← ply.yacc (LALR(1))
│               │    gramática BNF
│   AST +       │    árbol de derivación
│   syntax_errs │    errores sintácticos
└───────┬───────┘
        │ AST + tablas
        ▼
┌───────────────┐
│  visuals.py   │  ← CustomTkinter
│               │    editor de código
│   GUI con     │    pestañas de resultados
│   5 pestañas  │    exportación
└───────────────┘
```

### Flujo al presionar `[ RECORD ]`

1. Se limpia el estado anterior (error_list, lineno, symbol_table)
2. El lexer recorre el código token por token
3. Los identificadores precedidos de un tipo se registran en la tabla de símbolos
4. Los caracteres ilegales se reportan con línea y columna exacta
5. Si no hay errores léxicos → se ejecuta el parser automáticamente
6. El parser aplica las reglas BNF y construye el árbol de derivación
7. Los errores sintácticos se capturan con línea y columna
8. Los resultados se muestran en las pestañas correspondientes

---

## Palabras Reservadas

| Keyword | Rol |
|---|---|
| `RECORD` | Inicio del bloque principal |
| `STOP` | Fin del bloque principal |
| `FREQ` | Tipo entero |
| `DISTORT` | Tipo decimal |
| `VHS` | Tipo cadena |
| `PULSE` | Tipo booleano |
| `STATIC` | Constante |
| `ENCRYPT` | Solo lectura |
| `MANDELA` | Condicional (if) |
| `ALTERNATE` | Alternativa (else) |
| `LOOP_TAPE` | Ciclo (while) |
| `ARCHIVE` | Declaración de función |
| `REWIND` | Retorno de valor (return) |
| `PLAYBACK` | Salida por pantalla (print) |
| `INTERCEPT` | Entrada del usuario (input) |

---

*The signal was always there. You just needed to know how to listen.*
