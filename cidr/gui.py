import tkinter as tk
from tkinter import ttk, messagebox
from .calculos import calcular_info_red, dividir_en_subredes, calcular_subredes_por_prefijo


class CIDRFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.filas_subredes = []
        self._construir()

    def _construir(self):
        ttk.Label(self, text="Calculadora IP CIDR", font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))

        # selector de modo
        modo_frame = ttk.LabelFrame(self, text="Modo de calculo")
        modo_frame.pack(fill="x", padx=12, pady=4)

        self.modo = tk.StringVar(value="info")
        opciones = [
            ("Informacion de red",    "info"),
            ("Dividir en N subredes", "dividir"),
            ("Subredes por prefijo",  "prefijo"),
        ]
        for texto, valor in opciones:
            ttk.Radiobutton(
                modo_frame, text=texto,
                variable=self.modo, value=valor,
                command=self._cambiar_modo
            ).pack(side="left", padx=12, pady=6)

        # inputs
        self.param_frame = ttk.LabelFrame(self, text="Parametros")
        self.param_frame.pack(fill="x", padx=12, pady=4)

        ttk.Label(self.param_frame, text="Red base (CIDR):").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.entry_red = ttk.Entry(self.param_frame, width=22)
        self.entry_red.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        self.entry_red.insert(0, "192.168.1.0/24")

        self.lbl_extra = ttk.Label(self.param_frame, text="")
        self.lbl_extra.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.entry_extra = ttk.Entry(self.param_frame, width=22)
        self.entry_extra.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        ttk.Button(self.param_frame, text="Calcular", command=self._calcular).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # resultados
        res_frame = ttk.LabelFrame(self, text="Resultados")
        res_frame.pack(fill="both", expand=True, padx=12, pady=4)

        self.tree = ttk.Treeview(res_frame, show="headings")
        sy = ttk.Scrollbar(res_frame, orient="vertical", command=self.tree.yview)
        sx = ttk.Scrollbar(res_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self._cambiar_modo()

    # muestra u oculta el campo extra segun el modo elegido
    def _cambiar_modo(self):
        modo = self.modo.get()
        if modo == "info":
            self.lbl_extra.grid_remove()
            self.entry_extra.grid_remove()
        elif modo == "dividir":
            self.lbl_extra.config(text="Numero de subredes:")
            self.lbl_extra.grid()
            self.entry_extra.grid()
        elif modo == "prefijo":
            self.lbl_extra.config(text="Nuevo prefijo (ej. 26):")
            self.lbl_extra.grid()
            self.entry_extra.grid()

    def _limpiar_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = []

    def _configurar_columnas(self, cols, anchos=None):
        self.tree["columns"] = cols
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col)
            ancho = anchos[i] if anchos else 160
            self.tree.column(col, width=ancho, anchor="center")

    # muestra la info general de la red como tabla campo/valor
    def _mostrar_info(self, r):
        self._configurar_columnas(("Campo", "Valor"), (200, 220))
        filas = [
            ("Red", f"{r['red']}/{r['prefijo']}"),
            ("Mascara de subred", r["mascara"]),
            ("Wildcard mask", r["mascara_wildcard"]),
            ("Broadcast", r["broadcast"]),
            ("Primer host", r["primer_host"]),
            ("Ultimo host", r["ultimo_host"]),
            ("Hosts utilizables", r["hosts_utilizables"]),
            ("Total direcciones", r["total_direcciones"]),
            ("Bits de host", r["bits_host"]),
            ("Clase", r["clase"]),
            ("Tipo", r["tipo"]),
        ]
        for fila in filas:
            self.tree.insert("", "end", values=fila)

    # muestra la lista de subredes calculadas
    def _mostrar_subredes(self, subredes):
        cols = ("#", "Red/Prefijo", "Mascara", "Primer Host", "Ultimo Host", "Broadcast", "Hosts")
        anchos = (40, 150, 150, 130, 130, 130, 80)
        self._configurar_columnas(cols, anchos)
        for s in subredes:
            self.tree.insert("", "end", values=(
                s["indice"],
                f"{s['red']}/{s['prefijo']}",
                s["mascara"],
                s["primer_host"],
                s["ultimo_host"],
                s["broadcast"],
                s["hosts_utilizables"],
            ))

    def _calcular(self):
        self._limpiar_tree()
        red = self.entry_red.get().strip()
        modo = self.modo.get()
        try:
            if modo == "info":
                self._mostrar_info(calcular_info_red(red))
            elif modo == "dividir":
                r = dividir_en_subredes(red, self.entry_extra.get().strip())
                self._mostrar_subredes(r["subredes"])
            elif modo == "prefijo":
                r = calcular_subredes_por_prefijo(red, self.entry_extra.get().strip())
                self._mostrar_subredes(r["subredes"])
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
