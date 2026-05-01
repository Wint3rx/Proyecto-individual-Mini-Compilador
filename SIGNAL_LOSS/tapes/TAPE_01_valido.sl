// ─────────────────────────────────────────
//  TAPE_01.sl — Contador regresivo
//  Usa: FREQ, LOOP_TAPE, PLAYBACK
// ─────────────────────────────────────────
RECORD {
    FREQ contador = 10;
    FREQ paso     = 1;

    LOOP_TAPE (contador > 0) {
        PLAYBACK(contador);
        contador = contador - paso;
    }

    PLAYBACK(contador);
}
STOP
