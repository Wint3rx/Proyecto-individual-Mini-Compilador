// ─────────────────────────────────────────
//  ERROR_03.sl — Mezcla léxico + sintáctico
//  Errores: carácter ilegal Y estructura rota
// ─────────────────────────────────────────
RECORD {
    FREQ señal = 100;          // ñ no es válido en identificadores
    DISTORT nivel@ = 3.14;     // @ carácter ilegal

    MANDELA (señal > 50) {
        PLAYBACK(nivel@);      // doble error: ID inválido
    }

    ARCHIVE {                  // falta el nombre de la función y parámetros
        FREQ x = 1;
    }
}
STOP
