import tkinter as tk
from tkinter import ttk, messagebox
from .calculos import calcular_vlsm


class VLSMFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.filas = []  # cada elemento es (frame, entry_nombre, entry_hosts)
        self._construir()

    def _construir(self):
        ttk.Label(self, text="Calculadora IP VLSM", font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))

        # red base
        base_frame = ttk.LabelFrame(self, text="Red base")
        base_frame.pack(fill="x", padx=12, pady=4)

        ttk.Label(base_frame, text="Red base (CIDR):").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.entry_red = ttk.Entry(base_frame, width=22)
        self.entry_red.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        self.entry_red.insert(0, "192.168.0.0/24")

        # subredes
        sub_frame = ttk.LabelFrame(self, text="Subredes requeridas")
        sub_frame.pack(fill="x", padx=12, pady=4)

        encabezados = ttk.Frame(sub_frame)
        encabezados.pack(fill="x", padx=6, pady=(4, 0))
        ttk.Label(encabezados, text="Nombre de subred", width=22, anchor="w").pack(side="left", padx=4)
        ttk.Label(encabezados, text="Hosts requeridos", width=16, anchor="w").pack(side="left", padx=4)

        # contenedor con scroll para las filas de subredes
        canvas_cont = tk.Frame(sub_frame)
        canvas_cont.pack(fill="x", padx=6)

        self.canvas = tk.Canvas(canvas_cont, height=130, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_cont, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.filas_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.filas_frame, anchor="nw")

        self.filas_frame.bind("<Configure>", self._actualizar_scroll)

        # botones de control
        btn_frame = ttk.Frame(sub_frame)
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="+ Agregar subred", command=self._agregar_fila).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="- Quitar ultima", command=self._quitar_fila).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Calcular VLSM", command=self._calcular).pack(side="left", padx=15)

        # 2 filas por defecto
        self._agregar_fila()
        self._agregar_fila()

        # resumen
        self.resumen_var = tk.StringVar(value="")
        resumen_frame = ttk.LabelFrame(self, text="Resumen")
        resumen_frame.pack(fill="x", padx=12, pady=4)
        ttk.Label(resumen_frame, textvariable=self.resumen_var, anchor="w").pack(padx=8, pady=4, fill="x")

        # tabla de resultados
        res_frame = ttk.LabelFrame(self, text="Subredes calculadas")
        res_frame.pack(fill="both", expand=True, padx=12, pady=4)

        cols = ("Subred", "Red/Prefijo", "Mascara", "Primer Host", "Ultimo Host", "Broadcast", "H. Sol.", "H. Util.", "Sobrantes")
        self.tree = ttk.Treeview(res_frame, columns=cols, show="headings")

        anchos = (110, 150, 150, 130, 130, 130, 70, 70, 80)
        for col, ancho in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")

        sy = ttk.Scrollbar(res_frame, orient="vertical", command=self.tree.yview)
        sx = ttk.Scrollbar(res_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def _actualizar_scroll(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _agregar_fila(self):
        idx = len(self.filas)
        frame = ttk.Frame(self.filas_frame)
        frame.grid(row=idx, column=0, pady=2, sticky="w")

        e_nombre = ttk.Entry(frame, width=22)
        e_nombre.grid(row=0, column=0, padx=4)

        e_hosts = ttk.Entry(frame, width=16)
        e_hosts.grid(row=0, column=1, padx=4)

        self.filas.append((frame, e_nombre, e_hosts))
        self._actualizar_scroll()

    def _quitar_fila(self):
        if self.filas:
            frame, _, _ = self.filas.pop()
            frame.destroy()
            self._actualizar_scroll()

    def _calcular(self):
        self.tree.delete(*self.tree.get_children())

        red = self.entry_red.get().strip()
        requerimientos = []

        for _, e_nombre, e_hosts in self.filas:
            nombre = e_nombre.get().strip()
            hosts = e_hosts.get().strip()
            # solo tomamos filas que tengan algun dato
            if nombre or hosts:
                requerimientos.append((nombre, hosts))

        try:
            resultado = calcular_vlsm(red, requerimientos)

            r = resultado
            resumen = (
                f"Total: {r['direcciones_totales']}  |  "
                f"Asignadas: {r['direcciones_asignadas']}  |  "
                f"Restantes: {r['direcciones_restantes']}  |  "
                f"Hosts utilizables: {r['hosts_utilizables']}  |  "
                f"Hosts sobrantes: {r['hosts_sobrantes']}"
            )
            self.resumen_var.set(resumen)

            for s in resultado["subredes"]:
                self.tree.insert("", "end", values=(
                    s["nombre"],
                    f"{s['red']}/{s['prefijo']}",
                    s["mascara"],
                    s["primer_host"],
                    s["ultimo_host"],
                    s["broadcast"],
                    s["hosts_solicitados"],
                    s["hosts_utilizables"],
                    s["hosts_sobrantes"],
                ))
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
