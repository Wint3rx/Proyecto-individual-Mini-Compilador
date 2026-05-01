// ─────────────────────────────────────────
//  ERROR_02.sl — Puntuación faltante
//  Errores SINTÁCTICOS: falta ; y { }
// ─────────────────────────────────────────
RECORD {
    FREQ canal = 432       // falta ; al final
    FREQ nivel = 10;

    MANDELA (canal > 100)  // falta { para abrir el bloque
        PLAYBACK(canal);
    }

    LOOP_TAPE canal > 0 {  // falta ( ) en la condición
        canal = canal - 1;
    }
}
STOP
