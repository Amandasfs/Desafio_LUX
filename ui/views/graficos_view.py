# ui/views/graficos_view.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

class GraficosView:
    def __init__(self, parent, dados):
        self.parent = parent
        self.dados = dados
        self.container = None
        self.grafico_var = tk.StringVar()
        self.grafico_frame = None
        
    def show(self):
        self._create_ui()
        
    def hide(self):
        if self.container:
            self.container.destroy()
            
    def atualizar_dados(self, novos_dados):
        self.dados = novos_dados
        self._atualizar_grafico()
            
    def _create_ui(self):
        self.container = tk.Frame(self.parent, bg="#f8fafc", relief="flat")
        self.container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Título
        title_frame = tk.Frame(self.container, bg="#f8fafc")
        title_frame.pack(fill="x", pady=(0, 15))
        tk.Label(title_frame, text="📈 Análises Gráficas", bg="#f8fafc", 
                fg="#00215b", font=("Arial", 16, "bold")).pack(anchor="w")
        
        # Seletor de gráficos
        selector_frame = tk.Frame(self.container, bg="#f8fafc")
        selector_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(selector_frame, text="Selecione o tipo de gráfico:", bg="#f8fafc", 
                fg="#00215b", font=("Arial", 11)).pack(side="left", padx=(0, 10))
        
        opcoes_graficos = [
            "Consumo total por empresa",
            "Consumo Ponta vs Fora Ponta", 
            "Distribuição do consumo total",
            "Evolução do consumo médio",
            "Indicadores de cadastro",
            "Correlação entre Consumo e Valor da Fatura"
        ]
        
        self.grafico_var.set(opcoes_graficos[0])
        grafico_combo = ttk.Combobox(selector_frame, textvariable=self.grafico_var, 
                                    values=opcoes_graficos, state="readonly", width=30)
        grafico_combo.pack(side="left", padx=(0, 10))
        grafico_combo.bind('<<ComboboxSelected>>', self._atualizar_grafico)
        
        # Frame para o gráfico
        self.grafico_frame = tk.Frame(self.container, bg="#ffffff", relief="flat")
        self.grafico_frame.pack(fill="both", expand=True)
        
        # Mostrar gráfico inicial
        self._atualizar_grafico()
        
    def _atualizar_grafico(self, event=None):
        # Limpar frame do gráfico
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
            
        tipo_grafico = self.grafico_var.get()
        fig = self._criar_grafico(tipo_grafico)
        
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
    def _criar_grafico(self, tipo_grafico):
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#f8fafc')
            ax.set_facecolor('#ffffff')
            
            if tipo_grafico == "Consumo total por empresa":
                # Top 10 empresas por consumo
                if 'Consumo Total (kWh)' in self.dados.columns and 'Empresa' in self.dados.columns:
                    consumo_empresas = self.dados.groupby('Empresa')['Consumo Total (kWh)'].sum().nlargest(10)
                    bars = consumo_empresas.plot(kind='bar', ax=ax, color='#00215b', alpha=0.8)
                    ax.set_title('Top 10 Empresas - Consumo Total (kWh)', fontweight='bold', pad=20)
                    ax.tick_params(axis='x', rotation=45)
                    ax.grid(True, alpha=0.3)
                    
                    # Adicionar valores nas barras
                    for i, v in enumerate(consumo_empresas):
                        ax.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')
                else:
                    ax.text(0.5, 0.5, 'Dados de consumo não disponíveis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=12)
                    
            elif tipo_grafico == "Consumo Ponta vs Fora Ponta":
                # Comparação consumo ponta vs fora ponta
                if ('Consumo Ponta (kWh)' in self.dados.columns and 
                    'Consumo Fora Ponta (kWh)' in self.dados.columns):
                    ponta_total = self.dados['Consumo Ponta (kWh)'].sum()
                    fora_ponta_total = self.dados['Consumo Fora Ponta (kWh)'].sum()
                    
                    labels = ['Consumo Ponta', 'Consumo Fora Ponta']
                    valores = [ponta_total, fora_ponta_total]
                    cores = ['#00215b', '#0040b5']
                    
                    wedges, texts, autotexts = ax.pie(valores, labels=labels, colors=cores, 
                                                     autopct='%1.1f%%', startangle=90)
                    
                    ax.set_title('Distribuição: Consumo Ponta vs Fora Ponta', 
                                fontweight='bold', pad=20)
                    
                    # Estilizar textos
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')
                else:
                    ax.text(0.5, 0.5, 'Dados de consumo ponta/fora ponta não disponíveis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=12)
                    
            elif tipo_grafico == "Distribuição do consumo total":
                # Histograma de distribuição do consumo
                if 'Consumo Total (kWh)' in self.dados.columns:
                    consumos = self.dados['Consumo Total (kWh)'].dropna()
                    if len(consumos) > 0:
                        ax.hist(consumos, bins=20, color='#00215b', alpha=0.7, edgecolor='black')
                        ax.set_title('Distribuição do Consumo Total (kWh)', fontweight='bold', pad=20)
                        ax.set_xlabel('Consumo (kWh)')
                        ax.set_ylabel('Frequência')
                        ax.grid(True, alpha=0.3)
                    else:
                        ax.text(0.5, 0.5, 'Não há dados de consumo disponíveis', 
                               ha='center', va='center', transform=ax.transAxes, fontsize=12)
                else:
                    ax.text(0.5, 0.5, 'Dados de consumo não disponíveis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=12)
                    
            elif tipo_grafico == "Evolução do consumo médio":
                # Simular evolução temporal (ajustar conforme dados disponíveis)
                meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                
                if 'Consumo Total (kWh)' in self.dados.columns:
                    # Calcular consumo médio mensal (exemplo)
                    consumo_mensal = [self.dados['Consumo Total (kWh)'].mean() * (0.8 + 0.4 * i/11) 
                                     for i in range(12)]
                    
                    ax.plot(meses, consumo_mensal, marker='o', color='#00215b', linewidth=2, markersize=6)
                    ax.set_title('Evolução do Consumo Médio Mensal', fontweight='bold', pad=20)
                    ax.set_ylabel('Consumo Médio (kWh)')
                    ax.grid(True, alpha=0.3)
                    
                    # Adicionar valores nos pontos
                    for i, v in enumerate(consumo_mensal):
                        ax.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')
                else:
                    ax.text(0.5, 0.5, 'Dados de consumo não disponíveis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=12)
                    
            elif tipo_grafico == "Indicadores de cadastro":
                # Métricas de cadastro
                metricas = ['Total Contatos', 'Empresas Únicas', 'Com Telefone', 'Com Email']
                valores = [
                    len(self.dados),
                    self.dados['Empresa'].nunique() if 'Empresa' in self.dados.columns else 0,
                    self.dados['Telefone'].notna().sum() if 'Telefone' in self.dados.columns else 0,
                    self.dados['e-mail'].notna().sum() if 'e-mail' in self.dados.columns else 0
                ]
                
                bars = ax.bar(metricas, valores, color=['#00215b', '#00308b', '#0040b5', '#0055ff'])
                ax.set_title('Indicadores de Cadastro', fontweight='bold', pad=20)
                ax.grid(True, alpha=0.3)
                
                # Adicionar valores nas barras
                for bar, valor in zip(bars, valores):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{valor}', ha='center', va='bottom', fontweight='bold')
                    
            elif tipo_grafico == "Correlação entre Consumo e Valor da Fatura":
                # Scatter plot de correlação
                if ('Consumo Total (kWh)' in self.dados.columns and 
                    'Valor Médio da Fatura (R$)' in self.dados.columns):
                    x = self.dados['Consumo Total (kWh)'].dropna()
                    y = self.dados['Valor Médio da Fatura (R$)'].dropna()
                    
                    # Garantir que x e y tenham o mesmo tamanho
                    min_len = min(len(x), len(y))
                    x = x.head(min_len)
                    y = y.head(min_len)
                    
                    if len(x) > 0 and len(y) > 0:
                        ax.scatter(x, y, alpha=0.6, color='#00215b', s=50)
                        ax.set_title('Correlação: Consumo vs Valor da Fatura', fontweight='bold', pad=20)
                        ax.set_xlabel('Consumo Total (kWh)')
                        ax.set_ylabel('Valor Médio da Fatura (R$)')
                        ax.grid(True, alpha=0.3)
                        
                        # Adicionar linha de tendência
                        z = np.polyfit(x, y, 1)
                        p = np.poly1d(z)
                        ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2)
                        
                        # Calcular e mostrar coeficiente de correlação
                        correlacao = np.corrcoef(x, y)[0,1]
                        ax.text(0.05, 0.95, f'Correlação: {correlacao:.2f}', 
                               transform=ax.transAxes, fontsize=12, 
                               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
                    else:
                        ax.text(0.5, 0.5, 'Dados insuficientes para análise', 
                               ha='center', va='center', transform=ax.transAxes, fontsize=12)
                else:
                    ax.text(0.5, 0.5, 'Dados de consumo e valor da fatura não disponíveis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=12)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            # Em caso de erro, mostrar mensagem
            error_label = tk.Label(self.grafico_frame, 
                                 text=f"Erro ao gerar gráfico: {str(e)}", 
                                 bg="#ffffff", fg="red", font=("Arial", 12))
            error_label.pack(expand=True)
            return None