import tkinter as tk
from tkinter import ttk
from cidr.gui import CIDRFrame
from vlsm.gui import VLSMFrame


def main():
    root = tk.Tk()
    root.title("Calculadora de Subredes IPv4")
    root.geometry("920x660")
    root.resizable(True, True)

    # estilo visual
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"))
    style.configure("TButton", padding=4)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    style.configure("Treeview", rowheight=22)
    style.map("Treeview", background=[("selected", "#0078d4")])

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    cidr_tab = CIDRFrame(notebook)
    vlsm_tab = VLSMFrame(notebook)

    notebook.add(cidr_tab, text="  Calculadora CIDR  ")
    notebook.add(vlsm_tab, text="  Calculadora VLSM  ")

    root.mainloop()


if __name__ == "__main__":
    main()
