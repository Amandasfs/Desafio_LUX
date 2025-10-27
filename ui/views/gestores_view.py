import tkinter as tk
from tkinter import ttk

def mostrar_gestores(dashboard):
    """
    Exibe a view de gestores no main_content do dashboard
    """
    container = tk.Frame(dashboard.main_content, bg="#f8fafc")
    container.pack(fill="both", expand=True)

    tk.Label(
        container,
        text="Gestores",
        font=("Arial", 16, "bold"),
        bg="#f8fafc"
    ).pack(pady=10)

    # Exemplo de Treeview com dados de gestores
    tree = ttk.Treeview(container, columns=("Nome", "Cargo", "Empresa"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Cargo", text="Cargo")
    tree.heading("Empresa", text="Empresa")

    if hasattr(dashboard, "dados"):
        gestores = dashboard.dados.groupby("Gestor Responsável (LUX)")
        for _, row in dashboard.dados.iterrows():
            tree.insert("", "end", values=(row.get("Nome"), row.get("Cargo"), row.get("Empresa")))

    tree.pack(fill="both", expand=True, padx=20, pady=10)
