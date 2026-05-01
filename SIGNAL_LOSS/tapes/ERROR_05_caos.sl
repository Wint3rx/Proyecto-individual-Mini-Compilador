// ─────────────────────────────────────────
//  ERROR_05.sl — Caos total
//  Errores: léxicos, sintácticos y estructura
// ─────────────────────────────────────────
RECORD
    FREQ   canal  = 432;      // falta { después de RECORD
    FREQ   nivel% = 10;       // % carácter ilegal
    VHS    msg    = LOST;     // string sin comillas (error léxico/sintáctico)

    MANDELA canal > 100 {     // falta ( ) en condición
        PLAYBACK(canal)       // falta ;
    }

    LOOP_TAPE (nivel > 0) {
        nivel = nivel - 1;
        ARCHIVE inner() {     // función definida dentro de RECORD (estructura inválida)
            FREQ x = nivel * 2!;  // ! carácter ilegal dentro de expresión
        }
    }
STOP
