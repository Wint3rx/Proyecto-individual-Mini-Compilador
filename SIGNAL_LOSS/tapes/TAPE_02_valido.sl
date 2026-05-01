// ─────────────────────────────────────────
//  TAPE_02.sl — Clasificador de señal
//  Usa: FREQ, DISTORT, MANDELA, ALTERNATE
// ─────────────────────────────────────────
RECORD {
    FREQ    potencia = 75;
    DISTORT nivel    = 0.85;
    VHS     estado   = "UNKNOWN";

    MANDELA (potencia > 50) {
        estado = "STRONG_SIGNAL";
        PLAYBACK(estado);
    }
    ALTERNATE {
        estado = "WEAK_SIGNAL";
        PLAYBACK(estado);
    }

    MANDELA (nivel > 0.5) {
        PLAYBACK(nivel);
    }
}
STOP
