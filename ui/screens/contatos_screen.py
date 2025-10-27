# ui/dashboard/screens/contatos_screen.py
import tkinter as tk
from tkinter import ttk
from services.parser_excel import carregar_dados_excel

class ContatosScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        # === Botões de filtro ===
        filtro_frame = tk.Frame(self.frame, bg="#f0f0f0")
        filtro_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filtro_frame, text="Organizar por:", bg="#f0f0f0").pack(side="left")

        tk.Button(filtro_frame, text="Nome", command=lambda: self.carregar_tabela(ordenar="nome")).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Gestor", command=lambda: self.carregar_tabela(ordenar="gestor")).pack(side="left", padx=5)

        # === Treeview (tabela) ===
        columns = ["identificador", "nome", "cargo", "empresa", "telefone", "email", "gestor"]
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Cabeçalhos
        self.tree.heading("identificador", text="Identificador")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="e-mail")
        self.tree.heading("gestor", text="Gestor Responsável")

        # Largura das colunas
        for col in columns:
            self.tree.column(col, width=120, anchor="w")

        # Carrega os dados
        self.carregar_tabela()

    def carregar_tabela(self, ordenar=None):
        # Limpa a tabela
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Puxar dados reais do backend
        clientes, empresas, gestores = carregar_dados_excel("./dados_brutos.xlsx")

      # Preparar dados para exibição
        dados = []
        for c in clientes:
            # Pega o gestor do cliente ou, se não houver, pega o gestor da empresa
            gestor_nome = ""
            if c.gestor:
                gestor_nome = c.gestor.nome
            elif c.empresa and c.empresa.clientes:
                # Assume que o gestor principal da empresa é o primeiro gestor encontrado
                if hasattr(c.empresa, "gestor") and c.empresa.gestor:
                    gestor_nome = c.empresa.gestor.nome

            dados.append({
                "identificador": c.identificador,
                "nome": c.nome,
                "cargo": c.cargo,
                "empresa": c.empresa.nome if c.empresa else "",
                "telefone": c.telefone,
                "email": c.email,
                "gestor": gestor_nome
            })

        # Ordenar se necessário
        if ordenar == "nome":
            dados.sort(key=lambda x: x["nome"].lower())
        elif ordenar == "gestor":
            dados.sort(key=lambda x: (x["gestor"].lower(), x["nome"].lower()))

        # Inserir na tabela
        for item in dados:
            self.tree.insert("", "end", values=(
                item["identificador"], item["nome"], item["cargo"],
                item["empresa"], item["telefone"], item["email"], item["gestor"]
            ))
