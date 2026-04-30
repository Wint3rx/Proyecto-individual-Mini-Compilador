from lexer import lexer, error_list, find_column
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk

TYPE_KEYWORDS = {'FREQ', 'DISTORT', 'VHS', 'PULSE', 'ENCRYPT', 'STATIC'} 
FUNC_KEYWORD  = 'ARCHIVE'                                                  


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ── Configuración general ────────────────
        self.title("SIGNAL_LOSS — Decoder Terminal v2.0")
        self.geometry("1200x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # ── Paleta ───────────────────────────────
        self.BG        = "#050505"
        self.FG        = "#00FF41"
        self.DIM_FG    = "#008822"
        self.ERR_COLOR = "#FF0000"
        self.PANEL_BG  = "#0A0A0A"
        self.TOOLBAR   = "#101010"
        self.configure(fg_color=self.BG)

        # ── Fuentes ──────────────────────────────
        self.font_main  = ctk.CTkFont(family="Consolas", size=14, weight="bold")
        self.font_large = ctk.CTkFont(family="Consolas", size=18, weight="bold")
        self.font_small = ctk.CTkFont(family="Consolas", size=12)
        self.font_tiny  = ctk.CTkFont(family="Consolas", size=11)

        # ── Estado ───────────────────────────────
        self.current_file  = None
        self.symbol_table  = {}
        self.token_list    = []
        self.tape_list     = []

        # ── Layout ───────────────────────────────
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_toolbar()
        self._build_sidebar()
        self._build_main_area()

        self._boot_message()

    # ════════════════════════════════════════════
    #  CONSTRUCCIÓN DE LA UI
    # ════════════════════════════════════════════

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self, corner_radius=0, fg_color=self.TOOLBAR, height=50)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        def btn(parent, text, color, hover, cmd):
            return ctk.CTkButton(
                parent, text=text, font=self.font_main,
                fg_color="#202020", text_color=color, hover_color=hover,
                corner_radius=0, border_width=1, border_color=color,
                command=cmd, width=130
            )

        ctk.CTkLabel(bar, text="[ SIGNAL_LOSS v2.0 ]",
                     font=self.font_large, text_color=self.FG).pack(side="left", padx=20, pady=10)

        btn(bar, "[ RECORD ]",    self.FG,        "#00FF41", self.action_record   ).pack(side="left", padx=6, pady=10)
        btn(bar, "[ EJECT ]",     self.FG,        "#00FF41", self.action_eject    ).pack(side="left", padx=6, pady=10)
        btn(bar, "[ OPEN ]",      "#00BFFF",      "#005588", self.action_open     ).pack(side="left", padx=6, pady=10)
        btn(bar, "[ SAVE ]",      "#00BFFF",      "#005588", self.action_save     ).pack(side="left", padx=6, pady=10)
        btn(bar, "[ EXPORT ]",    "#FFAA00",      "#885500", self.action_export   ).pack(side="left", padx=6, pady=10)
        btn(bar, "[ INTERCEPT ]", self.ERR_COLOR, "#880000", self.action_intercept).pack(side="left", padx=6, pady=10)
        btn(bar, "[ SYNTAX ]",    "#AAFFAA",      "#226622", self.action_syntax   ).pack(side="left", padx=6, pady=10)

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=190, corner_radius=0,
                      fg_color=self.PANEL_BG, border_width=1, border_color=self.FG)
        sb.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=10)
        sb.grid_propagate(False)
        sb.grid_rowconfigure(3, weight=1)   # la lista de tapes se expande
        sb.grid_columnconfigure(0, weight=1)

        # ── Cabecera: solo título ────────────────────
        ctk.CTkLabel(sb, text="-- TAPES --",
             font=self.font_main, text_color=self.FG).grid(row=0, column=0, sticky="ew",
                                                            padx=8, pady=(12, 8))

        # ── Stats ────────────────────────────────────
        divider = ctk.CTkFrame(sb, height=1, fg_color=self.DIM_FG)
        divider.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 6))

        stats = ctk.CTkFrame(sb, fg_color="transparent")
        stats.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(stats, text="-- STATS --",
                 font=self.font_main, text_color=self.FG).pack(anchor="w", pady=(0, 4))

        self.lbl_tokens  = ctk.CTkLabel(stats, text="Tokens:   —", font=self.font_small, text_color=self.DIM_FG)
        self.lbl_symbols = ctk.CTkLabel(stats, text="Symbols:  —", font=self.font_small, text_color=self.DIM_FG)
        self.lbl_errors  = ctk.CTkLabel(stats, text="Errors:   —", font=self.font_small, text_color=self.DIM_FG)
        self.lbl_tokens .pack(anchor="w")
        self.lbl_symbols.pack(anchor="w")
        self.lbl_errors .pack(anchor="w")

        self.lbl_file = ctk.CTkLabel(stats, text="", font=self.font_tiny,
                                  text_color=self.DIM_FG, wraplength=160, justify="left")
        self.lbl_file.pack(anchor="w")

        # ── Lista scrollable de archivos ─────────────
        self.tape_listbox = ctk.CTkScrollableFrame(
            sb, fg_color="transparent", scrollbar_button_color=self.DIM_FG,
            scrollbar_button_hover_color=self.FG
        )
        self.tape_listbox.grid(row=3, column=0, sticky="nsew", padx=4, pady=(0, 8))
        self.tape_listbox.grid_columnconfigure(0, weight=1)

    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        main.grid_rowconfigure(0, weight=3)
        main.grid_rowconfigure(1, weight=2)
        main.grid_columnconfigure(0, weight=1)

        # ── Editor ───────────────────────────────
        self.editor = ctk.CTkTextbox(
            main, font=self.font_main,
            fg_color="#000000", text_color=self.FG,
            border_width=1, border_color=self.FG, corner_radius=0
        )
        self.editor.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.editor.insert("0.0",
            "# WRITE YOUR SIGNAL HERE...\n"
            "RECORD {\n"
            "    FREQ    canal   = 432;\n"
            "    DISTORT nivel   = 3.14;\n"
            "    VHS     mensaje = \"LOST_SIGNAL\";\n"
            "    MANDELA (canal > 100) {\n"
            "        PLAYBACK(canal);\n"
            "    }\n"
            "    ALTERNATE {\n"
            "        PLAYBACK(mensaje);\n"
            "    }\n"
            "    LOOP_TAPE (canal > 0) {\n"
            "        canal = canal - 1;\n"
            "    }\n"
            "}"
        )

        # ── Panel inferior con pestañas ──────────
        tab_frame = ctk.CTkFrame(main, fg_color=self.PANEL_BG,
                                  border_width=1, border_color=self.DIM_FG, corner_radius=0)
        tab_frame.grid(row=1, column=0, sticky="nsew")
        tab_frame.grid_rowconfigure(1, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)

        # Barra de pestañas manual
        tab_bar = ctk.CTkFrame(tab_frame, fg_color="#0F0F0F", height=32, corner_radius=0)
        tab_bar.grid(row=0, column=0, sticky="ew")

        self.tab_buttons = {}
        self.tab_panels  = {}
        tab_names = ["TERMINAL", "TOKENS", "SYMBOLS", "ERRORS", "ÁRBOL"]

        for name in tab_names:
            b = ctk.CTkButton(
                tab_bar, text=f"[{name}]", font=self.font_small,
                fg_color="transparent", text_color=self.DIM_FG,
                hover_color="#1A1A1A", corner_radius=0, width=110,
                command=lambda n=name: self._show_tab(n)
            )
            b.pack(side="left", padx=2, pady=3)
            self.tab_buttons[name] = b

        # Contenedor de paneles
        self.panel_container = ctk.CTkFrame(tab_frame, fg_color="transparent")
        self.panel_container.grid(row=1, column=0, sticky="nsew")
        self.panel_container.grid_rowconfigure(0, weight=1)
        self.panel_container.grid_columnconfigure(0, weight=1)

        # Panel TERMINAL
        self.terminal = ctk.CTkTextbox(
            self.panel_container, font=self.font_small,
            fg_color="#050505", text_color=self.DIM_FG,
            border_width=0, corner_radius=0, state="disabled"
        )

        # Panel TOKENS
        self.tokens_box = ctk.CTkTextbox(
            self.panel_container, font=self.font_tiny,
            fg_color="#050505", text_color="#AAFFAA",
            border_width=0, corner_radius=0, state="disabled"
        )

        # Panel SYMBOLS
        self.symbols_box = ctk.CTkTextbox(
            self.panel_container, font=self.font_tiny,
            fg_color="#050505", text_color="#AACCFF",
            border_width=0, corner_radius=0, state="disabled"
        )

        # Panel ERRORS
        self.errors_box = ctk.CTkTextbox(
            self.panel_container, font=self.font_tiny,
            fg_color="#050505", text_color="#FF6666",
            border_width=0, corner_radius=0, state="disabled"
        )

        # Panel ÁRBOL
        self.tree_box = ctk.CTkTextbox(
            self.panel_container, font=self.font_tiny,
            fg_color="#050505", text_color="#FFDD88",
            border_width=0, corner_radius=0, state="disabled"
        )

        self.tab_panels = {
            "TERMINAL": self.terminal,
            "TOKENS":   self.tokens_box,
            "SYMBOLS":  self.symbols_box,
            "ERRORS":   self.errors_box,
            "ÁRBOL":    self.tree_box,
        }

        self._show_tab("TERMINAL")

    def _show_tab(self, name):
        for n, panel in self.tab_panels.items():
            panel.grid_forget()
        self.tab_panels[name].grid(row=0, column=0, sticky="nsew")

        for n, btn in self.tab_buttons.items():
            is_active = (n == name)
            btn.configure(
                text_color=self.FG if is_active else self.DIM_FG,
                fg_color="#1A1A1A" if is_active else "transparent"
            )

    # ════════════════════════════════════════════
    #  ESCRITURA EN PANELES
    # ════════════════════════════════════════════

    def _write(self, widget, text, clear=False):
        widget.configure(state="normal")
        if clear:
            widget.delete("0.0", "end")
        widget.insert("end", text + "\n")
        widget.configure(state="disabled")
        widget.see("end")

    def write_to_terminal(self, text, is_error=False):
        prefix = "[ERR] " if is_error else "> "
        self._write(self.terminal, f"{prefix}{text}")

    # ════════════════════════════════════════════
    #  SIDEBAR — gestión de tapes
    # ════════════════════════════════════════════

    def sidebar_add_tape(self):
        """Abre el diálogo y añade el archivo a la lista del sidebar."""
        path = filedialog.askopenfilename(
            title="Add Tape to Sidebar",
            filetypes=[("SIGNAL_LOSS files", "*.sl"), ("Text files", "*.txt"), ("All", "*.*")]
        )
        if path and path not in self.tape_list:
            self.tape_list.append(path)
            self._sidebar_render_tapes()

    def _sidebar_render_tapes(self):
            """Redibuja todos los botones de archivos en el sidebar."""
            for widget in self.tape_listbox.winfo_children():
                widget.destroy()

            for path in self.tape_list:
                name = path.split("/")[-1].split("\\")[-1]
                is_active = (path == self.current_file)

                row = ctk.CTkFrame(self.tape_listbox, fg_color="transparent")
                row.pack(fill="x", pady=1)
                row.grid_columnconfigure(0, weight=1)

                btn = ctk.CTkButton(
                    row, text=f"> {name}",
                    font=self.font_small,
                    fg_color="#1A1A1A" if is_active else "transparent",
                    text_color=self.FG if is_active else self.DIM_FG,
                    hover_color="#1A1A1A",
                    anchor="w", corner_radius=0,
                    command=lambda p=path: self.sidebar_open_tape(p)
                )
                btn.grid(row=0, column=0, sticky="ew")

                # botón × para quitar de la lista
                ctk.CTkButton(
                    row, text="×", font=self.font_small,
                    fg_color="transparent", text_color=self.DIM_FG,
                    hover_color="#330000", corner_radius=0,
                    width=22,
                    command=lambda p=path: self.sidebar_remove_tape(p)
                ).grid(row=0, column=1)

    def sidebar_open_tape(self, path):
        """Carga un archivo del sidebar en el editor (pregunta si hay cambios)."""
        current_content = self.editor.get("1.0", "end-1c")
        # Detectar cambios sin guardar comparando con el archivo actual
        if self.current_file:
            try:
                with open(self.current_file, "r", encoding="utf-8") as f:
                    saved = f.read()
                if current_content.strip() != saved.strip():
                    if not messagebox.askyesno(
                        "Unsaved Changes",
                        "Current tape has unsaved changes.\nSwitch anyway?"
                    ):
                        return
            except Exception:
                pass  # si no se puede leer el archivo actual, seguimos igual

        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", code)
            self.current_file = path
            name = path.split("/")[-1].split("\\")[-1]
            self.lbl_file.configure(text=f"> {name}")
            self.write_to_terminal(f"TAPE LOADED: {name}")
            self._sidebar_render_tapes()   # refresca el resaltado activo
        except Exception as e:
            self.write_to_terminal(f"LOAD ERROR: {e}", is_error=True)

    def sidebar_remove_tape(self, path):
        """Quita un archivo de la lista del sidebar (no lo borra del disco)."""
        if path in self.tape_list:
            self.tape_list.remove(path)
            if self.current_file == path:
                self.current_file = None
                self.lbl_file.configure(text="")
            self._sidebar_render_tapes()

    # ════════════════════════════════════════════
    #  ACCIONES DE BOTONES
    # ════════════════════════════════════════════

    def action_eject(self):
        """Limpia el editor, las tablas y el terminal."""
        self.editor.delete("0.0", "end")
        self.editor.insert("0.0", "# WRITE YOUR SIGNAL HERE...\n")
        for box in [self.terminal, self.tokens_box, self.symbols_box, self.errors_box, self.tree_box]:
            box.configure(state="normal")
            box.delete("0.0", "end")
            box.configure(state="disabled")
        self.symbol_table = {}
        self.token_list   = []
        self.current_file = None
        self.lbl_file    .configure(text="> NO TAPE LOADED")
        self.lbl_tokens  .configure(text="Tokens:   —")
        self.lbl_symbols .configure(text="Symbols:  —")
        self.lbl_errors  .configure(text="Errors:   —")
        self.write_to_terminal("TAPE EJECTED. READY FOR NEW SIGNAL.")
        self._show_tab("TERMINAL")

    def action_open(self):
        path = filedialog.askopenfilename(
            title="Open Tape",
            filetypes=[("SIGNAL_LOSS files", "*.sl"), ("Text files", "*.txt"), ("All", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self.editor.delete("0.0", "end")
            self.editor.insert("0.0", code)
            self.current_file = path
            name = path.split("/")[-1].split("\\")[-1]
            self.lbl_file.configure(text=f"> {name}")
            if path not in self.tape_list:
                self.tape_list.append(path)
            self._sidebar_render_tapes()
            self.write_to_terminal(f"TAPE LOADED: {name}")
        except Exception as e:
            self.write_to_terminal(f"LOAD ERROR: {e}", is_error=True)

    def action_save(self):
        if not self.current_file:
            path = filedialog.asksaveasfilename(
                title="Save Tape",
                defaultextension=".sl",
                filetypes=[("SIGNAL_LOSS files", "*.sl"), ("Text files", "*.txt")]
            )
            if not path:
                return
            self.current_file = path

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.get("0.0", "end-1c"))
            name = self.current_file.split("/")[-1].split("\\")[-1]
            self.lbl_file.configure(text=f"> {name}")
            self.write_to_terminal(f"TAPE SAVED: {name}")
        except Exception as e:
            self.write_to_terminal(f"SAVE ERROR: {e}", is_error=True)

    def action_export(self):
        """Exporta las tres tablas a un archivo .txt listo para pegar en el documento."""
        if not self.symbol_table and not self.token_list:
            self.write_to_terminal("NO DATA TO EXPORT. Run RECORD first.", is_error=True)
            return

        path = filedialog.asksaveasfilename(
            title="Export Tables",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return

        from lexer import error_list
        lines = []

        # ── Tabla de Tokens ──────────────────────
        lines.append("=" * 60)
        lines.append("  TABLA DE TOKENS — SIGNAL_LOSS")
        lines.append("=" * 60)
        lines.append(f"{'#':<5} {'TOKEN':<20} {'TIPO':<18} {'LÍNEA':<6}")
        lines.append("-" * 60)
        for i, tok in enumerate(self.token_list, 1):
            lines.append(f"{i:<5} {str(tok['valor']):<20} {tok['tipo']:<18} {tok['linea']:<6}")

        # ── Tabla de Símbolos ────────────────────
        lines.append("")
        lines.append("=" * 60)
        lines.append("  TABLA DE SÍMBOLOS — SIGNAL_LOSS")
        lines.append("=" * 60)
        lines.append(f"{'NOMBRE':<20} {'TIPO':<12} {'LÍNEA':<6} {'VALOR'}")
        lines.append("-" * 60)
        for name, data in self.symbol_table.items():
            val = str(data.get('valor', '—'))
            lines.append(f"{name:<20} {data['tipo']:<12} {data['linea']:<6} {val}")

        # ── Tabla de Errores ─────────────────────
        lines.append("")
        lines.append("=" * 60)
        lines.append("  TABLA DE ERRORES — SIGNAL_LOSS")
        lines.append("=" * 60)
        if error_list:
            lines.append(f"{'TIPO':<10} {'LÍNEA':<6} {'COL':<6} {'DESCRIPCIÓN'}")
            lines.append("-" * 60)
            for err in error_list:
                lines.append(f"{err['tipo']:<10} {err['linea']:<6} {err['columna']:<6} {err['descripcion']}")
        else:
            lines.append("  (sin errores)")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self.write_to_terminal(f"TABLES EXPORTED → {path.split('/')[-1]}")
        except Exception as e:
            self.write_to_terminal(f"EXPORT ERROR: {e}", is_error=True)
    
    def action_syntax(self):
        """Corre solo el análisis sintáctico y muestra el árbol."""
        from parser_sl import parse
        code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.write_to_terminal("EMPTY TAPE. NO SIGNAL.", is_error=True)
            return
        self.write_to_terminal("─" * 40)
        self.write_to_terminal("RUNNING SYNTAX ANALYSIS...")
        ast, serrors = parse(code)
        self._poblar_arbol(ast)
        self._poblar_errores_sint(serrors)
        if serrors:
            self.write_to_terminal(f"{len(serrors)} SYNTAX ERROR(S) FOUND.", is_error=True)
            self._show_tab("ERRORS")
        else:
            self.write_to_terminal("SYNTAX OK. DERIVATION TREE GENERATED.")
            self._show_tab("ÁRBOL")

    def _poblar_arbol(self, ast):
        from parser_sl import arbol_completo_texto
        self.tree_box.configure(state="normal")
        self.tree_box.delete("0.0", "end")
        self.tree_box.insert("end", "DERIVATION TREE — SIGNAL_LOSS\n")
        self.tree_box.insert("end", "═" * 50 + "\n")
        self.tree_box.insert("end", arbol_completo_texto(ast) + "\n")
        self.tree_box.configure(state="disabled")

    def _poblar_errores(self, lexical_errors, syntactic_errors):
        self.errors_box.configure(state="normal")
        if lexical_errors:
            self.errors_box.insert("end", "\n── ERRORES LÉXICOS ──\n")
            self.errors_box.insert("end", f"{'TIPO':<10} {'LÍN':<5} {'COL':<5} {'DESCRIPCIÓN'}\n")
            self.errors_box.insert("end", "─" * 55 + "\n")
            for err in lexical_errors:
                self.errors_box.insert(
                    "end",
                    f"{err['tipo']:<10} {err['linea']:<5} {err['columna']:<5} {err['descripcion']}\n"
                )
        if syntactic_errors:
            self.errors_box.insert("end", "\n── ERRORES SINTÁCTICOS ──\n")
            self.errors_box.insert("end", f"{'TIPO':<10} {'LÍN':<5} {'COL':<5} {'DESCRIPCIÓN'}\n")
            self.errors_box.insert("end", "─" * 55 + "\n")
            for err in syntactic_errors:
                self.errors_box.insert(
                    "end",
                    f"{err['tipo']:<10} {err['linea']:<5} {err['columna']:<5} {err['descripcion']}\n"
                )
        if not lexical_errors and not syntactic_errors:
            self.errors_box.insert("end", "✓ Sin errores detectados.\n")
        self.errors_box.configure(state="disabled")

    def _eval_expr(self, node, env):
        if node is None:
            return None

        node_type = node.get("tipo")

        if node_type == "LITERAL":
            return node.get("valor")

        if node_type == "VARIABLE":
            return env.get(node.get("nombre"), self.symbol_table.get(node.get("nombre"), {}).get("valor", 0))

        if node_type == "NEGACION":
            value = self._eval_expr(node.get("operando"), env)
            try:
                return -value
            except Exception:
                return 0

        if node_type == "OPERACION":
            left = self._eval_expr(node.get("izquierda"), env)
            right = self._eval_expr(node.get("derecha"), env)
            op = node.get("operador")

            try:
                if op == "+":
                    return left + right
                if op == "-":
                    return left - right
                if op == "*":
                    return left * right
                if op == "/":
                    return left / right
                if op == ">":
                    return left > right
                if op == "<":
                    return left < right
                if op == ">=":
                    return left >= right
                if op == "<=":
                    return left <= right
                if op == "==":
                    return left == right
                if op == "!=":
                    return left != right
            except Exception:
                return 0

        if node_type == "LLAMADA_FUNCION":
            return [self._eval_expr(arg, env) for arg in node.get("argumentos", [])]

        return None

    def _execute_block(self, statements, env, depth=0, max_iterations=1000):
        for statement in statements or []:
            self._execute_node(statement, env, depth=depth, max_iterations=max_iterations)

    def _execute_node(self, node, env, depth=0, max_iterations=1000):
        if node is None:
            return

        node_type = node.get("tipo")

        if node_type == "PROGRAMA":
            self._execute_block(node.get("cuerpo", []), env, depth=depth, max_iterations=max_iterations)
            return

        if node_type == "DECLARACION":
            value = self._eval_expr(node.get("valor"), env)
            name = node.get("nombre")
            env[name] = value
            if name in self.symbol_table:
                self.symbol_table[name]["valor"] = value
            else:
                self.symbol_table[name] = {
                    "tipo": node.get("tipo_dato", "?"),
                    "linea": node.get("linea", "?"),
                    "valor": value,
                }
            return

        if node_type == "ASIGNACION":
            value = self._eval_expr(node.get("valor"), env)
            name = node.get("nombre")
            env[name] = value
            if name in self.symbol_table:
                self.symbol_table[name]["valor"] = value
            return

        if node_type == "PLAYBACK":
            value = self._eval_expr(node.get("argumento"), env)
            self.write_to_terminal(str(value))
            return

        if node_type == "CONDICIONAL":
            if self._eval_expr(node.get("condicion"), env):
                self._execute_block(node.get("cuerpo_then", []), env, depth=depth + 1, max_iterations=max_iterations)
            else:
                self._execute_block(node.get("cuerpo_else", []), env, depth=depth + 1, max_iterations=max_iterations)
            return

        if node_type == "BUCLE":
            iterations = 0
            while self._eval_expr(node.get("condicion"), env):
                self._execute_block(node.get("cuerpo", []), env, depth=depth + 1, max_iterations=max_iterations)
                iterations += 1
                if iterations >= max_iterations:
                    self.write_to_terminal("LOOP STOPPED: MAX ITERATIONS REACHED.", is_error=True)
                    break
            return

        if node_type == "LLAMADA_FUNCION":
            return

        if node_type == "RETORNO":
            return self._eval_expr(node.get("valor"), env)

    def _run_program(self, ast):
        env = {}
        self.write_to_terminal("RUNNING SIGNAL...")
        self._execute_node(ast, env)
        return env

    def action_intercept(self):
        """Muestra todos los tokens ilegales encontrados."""
        if not error_list:
            self.write_to_terminal("NO ANOMALIES INTERCEPTED.")
        else:
            self.write_to_terminal(f"{len(error_list)} ANOMALIES INTERCEPTED:", is_error=True)
            for err in error_list:
                self.write_to_terminal(
                    f"  L:{err['linea']} C:{err['columna']} — {err['descripcion']}", is_error=True
                )
        self._show_tab("ERRORS")

    # ════════════════════════════════════════════
    #  LÓGICA PRINCIPAL: RECORD (análisis léxico)
    # ════════════════════════════════════════════

    def action_record(self):
        from lexer import lexer, error_list, find_column

        # Reinicio limpio
        error_list.clear()
        lexer.lineno = 1
        self.symbol_table = {}
        self.token_list   = []

        code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.write_to_terminal("EMPTY TAPE. NO SIGNAL DETECTED.", is_error=True)
            return

        self.write_to_terminal("─" * 40)
        self.write_to_terminal("INITIATING SCAN...")
        lexer.input(code)

        # ── Pasada de tokens ─────────────────────
        pending_type = None   # último keyword de tipo visto (FREQ / VHS / PULSE)
        pending_func = False  # acabamos de ver INTERCEPT (declaración de función)

        while True:
            tok = lexer.token()
            if not tok:
                break

            # Guardar en lista de tokens
            self.token_list.append({
                "valor": tok.value,
                "tipo":  tok.type,
                "linea": tok.lineno,
            })

            # ── Lógica de tabla de símbolos ──────
            if tok.type in TYPE_KEYWORDS:
                pending_type = tok.type
                pending_func = False

            elif tok.type == FUNC_KEYWORD:
                pending_func = True
                pending_type = None

            elif tok.type == 'ID':
                if tok.value not in self.symbol_table:
                    if pending_type:
                        self.symbol_table[tok.value] = {
                            "tipo":  pending_type,
                            "linea": tok.lineno,
                            "valor": "—",
                        }
                    elif pending_func:
                        self.symbol_table[tok.value] = {
                            "tipo":  "FUNCTION",
                            "linea": tok.lineno,
                            "valor": "—",
                        }
                pending_type = None
                pending_func = False

            elif tok.type == 'SEMICOLON':
                pending_type = None
                pending_func = False

        # ── Poblar pestaña TOKENS ────────────────
        self.tokens_box.configure(state="normal")
        self.tokens_box.delete("0.0", "end")
        header = f"{'#':<5} {'VALOR':<22} {'TIPO':<20} {'LÍNEA'}"
        self.tokens_box.insert("end", header + "\n" + "─" * 60 + "\n")
        for i, tok in enumerate(self.token_list, 1):
            self.tokens_box.insert(
                "end",
                f"{i:<5} {str(tok['valor']):<22} {tok['tipo']:<20} {tok['linea']}\n"
            )
        self.tokens_box.configure(state="disabled")

        # ── Poblar pestaña SYMBOLS ───────────────
        self.symbols_box.configure(state="normal")
        self.symbols_box.delete("0.0", "end")
        self.symbols_box.insert("end", f"{'NOMBRE':<20} {'TIPO':<12} {'LÍNEA':<6} {'VALOR'}\n")
        self.symbols_box.insert("end", "─" * 55 + "\n")
        if self.symbol_table:
            for name, data in self.symbol_table.items():
                self.symbols_box.insert(
                    "end",
                    f"{name:<20} {data['tipo']:<12} {data['linea']:<6} {data.get('valor','—')}\n"
                )
        else:
            self.symbols_box.insert("end", "(no se detectaron símbolos)\n")
        self.symbols_box.configure(state="disabled")

        # ── Poblar pestaña ERRORS ────────────────
        self.errors_box.configure(state="normal")
        self.errors_box.delete("0.0", "end")
        if error_list:
            self.errors_box.insert("end", f"{'TIPO':<10} {'LÍN':<5} {'COL':<5} {'DESCRIPCIÓN'}\n")
            self.errors_box.insert("end", "─" * 55 + "\n")
            for err in error_list:
                self.errors_box.insert(
                    "end",
                    f"{err['tipo']:<10} {err['linea']:<5} {err['columna']:<5} {err['descripcion']}\n"
                )
        else:
            self.errors_box.insert("end", "✓ Sin errores léxicos detectados.\n")
        self.errors_box.configure(state="disabled")

        # ── Actualizar sidebar ───────────────────
        self.lbl_tokens .configure(text=f"Tokens:   {len(self.token_list)}")
        self.lbl_symbols.configure(text=f"Symbols:  {len(self.symbol_table)}")
        self.lbl_errors .configure(text=f"Errors:   {len(error_list)}")

        # ── Análisis sintáctico automático ────────
        if error_list:
            self.write_to_terminal(
                f"{len(error_list)} ANOMAL{'Y' if len(error_list)==1 else 'IES'} IN SIGNAL.", is_error=True
            )
        else:
            self.write_to_terminal(f"LEX OK — {len(self.token_list)} tokens · {len(self.symbol_table)} symbols.")

        self.write_to_terminal("RUNNING SYNTAX ANALYSIS...")
        from parser_sl import parse
        ast, serrors = parse(code)

        self._poblar_arbol(ast)
        total_errors = len(error_list) + len(serrors)
        self._poblar_errores(error_list, serrors)

        nerr = total_errors
        self.lbl_errors.configure(text=f"Errors:   {nerr}")

        if total_errors:
            self.write_to_terminal(f"{nerr} ERROR(S) DETECTED.", is_error=True)
            self._show_tab("ERRORS")
        else:
            self.write_to_terminal("SIGNAL DECODED. TREE GENERATED.")
            self._show_tab("ÁRBOL")
            self._run_program(ast)

    # ════════════════════════════════════════════
    #  BOOT
    # ════════════════════════════════════════════

    def _boot_message(self):
        msgs = [
            "SIGNAL_LOSS OS v2.0 — DECODER TERMINAL",
            "LEXICAL ENGINE: ONLINE",
            "MEMORY BANKS: CLEAR",
            "─" * 38,
            "INSERT TAPE OR TYPE SIGNAL.",
            "PRESS [ RECORD ] TO SCAN.",
        ]
        for m in msgs:
            self.write_to_terminal(m)


if __name__ == "__main__":
    app = App()
    app.mainloop()