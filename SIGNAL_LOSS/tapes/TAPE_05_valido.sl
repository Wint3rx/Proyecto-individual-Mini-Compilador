// ─────────────────────────────────────────
//  TAPE_05.sl — Sistema de decodificación
// ─────────────────────────────────────────
ARCHIVE decodificar(entrada, clave) {
    FREQ    resultado = entrada - clave;
    DISTORT factor    = resultado * 0.01;
    REWIND factor;
}

ARCHIVE validar(senal) {
    MANDELA (senal > 0) {
        REWIND senal;
    }
    ALTERNATE {
        FREQ error = 0;
        REWIND error;
    }
}

RECORD {
    FREQ    bruto    = 888;
    FREQ    clave    = 456;
    DISTORT ganancia = 2.5;
    VHS     modo     = "DECODE_MODE";
    STATIC  version  = 2;

    PLAYBACK(modo);

    FREQ limpio = bruto - clave;

    MANDELA (limpio > 0) {
        decodificar(bruto, clave);
        PLAYBACK(limpio);
    }

    FREQ i = 0;
    LOOP_TAPE (i < version) {
        validar(limpio);
        i = i + 1;
    }

    PLAYBACK(version);
}
STOP
