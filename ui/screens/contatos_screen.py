import tkinter as tk
from tkinter import ttk, messagebox
from services.parser_excel import carregar_dados_excel
import os
import sys


def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso (compatível com PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ContatosScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Frame superior com botões ===
        filtro_frame = tk.Frame(self.frame, bg="#f0f0f0")
        filtro_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            filtro_frame,
            text="Organizar por:",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg="#00215b"
        ).pack(side="left")

        tk.Button(
            filtro_frame,
            text="Nome",
            command=lambda: self.carregar_tabela(ordenar="nome"),
            bg="#004aad",
            fg="white",
            font=("Arial", 9, "bold"),
            width=10
        ).pack(side="left", padx=5)

        tk.Button(
            filtro_frame,
            text="Gestor",
            command=lambda: self.carregar_tabela(ordenar="gestor"),
            bg="#007bff",
            fg="white",
            font=("Arial", 9, "bold"),
            width=10
        ).pack(side="left", padx=5)

        # === Treeview (tabela principal) ===
        columns = ["identificador", "nome", "cargo", "empresa", "telefone", "email", "gestor"]
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=18)
        self.tree.pack(fill="both", expand=True)

        # Cabeçalhos
        headers = [
            "Identificador", "Nome", "Cargo", "Empresa",
            "Telefone", "E-mail", "Gestor Responsável"
        ]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=150 if col != "email" else 200, anchor="w")

        # Scrollbar vertical
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")

        # Carrega os dados inicialmente
        self.carregar_tabela()

    def carregar_tabela(self, ordenar=None):
        """Carrega os dados de contatos a partir do Excel e exibe na tabela."""
        # Limpa a tabela antes de atualizar
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            excel_path = resource_path("dados_brutos.xlsx")
            clientes, empresas, gestores = carregar_dados_excel(excel_path)

            dados = []
            for c in clientes:
                gestor_nome = ""

                # Pega o gestor do cliente, ou o gestor da empresa
                if hasattr(c, "gestor") and c.gestor:
                    gestor_nome = c.gestor.nome
                elif c.empresa and hasattr(c.empresa, "gestor") and c.empresa.gestor:
                    gestor_nome = c.empresa.gestor.nome

                dados.append({
                    "identificador": getattr(c, "identificador", ""),
                    "nome": getattr(c, "nome", ""),
                    "cargo": getattr(c, "cargo", ""),
                    "empresa": getattr(c.empresa, "nome", "") if c.empresa else "",
                    "telefone": getattr(c, "telefone", ""),
                    "email": getattr(c, "email", ""),
                    "gestor": gestor_nome
                })

            # Ordenação
            if ordenar == "nome":
                dados.sort(key=lambda x: x["nome"].lower())
            elif ordenar == "gestor":
                dados.sort(key=lambda x: (x["gestor"].lower(), x["nome"].lower()))

            # Insere os dados na tabela
            for item in dados:
                self.tree.insert("", "end", values=(
                    item["identificador"], item["nome"], item["cargo"],
                    item["empresa"], item["telefone"], item["email"], item["gestor"]
                ))

        except Exception as e:
            messagebox.showerror("Erro ao carregar dados", f"Não foi possível carregar contatos.\n\n{e}")
