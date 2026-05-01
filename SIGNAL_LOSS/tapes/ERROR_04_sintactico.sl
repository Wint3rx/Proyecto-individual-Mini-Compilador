// ─────────────────────────────────────────
//  ERROR_04.sl — Estructura de bloques rota
//  Errores SINTÁCTICOS: bloques sin cerrar,
//  ALTERNATE sin MANDELA previo
// ─────────────────────────────────────────
RECORD {
    FREQ canal = 200;

    ALTERNATE {               // ALTERNATE sin MANDELA antes
        PLAYBACK(canal);
    }

    LOOP_TAPE (canal > 0) {
        canal = canal - 1;
                              // falta cerrar } del LOOP_TAPE

    FREQ extra = 5;
}
STOP
