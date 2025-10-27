import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from services.parser_excel import carregar_dados_excel


class GraficosScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f9f9f9")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === Título ===
        tk.Label(
            self.frame,
            text="Painel de Gráficos",
            font=("Arial", 18, "bold"),
            bg="#f9f9f9",
            fg="#00215b"
        ).pack(anchor="w", pady=(0, 10))

        # === Carrega os dados do backend ===
        self.clientes, self.empresas, self.gestores = carregar_dados_excel("./dados_brutos.xlsx")

        # === ChoiceBox de seleção de gráfico ===
        tk.Label(self.frame, text="Escolha o tipo de gráfico:", bg="#f9f9f9", font=("Arial", 11)).pack(anchor="w")
        self.grafico_var = tk.StringVar()

        opcoes = [
            "Consumo total por empresa",
            "Consumo Ponta vs Fora Ponta",
            "Distribuição do consumo total",
            "Evolução do consumo médio",
            "Distribuidora x Modalidade Tarifária"
        ]

        self.combobox = ttk.Combobox(
            self.frame, textvariable=self.grafico_var, state="readonly", values=opcoes, width=40
        )
        self.combobox.pack(anchor="w", pady=(0, 10))
        self.combobox.bind("<<ComboboxSelected>>", self.atualizar_grafico)

        # === Canvas com scrollbar para matplotlib ===
        canvas_frame = tk.Frame(self.frame)
        canvas_frame.pack(fill="both", expand=True)

        self.scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")

        self.inner_canvas = tk.Canvas(canvas_frame, bg="#f9f9f9", xscrollcommand=self.scroll_x.set)
        self.inner_canvas.pack(side="left", fill="both", expand=True)

        self.scroll_x.config(command=self.inner_canvas.xview)

        self.fig, self.ax = plt.subplots(figsize=(14, 9), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.inner_canvas)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="top", fill="both", expand=True)

        # Atualiza a região rolável
        self.inner_canvas.update_idletasks()
        self.inner_canvas.config(scrollregion=self.inner_canvas.bbox("all"))

        # Configurações de fonte globais
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
        grafico = self.grafico_var.get()
        self.ax.clear()

        if not self.empresas and not self.clientes:
            self.ax.text(0.5, 0.5, "Nenhum dado disponível", ha="center", va="center", fontsize=14, transform=self.ax.transAxes)
            self.canvas.draw()
            return

        try:
            # === Gráfico 1 - Consumo total por empresa ===
            if grafico == "Consumo total por empresa":
                nomes = [e.nome for e in self.empresas]
                consumos = [e.consumo_ponta + e.consumo_fora_ponta for e in self.empresas]

                bars = self.ax.bar(nomes, consumos, color="#004aad", width=0.7)
                self.ax.set_ylabel("Consumo Total (kWh)")
                self.ax.set_title("Consumo Total por Empresa", pad=20)
                self.ax.tick_params(axis='x', rotation=45, labelsize=10)

                for bar in bars:
                    h = bar.get_height()
                    self.ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.0f}', ha='center', va='bottom', fontsize=9)

            # === Gráfico 2 - Consumo Ponta vs Fora Ponta ===
            elif grafico == "Consumo Ponta vs Fora Ponta":
                nomes = [e.nome for e in self.empresas]
                ponta = [e.consumo_ponta for e in self.empresas]
                fora_ponta = [e.consumo_fora_ponta for e in self.empresas]

                x = range(len(nomes))
                bar_width = 0.35
                self.ax.bar([i - bar_width/2 for i in x], ponta, width=bar_width, label="Ponta", color="#00215b")
                self.ax.bar([i + bar_width/2 for i in x], fora_ponta, width=bar_width, label="Fora Ponta", color="#00a8ff")

                self.ax.set_xticks(x)
                self.ax.set_xticklabels(nomes, rotation=45, ha='right', fontsize=10)
                self.ax.set_ylabel("Consumo (kWh)")
                self.ax.set_title("Consumo Ponta vs Fora Ponta", pad=20)
                self.ax.legend(fontsize=11)
                self.ax.margins(x=0.05)

            # === Gráfico 3 - Distribuição do consumo total (pizza) ===
            elif grafico == "Distribuição do consumo total":
                labels = [e.nome for e in self.empresas]
                sizes = [e.consumo_ponta + e.consumo_fora_ponta for e in self.empresas]
                valid_data = [(l, s) for l, s in zip(labels, sizes) if s > 0]
                if valid_data:
                    labels, sizes = zip(*valid_data)
                    wedges, texts, autotexts = self.ax.pie(
                        sizes, labels=labels, autopct='%1.1f%%', startangle=140,
                        textprops={'fontsize': 11}
                    )
                    for autotext in autotexts:
                        autotext.set_fontsize(10)
                        autotext.set_color('white')
                        autotext.set_weight('bold')
                    self.ax.set_title("Distribuição do Consumo Total", pad=20)
                else:
                    self.ax.text(0.5, 0.5, "Nenhum consumo disponível", ha="center", va="center", fontsize=14, transform=self.ax.transAxes)

            # === Gráfico 4 - Evolução do consumo médio ===
            elif grafico == "Evolução do consumo médio":
                clientes = [c.nome for c in self.clientes]
                valores = [c.empresa.valor_medio if c.empresa and c.empresa.valor_medio else 0 for c in self.clientes]

                if any(valores):
                    self.ax.plot(clientes, valores, marker='o', linestyle='-', color="#004aad", linewidth=2, markersize=6)
                    self.ax.set_ylabel("Valor Médio da Fatura (R$)")
                    self.ax.set_xlabel("Clientes")
                    self.ax.set_title("Evolução do Consumo Médio", pad=20)
                    self.ax.tick_params(axis='x', rotation=45, labelsize=10)
                    self.ax.grid(True, alpha=0.3)

                    for i, (cliente, valor) in enumerate(zip(clientes, valores)):
                        if valor > 0:
                            self.ax.annotate(f'R$ {valor:.2f}', (i, valor), xytext=(0, 8), textcoords='offset points',
                                             ha='center', fontsize=9)
                else:
                    self.ax.text(0.5, 0.5, "Nenhum valor médio disponível", ha="center", va="center", fontsize=14, transform=self.ax.transAxes)

            # === Gráfico 5 - Distribuidora x Modalidade Tarifária ===
            elif grafico == "Distribuidora x Modalidade Tarifária":
                df = pd.DataFrame({
                    "Distribuidora": [e.distribuidora for e in self.empresas if e.distribuidora],
                    "Modalidade": [e.modalidade for e in self.empresas if e.modalidade]
                })
                tabela = df.groupby(["Distribuidora", "Modalidade"]).size().unstack(fill_value=0)

                if not tabela.empty:
                    tabela.plot(kind="bar", stacked=True, ax=self.ax,
                                color=["#004aad", "#00a8ff", "#66c2ff", "#00215b", "#a6d4ff"],
                                width=0.8)
                    self.ax.set_title("Distribuidora x Modalidade Tarifária", pad=20)
                    self.ax.set_ylabel("Quantidade de Empresas")
                    self.ax.set_xlabel("Distribuidora")
                    self.ax.legend(title="Modalidade Tarifária", fontsize=11, title_fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
                    self.ax.tick_params(axis='x', rotation=45, labelsize=10)
                    self.fig.subplots_adjust(right=0.8)
                else:
                    self.ax.text(0.5, 0.5, "Dados insuficientes para o gráfico", ha="center", va="center", fontsize=14, transform=self.ax.transAxes)

            self.fig.tight_layout(pad=4.0)
            self.canvas.draw()
            self.inner_canvas.config(scrollregion=self.inner_canvas.bbox("all"))

        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Erro ao gerar gráfico:\n{str(e)}", ha="center", va="center", fontsize=12, transform=self.ax.transAxes)
            self.canvas.draw()
