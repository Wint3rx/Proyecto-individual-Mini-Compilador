// ─────────────────────────────────────────
//  TAPE_03.sl — Función de amplificación
//  Usa: ARCHIVE, REWIND, FREQ, DISTORT
// ─────────────────────────────────────────
ARCHIVE amplificar(senal, factor) {
    DISTORT resultado = senal * factor;
    REWIND resultado;
}

RECORD {
    FREQ    entrada  = 120;
    DISTORT ganancia = 1.5;
    FREQ    ciclos   = 3;

    LOOP_TAPE (ciclos > 0) {
        amplificar(entrada, ganancia);
        ciclos = ciclos - 1;
    }
    PLAYBACK (ciclos);
}
STOP
