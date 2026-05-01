// ─────────────────────────────────────────
//  TAPE_04.sl — Monitor de interferencia
//  Usa: FREQ, VHS, PULSE, STATIC, MANDELA anidado
// ─────────────────────────────────────────
RECORD {
    FREQ    canal      = 432;
    FREQ    umbral_alto = 500;
    FREQ    umbral_bajo = 100;
    VHS     alerta     = "INTERFERENCE_DETECTED";
    STATIC  limite     = 999;

    MANDELA (canal > umbral_bajo) {
        MANDELA (canal > umbral_alto) {
            PLAYBACK(limite);
        }
        ALTERNATE {
            PLAYBACK(canal);
        }
    }
    ALTERNATE {
        PLAYBACK(alerta);
    }

    LOOP_TAPE (canal < umbral_alto) {
        canal = canal + 10;
        PLAYBACK(canal);
    }
}
STOP
