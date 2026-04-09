from lexer import lexer, error_list, find_column
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("SIGNAL_LOSS - Decoder Terminal")
        self.geometry("1100x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Fonts
        self.font_main = ctk.CTkFont(family="Consolas", size=14, weight="bold")
        self.font_large = ctk.CTkFont(family="Consolas", size=18, weight="bold")
        self.font_small = ctk.CTkFont(family="Consolas", size=12)

        # Colors
        self.bg_color = "#050505"
        self.fg_color = "#00FF41"
        self.dim_fg_color = "#008822"
        self.error_color = "#FF0000"

        self.configure(fg_color=self.bg_color)

        # Grid configuration for main window
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # TOP BAR (Toolbar)
        self.top_bar = ctk.CTkFrame(self, corner_radius=0, fg_color="#101010", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.label_title = ctk.CTkLabel(self.top_bar, text="[ SIGNAL_LOSS v1.0.4 ]", font=self.font_large, text_color=self.fg_color)
        self.label_title.pack(side="left", padx=20, pady=10)

        self.btn_record = ctk.CTkButton(self.top_bar, text="[ RECORD ]", font=self.font_main, fg_color="#202020", text_color=self.fg_color, hover_color="#00FF41", corner_radius=0, border_width=1, border_color="#00FF41", command=self.action_record)
        self.btn_record.pack(side="left", padx=10, pady=10)

        self.btn_playback = ctk.CTkButton(self.top_bar, text="[ PLAYBACK ]", font=self.font_main, fg_color="#202020", text_color=self.fg_color, hover_color="#00FF41", corner_radius=0, border_width=1, border_color="#00FF41", command=self.action_playback)
        self.btn_playback.pack(side="left", padx=10, pady=10)

        self.btn_intercept = ctk.CTkButton(self.top_bar, text="[ INTERCEPT ]", font=self.font_main, fg_color="#202020", text_color=self.error_color, hover_color="#880000", corner_radius=0, border_width=1, border_color=self.error_color, command=self.action_intercept)
        self.btn_intercept.pack(side="left", padx=10, pady=10)

        # SIDEBAR (TAPES)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0A0A0A", border_width=1, border_color="#00FF41")
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=10)
        self.sidebar.grid_propagate(False)

        self.label_tapes = ctk.CTkLabel(self.sidebar, text="-- TAPES --", font=self.font_main, text_color=self.fg_color)
        self.label_tapes.pack(pady=(10, 20))

        self.btn_file = ctk.CTkButton(self.sidebar, text="> TAPE_01.sl", font=self.font_main, fg_color="transparent", text_color=self.fg_color, hover_color="#101010", anchor="w", corner_radius=0)
        self.btn_file.pack(fill="x", padx=10, pady=5)

        # MAIN AREA (Editor + Terminal)
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.main_area.grid_rowconfigure(0, weight=3) # Editor gets more space
        self.main_area.grid_rowconfigure(1, weight=1) # Terminal gets less space
        self.main_area.grid_columnconfigure(0, weight=1)

        # Text Editor
        self.editor = ctk.CTkTextbox(
            self.main_area, 
            font=self.font_main, 
            fg_color="#000000", 
            text_color=self.fg_color,
            border_width=1,
            border_color="#00FF41",
            corner_radius=0
        )
        self.editor.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.editor.insert("0.0", "# WRITE YOUR SIGNAL HERE...\nRECORD \n    FREQ = 432;\n    DISTORT(FREQ);\nSTOP")

        # Terminal Output
        self.terminal = ctk.CTkTextbox(
            self.main_area,
            font=self.font_small,
            fg_color="#050505",
            text_color=self.dim_fg_color,
            border_width=1,
            border_color="#006611",
            corner_radius=0,
            state="disabled"
        )
        self.terminal.grid(row=1, column=0, sticky="nsew")

        # Initial Boot Text
        self.write_to_terminal("SIGNAL_LOSS OS v1.0.4 loaded.")
        self.write_to_terminal("WAITING FOR TAPE INSERTION...")
        self.write_to_terminal("READY.")

    def write_to_terminal(self, text, is_error=False):
        self.terminal.configure(state="normal")
        color = self.error_color if is_error else self.dim_fg_color
        prefix = "[ERROR] " if is_error else "> "
        self.terminal.insert("end", f"{prefix}{text}\n")
        self.terminal.configure(state="disabled")
        self.terminal.see("end")

    def action_record(self):
        self.write_to_terminal("COMPILING SIGNAL...")
        code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.write_to_terminal("EMPTY TAPE DETECTED. CANNOT RECORD.", is_error=True)
            return
        self.write_to_terminal("SIGNAL RECORDED SUCCESSFULLY.")

    def action_playback(self):
        self.write_to_terminal("PLAYING BACK FREQUENCY...")
        self.write_to_terminal("... DISTORTION AT 432Hz ...")

    def action_intercept(self):
        self.write_to_terminal("INTERCEPTING UNKNOWN SIGNAL...")
        self.write_to_terminal("ANOMALY DETECTED IN SECTOR 4. SIGNAL LOST.", is_error=True)

    def action_record(self):
        self.write_to_terminal("INITIATING SCAN...")
        
        error_list.clear()
    
        code = self.editor.get("1.0", "end-1c")
        
        if not code.strip():
            self.write_to_terminal("EMPTY TAPE. NO SIGNAL DETECTED.", is_error=True)
            return

        lexer.input(code)
        
        self.symbol_table = []
        
        self.write_to_terminal("DECODING TOKENS...")
        
        while True:
            tok = lexer.token()
            if not tok:
                break
            
            if tok.type == 'ID':
                self.symbol_table.append(f"TOKEN: {tok.type} | VALUE: {tok.value}")
                self.write_to_terminal(f"DETECTED: {tok.type}({tok.value})")

        if error_list:
            self.write_to_terminal(f"{len(error_list)} ANOMALIES DETECTED IN SIGNAL.", is_error=True)
            for err in error_list:
                self.write_to_terminal(f"L:{err['linea']} C:{err['columna']} - {err['descripcion']}", is_error=True)
        else:
            self.write_to_terminal("SIGNAL STABLE. DECODING COMPLETE.")

if __name__ == "__main__":
    app = App()
    app.mainloop()