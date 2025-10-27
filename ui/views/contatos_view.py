# ui/views/contatos_view.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd

class ContatosView:
    def __init__(self, parent, dados):
        self.parent = parent
        self.dados = dados
        self.container = None
        self.tree = None
        self.gestor_var = tk.StringVar(value="Todos os Gestores")
        
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
        
        # Título e filtros
        header_frame = tk.Frame(self.container, bg="#f8fafc")
        header_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(header_frame, text="📋 Lista de Contatos", bg="#f8fafc", 
                fg="#00215b", font=("Arial", 16, "bold")).pack(anchor="w")
        
        # Filtro por gestor
        filter_frame = tk.Frame(header_frame, bg="#f8fafc")
        filter_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(filter_frame, text="Filtrar por Gestor:", bg="#f8fafc", 
                fg="#00215b", font=("Arial", 11)).pack(side="left", padx=(0, 10))
        
        # Obter lista de gestores
        gestores = ["Todos os Gestores"]
        if 'Gestor Responsável (LUX)' in self.dados.columns:
            gestores.extend(self.dados['Gestor Responsável (LUX)'].dropna().unique().tolist())
        
        gestor_combo = ttk.Combobox(filter_frame, textvariable=self.gestor_var, 
                                   values=gestores, state="readonly", width=30)
        gestor_combo.pack(side="left", padx=(0, 10))
        gestor_combo.bind('<<ComboboxSelected>>', self._filtrar_por_gestor)
        
        # Treeview
        tree_frame = tk.Frame(self.container, bg="#f8fafc")
        tree_frame.pack(fill="both", expand=True)
        
        # Colunas específicas para contatos
        colunas = [
            'Identificador',
            'Nome', 
            'Cargo',
            'Empresa',
            'Telefone',
            'e-mail',
            'Gestor Responsável (LUX)'
        ]
        
        # Verificar quais colunas existem nos dados
        colunas_existentes = [col for col in colunas if col in self.dados.columns]
        
        self.tree = ttk.Treeview(tree_frame, columns=colunas_existentes, 
                                show="headings", height=15)
        
        # Configurar colunas
        for col in colunas_existentes:
            self.tree.heading(col, text=col)
            if col == 'Nome':
                self.tree.column(col, width=180)
            elif col == 'Identificador':
                self.tree.column(col, width=100)
            elif col == 'Cargo':
                self.tree.column(col, width=150)
            elif col == 'Empresa':
                self.tree.column(col, width=180)
            elif col == 'Telefone':
                self.tree.column(col, width=120)
            elif col == 'e-mail':
                self.tree.column(col, width=200)
            elif 'Gestor' in col:
                self.tree.column(col, width=180)
            else:
                self.tree.column(col, width=120)
            
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self._atualizar_treeview()
        
    def _filtrar_por_gestor(self, event=None):
        self._atualizar_treeview()
        
    def _atualizar_treeview(self):
        if not self.tree:
            return
            
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filtrar dados por gestor selecionado
        dados_filtrados = self.dados.copy()
        gestor_selecionado = self.gestor_var.get()
        
        if (gestor_selecionado != "Todos os Gestores" and 
            'Gestor Responsável (LUX)' in self.dados.columns):
            dados_filtrados = self.dados[
                self.dados['Gestor Responsável (LUX)'] == gestor_selecionado
            ]
        
        # Popular com dados
        for _, row in dados_filtrados.iterrows():
            valores = []
            for col in self.tree['columns']:
                valor = row[col] if col in row else ''
                valores.append(str(valor) if pd.notna(valor) else "N/A")
                    
            self.tree.insert("", "end", values=valores)
            
    def atualizar_contato(self):
        """Atualizar contato existente"""
        from tkinter import simpledialog
        
        contato_nome = simpledialog.askstring("Atualizar Contato", 
                                            "Digite o nome do contato a ser atualizado:")
        if contato_nome:
            contato = self.dados[self.dados['Nome'].str.contains(contato_nome, case=False, na=False)]
            if len(contato) == 0:
                messagebox.showerror("Erro", "Contato não encontrado!")
                return
                
            # Mostrar informações atuais
            contato_info = f"Contato encontrado:\n\nNome: {contato.iloc[0]['Nome']}\n"
            if 'Empresa' in contato.columns:
                contato_info += f"Empresa: {contato.iloc[0]['Empresa']}\n"
            if 'Telefone' in contato.columns:
                contato_info += f"Telefone: {contato.iloc[0]['Telefone']}\n"
                
            contato_info += "\nDigite os novos dados:"
            
            # Aqui você pode expandir para um formulário mais completo
            novo_nome = simpledialog.askstring("Atualizar Contato", contato_info, 
                                             initialvalue=contato.iloc[0]['Nome'])
            if novo_nome:
                # Em uma aplicação real, isso salvaria no backend
                index = contato.index[0]
                self.dados.at[index, 'Nome'] = novo_nome
                messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
                self._atualizar_treeview()
                
    def cadastrar_contato(self):
        """Cadastrar novo contato"""
        from tkinter import simpledialog
        
        # Coletar informações do novo contato
        nome = simpledialog.askstring("Cadastrar Novo Contato", "Nome completo:")
        if not nome:
            return
            
        empresa = simpledialog.askstring("Cadastrar Novo Contato", "Empresa:")
        telefone = simpledialog.askstring("Cadastrar Novo Contato", "Telefone:")
        cargo = simpledialog.askstring("Cadastrar Novo Contato", "Cargo:")
        email = simpledialog.askstring("Cadastrar Novo Contato", "E-mail:")
        
        # Criar novo registro
        novo_contato = {
            'Nome': nome,
            'Empresa': empresa if empresa else '',
            'Telefone': telefone if telefone else '',
            'Cargo': cargo if cargo else '',
            'e-mail': email if email else '',
            'Identificador': f"CT{len(self.dados) + 1:04d}"  # Gerar ID automático
        }
        
        # Adicionar ao DataFrame (em uma aplicação real, isso salvaria no backend)
        novo_df = pd.DataFrame([novo_contato])
        self.dados = pd.concat([self.dados, novo_df], ignore_index=True)
        
        messagebox.showinfo("Sucesso", "Contato cadastrado com sucesso!")
        self._atualizar_treeview()