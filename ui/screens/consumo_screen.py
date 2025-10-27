import tkinter as tk
from tkinter import ttk
from services.parser_excel import carregar_dados_excel
import os
import sys


def get_resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, compatível com executável PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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

        # === Controles de filtro e ordenação ===
        control_frame = tk.Frame(self.frame, bg="#f0f0f0")
        control_frame.pack(fill="x", pady=(0, 10))

        tk.Label(control_frame, text="Filtrar por Distribuidora:", bg="#f0f0f0").pack(side="left", padx=(0, 5))
        self.filtro_var = tk.StringVar()
        self.combo_filtro = ttk.Combobox(control_frame, textvariable=self.filtro_var, state="readonly", width=25)
        self.combo_filtro.pack(side="left", padx=(0, 15))
        self.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_dados)

        tk.Label(control_frame, text="Ordenar por:", bg="#f0f0f0").pack(side="left", padx=(10, 5))
        self.ordenar_var = tk.StringVar(value="Empresa")
        self.combo_ordenar = ttk.Combobox(
            control_frame,
            textvariable=self.ordenar_var,
            state="readonly",
            values=["Empresa", "Distribuidora", "Modalidade", "Valor Médio"]
        )
        self.combo_ordenar.pack(side="left", padx=(0, 5))

        tk.Button(
            control_frame,
            text="Aplicar",
            command=self.aplicar_ordenacao,
            bg="#004aad",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10
        ).pack(side="left", padx=(10, 0))

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
            self.tree.column(col, width=160, anchor="w")

        # Carrega dados do backend
        self.empresas = []
        self.carregar_dados()

    # === Carregamento de dados ===
    def carregar_dados(self):
        """Carrega os dados de consumo do arquivo Excel."""
        try:
            excel_path = get_resource_path("dados_brutos.xlsx")
            _, empresas, _ = carregar_dados_excel(excel_path)
            self.empresas = empresas

            self.popular_tabela(empresas)
            self.atualizar_opcoes_filtro()
        except Exception as e:
            tk.Label(
                self.frame,
                text=f"Erro ao carregar dados: {e}",
                fg="red",
                bg="#f0f0f0",
                font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(5, 10))

    # === Tabela ===
    def popular_tabela(self, empresas):
        """Popula a tabela com os dados das empresas."""
        for item in self.tree.get_children():
            self.tree.delete(item)

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

    # === Filtro ===
    def atualizar_opcoes_filtro(self):
        """Atualiza a combobox de filtro com as distribuidoras disponíveis."""
        distribuidoras = sorted({e.distribuidora for e in self.empresas if e.distribuidora})
        self.combo_filtro["values"] = ["Todas"] + distribuidoras
        self.combo_filtro.set("Todas")

    def filtrar_dados(self, event=None):
        """Filtra as empresas pela distribuidora selecionada."""
        filtro = self.filtro_var.get()
        if filtro == "Todas" or not filtro:
            filtradas = self.empresas
        else:
            filtradas = [e for e in self.empresas if e.distribuidora == filtro]
        self.popular_tabela(filtradas)

    # === Ordenação ===
    def aplicar_ordenacao(self):
        """Ordena a tabela conforme o critério selecionado."""
        criterio = self.ordenar_var.get()
        empresas = list(self.empresas)

        if criterio == "Empresa":
            empresas.sort(key=lambda e: (e.nome or "").lower())
        elif criterio == "Distribuidora":
            empresas.sort(key=lambda e: (e.distribuidora or "").lower())
        elif criterio == "Modalidade":
            empresas.sort(key=lambda e: (e.modalidade or "").lower())
        elif criterio == "Valor Médio":
            empresas.sort(key=lambda e: e.valor_medio or 0, reverse=True)

        # Se houver filtro ativo, aplica antes de exibir
        filtro = self.filtro_var.get()
        if filtro and filtro != "Todas":
            empresas = [e for e in empresas if e.distribuidora == filtro]

        self.popular_tabela(empresas)
