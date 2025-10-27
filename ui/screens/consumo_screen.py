# ui/screens/consumo_screen.py
import tkinter as tk
from tkinter import ttk
from services.parser_excel import carregar_dados_excel

class ConsumoScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Label título ===
        tk.Label(
            self.frame,
            text="Gestão de Consumo",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#00215b"
        ).pack(anchor="w", pady=(0, 10))

        # === Treeview (Tabela) ===
        columns = [
            "Empresa", "Distribuidora", "Modalidade", "ConsumoPonta",
            "ConsumoForaPonta", "ValorMedio"
        ]

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        # Configura títulos das colunas
        headings = [
            "Empresa", "Distribuidora", "Modalidade Tarifária",
            "Consumo Ponta (kWh)", "Consumo Fora Ponta (kWh)", "Valor Médio da Fatura (R$)"
        ]
        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=140, anchor="w")

        # Carrega dados do backend
        self.carregar_dados()

    def carregar_dados(self):
        try:
            _, empresas, _ = carregar_dados_excel("./dados_brutos.xlsx")

            for empresa in empresas:
                self.tree.insert(
                    "",
                    "end",
                    values=[
                        empresa.nome,
                        empresa.distribuidora or "",
                        empresa.modalidade or "",
                        f"{empresa.consumo_ponta:.2f}" if empresa.consumo_ponta else "0.0",
                        f"{empresa.consumo_fora_ponta:.2f}" if empresa.consumo_fora_ponta else "0.0",
                        f"{empresa.valor_medio:.2f}" if empresa.valor_medio else "0.0"
                    ]
                )
        except Exception as e:
            tk.Label(self.frame, text=f"Erro ao carregar dados: {e}", fg="red").pack()
