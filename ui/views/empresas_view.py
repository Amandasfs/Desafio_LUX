import tkinter as tk
from tkinter import ttk

def mostrar_empresas(dashboard):
    """
    Exibe a view de empresas no main_content do dashboard
    """
    container = tk.Frame(dashboard.main_content, bg="#f8fafc")
    container.pack(fill="both", expand=True)

    tk.Label(
        container,
        text="Empresas",
        font=("Arial", 16, "bold"),
        bg="#f8fafc"
    ).pack(pady=10)

    # Exemplo de Treeview com dados de empresas
    tree = ttk.Treeview(container, columns=("Nome", "CNPJ", "Endereço"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("CNPJ", text="CNPJ")
    tree.heading("Endereço", text="Endereço")

    # Preenchendo com dados filtrados do dashboard
    if hasattr(dashboard, "dados"):
        for _, row in dashboard.dados.iterrows():
            tree.insert("", "end", values=(row.get("Empresa"), row.get("CNPJ"), row.get("Endereço - Rua")))

    tree.pack(fill="both", expand=True, padx=20, pady=10)
