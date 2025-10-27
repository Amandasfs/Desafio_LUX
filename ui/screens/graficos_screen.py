import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from services.parser_excel import carregar_dados_excel
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, seja no dev ou no exe PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Diretório temporário criado pelo PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GraficosScreen:
    def __init__(self, parent):
        self.parent = parent

        # === Frame container com scroll vertical/horizontal ===
        self.frame = tk.Frame(parent, bg="#f9f9f9")
        self.frame.pack(fill="both", expand=True)

        self.canvas_frame = tk.Canvas(self.frame, bg="#f9f9f9")
        self.canvas_frame.pack(side="left", fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas_frame.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x = tk.Scrollbar(parent, orient="horizontal", command=self.canvas_frame.xview)
        self.scroll_x.pack(side="bottom", fill="x")

        self.canvas_frame.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.canvas_frame.bind('<Configure>', lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas_frame, bg="#f9f9f9")
        self.canvas_frame.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # === Título ===
        tk.Label(
            self.inner_frame,
            text="Painel de Gráficos",
            font=("Arial", 18, "bold"),
            bg="#f9f9f9",
            fg="#00215b"
        ).pack(anchor="w", pady=(0, 10))

        # === Caminho do Excel (compatível com .exe) ===
        excel_path = resource_path("dados_brutos.xlsx")

        # === Carrega dados ===
        self.clientes, self.empresas, self.gestores = carregar_dados_excel(excel_path)

        # === ChoiceBox para seleção de gráfico ===
        tk.Label(self.inner_frame, text="Escolha o tipo de gráfico:", bg="#f9f9f9", font=("Arial", 11)).pack(anchor="w")
        self.grafico_var = tk.StringVar()
        opcoes = ["Consumo Ponta vs Fora Ponta", "Distribuição do consumo total"]
        self.combobox = ttk.Combobox(self.inner_frame, textvariable=self.grafico_var, state="readonly", values=opcoes, width=40)
        self.combobox.pack(anchor="w", pady=(0,10))
        self.combobox.bind("<<ComboboxSelected>>", self.atualizar_grafico)

        # === Canvas matplotlib no inner_frame ===
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.inner_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Configurações globais do matplotlib
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 16,
            'axes.labelsize': 14,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 11,
            'figure.titlesize': 18
        })

    def atualizar_grafico(self, event=None):
        self.ax.clear()
        grafico = self.grafico_var.get()

        try:
            if not self.empresas and not self.clientes:
                self.ax.text(0.5,0.5,"Nenhum dado disponível", ha='center', va='center', fontsize=14, transform=self.ax.transAxes)
                self.canvas.draw()
                return

            # ================= Gráfico 1 - Consumo Ponta vs Fora Ponta =================
            if grafico == "Consumo Ponta vs Fora Ponta":
                nomes = [e.nome for e in self.empresas]
                ponta = [e.consumo_ponta for e in self.empresas]
                fora_ponta = [e.consumo_fora_ponta for e in self.empresas]

                x = range(len(nomes))
                
                # Diminuir a largura das barras para aumentar espaço
                bar_width = 0.25
                self.ax.bar([i - bar_width/2 for i in x], ponta, width=bar_width, label="Ponta", color="#00215b")
                self.ax.bar([i + bar_width/2 for i in x], fora_ponta, width=bar_width, label="Fora Ponta", color="#00a8ff")
                
                self.ax.set_xticks(x)
                self.ax.set_xticklabels(nomes, rotation=50, ha='right')  # girar mais para dar espaço
                self.ax.set_ylabel("Consumo (kWh)")
                self.ax.set_title("Consumo Ponta vs Fora Ponta", pad=20)
                self.ax.legend()
                
                # Margens um pouco maiores para espaçamento extra
                self.ax.margins(x=0.2, y=0.1)

            # ================= Gráfico 2 - Distribuição do consumo total (Pizza) =================
            elif grafico == "Distribuição do consumo total":
                labels = [e.nome for e in self.empresas]
                sizes = [e.consumo_ponta + e.consumo_fora_ponta for e in self.empresas]
                valid_data = [(label, size) for label, size in zip(labels, sizes) if size > 0]

                if valid_data:
                    labels, sizes = zip(*valid_data)
                    wedges, texts, autotexts = self.ax.pie(
                        sizes,
                        labels=labels,
                        autopct='%1.1f%%',
                        startangle=140,
                        textprops={'fontsize': 12}
                    )
                    for autotext in autotexts:
                        autotext.set_fontsize(10)
                        autotext.set_color('white')
                        autotext.set_weight('bold')
                    self.ax.set_title("Distribuição do Consumo Total", pad=20)
                    self.fig.tight_layout()
                else:
                    self.ax.text(0.5,0.5,"Nenhum consumo disponível", ha='center', va='center', fontsize=14, transform=self.ax.transAxes)

            self.canvas.draw()

        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5,0.5,f"Erro ao gerar gráfico:\n{str(e)}", ha='center', va='center', fontsize=12, transform=self.ax.transAxes)
            self.canvas.draw()
