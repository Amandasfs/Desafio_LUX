# ui/dashboard/dashboard_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.parser_excel import carregar_dados

# Componentes
from ui.dashboard.components.header import create_header as Header
from ui.dashboard.components.sidebar import create_sidebar as Sidebar
from ui.dashboard.components.toolbar import create_toolbar as Toolbar
from ui.dashboard.components.cards import create_cards as Cards

# Views
from ui.views.contatos_view import ContatosView
from ui.views.empresas_view import EmpresasView
from ui.views.consumo_view import ConsumoView
from ui.views.graficos_view import GraficosView
from ui.views.gestores_view import GestoresView


class DashboardWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Sistema de Gerenciamento de Contatos")
        self.root.geometry("1300x800")
        self.root.configure(bg="#f8fafc")

        # === Estilos ===
        self.setup_styles()
        self.dados = carregar_dados()

        # === Componentes fixos ===
        Header(root)
        self.toolbar = Toolbar(root, self)
        self.sidebar = Sidebar(root, self)

        # === Container principal ===
        self.main_container = tk.Frame(root, bg="#f8fafc")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # === Sidebar e conteúdo ===
        self.sidebar_frame = self.sidebar.create(self.main_container)
        self.content_frame = tk.Frame(self.main_container, bg="#ffffff", relief="flat")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # === Cards e conteúdo principal ===
        self.cards = Cards(self.content_frame, self.dados)
        self.main_content = tk.Frame(self.content_frame, bg="#ffffff")
        self.main_content.pack(fill="both", expand=True)

        # === Views ===
        self.views = {
            "contatos": lambda: ContatosView(self),
            "empresas": lambda: EmpresasView(self),
            "consumo": lambda: ConsumoView(self),
            "graficos": lambda: GraficosView(self),
            "gestores": lambda: GestoresView(self),
        }

        self.current_view = None
        self.mostrar_contatos()

    # === ESTILOS ===
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="#333333",
            rowheight=25,
            fieldbackground="white",
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#00215b",
            foreground="white",
            relief="flat",
            font=("Arial", 11, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#00308b")])

    # === FUNÇÕES DE LIMPEZA E TROCA DE VIEW ===
    def limpar_main_area(self):
        """Remove widgets da área principal antes de carregar uma nova view."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def _show_view(self, nome_view):
        """Troca entre as telas (views)"""
        self.limpar_main_area()
        self.views[nome_view]()  # executa função da view
        self.cards.atualizar()

    # === AÇÕES DE NAVEGAÇÃO ===
    def mostrar_contatos(self):
        self._show_view("contatos")

    def mostrar_empresas(self):
        self._show_view("empresas")

    def mostrar_consumo(self):
        self._show_view("consumo")

    def mostrar_graficos(self):
        self._show_view("graficos")

    def mostrar_gestores(self):
        self._show_view("gestores")

    # === FUNÇÕES ===
    def buscar(self):
        """Busca por nome"""
        termo = self.toolbar.get_search_term()
        if termo:
            self.dados = self.dados[self.dados["Nome"].str.lower().str.contains(termo.lower())]
        else:
            self.dados = carregar_dados()

        self.mostrar_contatos()
        self.cards.atualizar()

    def organizar_dados(self):
        """Organiza dados por diferentes critérios"""
        from tkinter import simpledialog

        opcoes_ordenacao = [
            "Nome A-Z",
            "Nome Z-A",
            "Empresa A-Z",
            "Consumo Maior-Menor",
        ]

        escolha = simpledialog.askstring(
            "Organizar Dados",
            "Selecione o critério de ordenação:\n\n"
            + "\n".join([f"{i+1}. {opcao}" for i, opcao in enumerate(opcoes_ordenacao)]),
        )

        if escolha:
            try:
                opcao_num = int(escolha)
                if opcao_num == 1:
                    self.dados = self.dados.sort_values("Nome")
                elif opcao_num == 2:
                    self.dados = self.dados.sort_values("Nome", ascending=False)
                elif opcao_num == 3:
                    self.dados = self.dados.sort_values("Empresa")
                elif opcao_num == 4:
                    if "Consumo Total (kWh)" in self.dados.columns:
                        self.dados = self.dados.sort_values(
                            "Consumo Total (kWh)", ascending=False
                        )

                self._show_view("contatos")
                self.cards.atualizar()

            except (ValueError, IndexError):
                messagebox.showerror("Erro", "Opção inválida!")

    def atualizar_contato(self):
        """Atualizar contato"""
        try:
            self.views["contatos"]().atualizar_contato()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar o contato.\n\n{e}")

    def cadastrar_contato(self):
        """Cadastrar novo contato"""
        try:
            self.views["contatos"]().cadastrar_contato()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar o contato.\n\n{e}")
