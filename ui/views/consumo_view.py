# ui/views/consumo_view.py
import tkinter as tk
from tkinter import ttk
import pandas as pd

class ConsumoView:
    def __init__(self, parent, dados):
        self.parent = parent
        self.dados = dados
        self.container = None
        self.tree = None
        
    def show(self):
        self._create_ui()
        
    def hide(self):
        if self.container:
            self.container.destroy()
            
    def atualizar_dados(self, novos_dados):
        self.dados = novos_dados
        if self.tree:
            self._atualizar_treeview()
            
    def _create_ui(self):
        self.container = tk.Frame(self.parent, bg="#f8fafc", relief="flat")
        self.container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Título
        title_frame = tk.Frame(self.container, bg="#f8fafc")
        title_frame.pack(fill="x", pady=(0, 15))
        tk.Label(title_frame, text="📊 Dados de Consumo", bg="#f8fafc", 
                fg="#00215b", font=("Arial", 16, "bold")).pack(anchor="w")
        
        # Treeview
        tree_frame = tk.Frame(self.container, bg="#f8fafc")
        tree_frame.pack(fill="both", expand=True)
        
        # Colunas específicas para consumo
        colunas = [
            'Empresa',
            'Distribuidora', 
            'Modalidade Tarifária',
            'Consumo Ponta (kWh)',
            'Consumo Fora Ponta (kWh)',
            'Valor Médio da Fatura (R$)',
            'Gestor Responsável (LUX)'
        ]
        
        # Verificar quais colunas existem nos dados
        colunas_existentes = [col for col in colunas if col in self.dados.columns]
        
        self.tree = ttk.Treeview(tree_frame, columns=colunas_existentes, 
                                show="headings", height=15)
        
        # Configurar colunas
        for col in colunas_existentes:
            self.tree.heading(col, text=col)
            if col == 'Empresa':
                self.tree.column(col, width=200)
            elif col == 'Distribuidora':
                self.tree.column(col, width=150)
            elif col == 'Modalidade Tarifária':
                self.tree.column(col, width=150)
            elif 'Consumo' in col:
                self.tree.column(col, width=140)
            elif 'Valor' in col:
                self.tree.column(col, width=150)
            elif 'Gestor' in col:
                self.tree.column(col, width=180)
            else:
                self.tree.column(col, width=120)
            
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self._atualizar_treeview()
        
    def _atualizar_treeview(self):
        if not self.tree:
            return
            
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Popular com dados formatados
        for _, row in self.dados.iterrows():
            valores = []
            for col in self.tree['columns']:
                valor = row[col] if col in row else ''
                
                # Formatar valores numéricos
                if 'kWh' in col and pd.notna(valor):
                    try:
                        valores.append(f"{float(valor):,.0f}")
                    except (ValueError, TypeError):
                        valores.append("N/A")
                elif 'R$' in col and pd.notna(valor):
                    try:
                        valores.append(f"R$ {float(valor):,.2f}")
                    except (ValueError, TypeError):
                        valores.append("N/A")
                else:
                    valores.append(str(valor) if pd.notna(valor) else "N/A")
                    
            self.tree.insert("", "end", values=valores)