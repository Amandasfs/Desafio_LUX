# ui/screens/gestores_screen.py
import tkinter as tk
from tkinter import ttk
from services.parser_excel import carregar_dados_excel

class GestoresScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Título ===
        tk.Label(
            self.frame,
            text="Gestão de Clientes por Gestor",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#00215b"
        ).pack(anchor="w", pady=(0, 10))

        # Carrega dados do backend
        _, empresas, gestores = carregar_dados_excel("./dados_brutos.xlsx")
        self.gestores = gestores

        # === Choice box com nomes dos gestores ===
        tk.Label(self.frame, text="Selecione um Gestor:", bg="#f0f0f0").pack(anchor="w")
        self.gestor_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.gestor_var,
            state="readonly",
            values=[g.nome for g in self.gestores]
        )
        self.combobox.pack(anchor="w", pady=(0, 10))
        self.combobox.bind("<<ComboboxSelected>>", self.atualizar_tabela)

        # === Treeview (Tabela) ===
        columns = ["Cliente", "Empresa", "Distribuidora", "ValorMedio"]
        headings = ["Nome do Cliente", "Empresa", "Distribuidora", "Valor Médio da Fatura (R$)"]

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=180, anchor="w")

    def atualizar_tabela(self, event=None):
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtém o gestor selecionado
        nome_gestor = self.gestor_var.get()
        gestor = next((g for g in self.gestores if g.nome == nome_gestor), None)
        if not gestor:
            return

        # Pega todos os clientes das empresas associadas a esse gestor
        clientes = []
        for empresa in gestor.empresas:
            clientes.extend(empresa.clientes)

        # Ordena clientes alfabeticamente
        clientes_ordenados = sorted(clientes, key=lambda c: c.nome.lower())

        for cliente in clientes_ordenados:
            empresa = cliente.empresa
            self.tree.insert(
                "",
                "end",
                values=[
                    cliente.nome,
                    empresa.nome if empresa else "",
                    empresa.distribuidora if empresa else "",
                    f"{empresa.valor_medio:.2f}" if empresa and empresa.valor_medio else "0.0"
                ]
            )
