# ui/screens/empresas_screen.py
import tkinter as tk
from tkinter import ttk
from services.parser_excel import carregar_dados_excel
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, seja no dev ou no exe PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Diretório temporário do PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class EmpresasScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Label título ===
        tk.Label(
            self.frame,
            text="Empresas",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#00215b"
        ).pack(anchor="w", pady=(0, 10))

        # === Treeview (Tabela) ===
        columns = [
            "Empresa", "Rua", "Numero", "Estado", "Cidade", "CEP",
            "RazaoSocial", "CNPJ", "Distribuidora", "Modalidade", "Gestor"
        ]

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        # Configura títulos das colunas
        headings = [
            "Empresa", "Rua", "Número", "Estado", "Cidade", "CEP",
            "Razão Social", "CNPJ", "Distribuidora", "Modalidade Tarifária", "Nome Gestor"
        ]
        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=120, anchor="w")  # Ajuste de largura inicial

        # Carrega dados do backend
        self.carregar_dados()

    def carregar_dados(self):
        try:
            # Caminho absoluto do Excel (funciona no exe também)
            excel_path = resource_path("dados_brutos.xlsx")
            _, empresas, gestores = carregar_dados_excel(excel_path)

            for empresa in empresas:
                gestor_nome = ""
                # Usa o gestor associado diretamente à empresa, se houver
                if hasattr(empresa, "gestor") and empresa.gestor:
                    gestor_nome = empresa.gestor.nome
                else:
                    # fallback: pega o primeiro gestor que tenha cliente nessa empresa
                    for gestor in gestores:
                        if any(c.empresa == empresa for c in gestor.clientes):
                            gestor_nome = gestor.nome
                            break

                self.tree.insert(
                    "",
                    "end",
                    values=[
                        empresa.nome,
                        empresa.rua,
                        empresa.numero,
                        empresa.estado,
                        empresa.cidade,
                        empresa.cep,
                        empresa.razao_social,
                        empresa.cnpj,
                        empresa.distribuidora or "",
                        empresa.modalidade or "",
                        gestor_nome
                    ]
                )
        except Exception as e:
            tk.Label(self.frame, text=f"Erro ao carregar dados: {e}", fg="red").pack()
