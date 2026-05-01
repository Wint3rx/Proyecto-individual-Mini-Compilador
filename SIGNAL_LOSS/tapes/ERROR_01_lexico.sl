// ─────────────────────────────────────────
//  ERROR_01.sl — Caracteres ilegales
//  Errores LÉXICOS: @, #, $, ?
// ─────────────────────────────────────────
RECORD {
    FREQ canal@ = 432;        // @ no es un carácter válido
    FREQ nivel  = 10 # 5;     // # no es operador en SIGNAL_LOSS
    VHS  msg    = $"LOST";    // $ no existe en el lenguaje
    FREQ result = canal? + 1; // ? no es válido
}
STOP
