# ui/dashboard/components/sidebar.py
import tkinter as tk

def create_sidebar(parent, dashboard):
    # Sidebar com sombra sutil e bordas arredondadas
    sidebar = tk.Frame(parent, bg="#00215b", width=220, relief="flat")
    sidebar.pack(side="left", fill="y", padx=(0, 0))
    sidebar.pack_propagate(False)
    
    # === HEADER DA SIDEBAR COM LOGO ===
    sidebar_header = tk.Frame(sidebar, bg="#001a4d", height=100)
    sidebar_header.pack(fill="x", pady=(0, 10))
    sidebar_header.pack_propagate(False)
    
    # Logo container
    logo_frame = tk.Frame(sidebar_header, bg="#001a4d")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Ícone do sistema
    logo_icon = tk.Label(logo_frame, text="⚡", bg="#001a4d", fg="#00a8ff",
                        font=("Arial", 24, "bold"))
    logo_icon.pack()
    
    # Nome do sistema
    tk.Label(logo_frame, text="LUX SYSTEM", bg="#001a4d", fg="white",
            font=("Arial", 12, "bold")).pack(pady=(5, 0))
    
    tk.Label(logo_frame, text="Dashboard", bg="#001a4d", fg="#a0d2ff",
            font=("Arial", 9)).pack()
    
    # === SEÇÃO DE NAVEGAÇÃO ===
    nav_section = tk.Frame(sidebar, bg="#00215b")
    nav_section.pack(fill="x", pady=(0, 20))
    
    # Título da seção
    nav_title = tk.Label(nav_section, text="NAVEGAÇÃO", bg="#00215b", 
                        fg="#a0d2ff", font=("Arial", 10, "bold"), 
                        pady=8, padx=15)
    nav_title.pack(fill="x", anchor="w")
    
    # Lista de botões de navegação
    botoes = [
        ("👥", "Contatos", dashboard.mostrar_contatos),
        ("🏢", "Empresas", dashboard.mostrar_empresas),
        ("📊", "Consumo", dashboard.mostrar_consumo),
        ("📈", "Gráficos", dashboard.mostrar_graficos),
        ("👨‍💼", "Gestores", dashboard.mostrar_gestores)
    ]
    
    for icon, texto, comando in botoes:
        btn_container = tk.Frame(nav_section, bg="#00215b", height=40)
        btn_container.pack(fill="x", padx=8, pady=1)
        btn_container.pack_propagate(False)
        
        btn = tk.Frame(btn_container, bg="#00215b", cursor="hand2")
        btn.pack(fill="both", expand=True, padx=2)
        
        # Ícone
        icon_label = tk.Label(btn, text=icon, bg="#00215b", fg="#a0d2ff",
                            font=("Arial", 14), width=3)
        icon_label.pack(side="left", padx=(10, 0))
        
        # Texto
        text_label = tk.Label(btn, text=texto, bg="#00215b", fg="white",
                            font=("Arial", 11), anchor="w")
        text_label.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Indicador de seleção (invisível inicialmente)
        indicator = tk.Frame(btn, bg="#00a8ff", width=3, height=0)
        indicator.pack(side="right", fill="y", padx=(0, 5))
        indicator.pack_propagate(False)
        
        # Configurar comandos e efeitos
        def make_command(cmd, container=btn, ind=indicator, icn=icon_label, txt=text_label):
            def wrapper():
                # Resetar todos os botões primeiro
                for widget in nav_section.winfo_children():
                    if isinstance(widget, tk.Frame) and hasattr(widget, 'children'):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Frame):
                                child.config(bg="#00215b")
                                # Encontrar e resetar ícone e texto
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, tk.Label):
                                        if grandchild['text'] in ["👥", "🏢", "📊", "📈", "👨‍💼"]:
                                            grandchild.config(bg="#00215b", fg="#a0d2ff")
                                        else:
                                            grandchild.config(bg="#00215b", fg="white")
                                # Resetar indicador
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, tk.Frame):
                                        grandchild.config(bg="#00215b")
                
                # Aplicar estilo ativo ao botão clicado
                container.config(bg="#00308b")
                ind.config(bg="#00a8ff")
                icn.config(bg="#00308b", fg="#00a8ff")
                txt.config(bg="#00308b", fg="white")
                
                # Executar comando
                cmd()
            return wrapper
        
        # Efeitos hover
        def on_enter(e, container=btn, ind=indicator, icn=icon_label, txt=text_label):
            current_bg = container.cget('bg')
            if current_bg == "#00215b":  # Só aplica hover se não estiver ativo
                container.config(bg="#00308b")
                icn.config(bg="#00308b", fg="#00a8ff")
                txt.config(bg="#00308b", fg="white")
        
        def on_leave(e, container=btn, ind=indicator, icn=icon_label, txt=text_label):
            current_bg = container.cget('bg')
            if current_bg == "#00308b":  # Só volta se não estiver ativo
                # Verificar se é o botão ativo
                active_indicator = ind.cget('bg')
                if active_indicator != "#00a8ff":
                    container.config(bg="#00215b")
                    icn.config(bg="#00215b", fg="#a0d2ff")
                    txt.config(bg="#00215b", fg="white")
        
        btn.bind("<Button-1>", lambda e, cmd=make_command(comando): cmd())
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Tornar os labels também clicáveis
        for label in [icon_label, text_label]:
            label.bind("<Button-1>", lambda e, cmd=make_command(comando): cmd())
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
    
    # === SEÇÃO DE FERRAMENTAS ===
    tools_section = tk.Frame(sidebar, bg="#00215b")
    tools_section.pack(fill="x", pady=(0, 20))
    
    tk.Label(tools_section, text="FERRAMENTAS", bg="#00215b", 
            fg="#a0d2ff", font=("Arial", 10, "bold"), 
            pady=8, padx=15).pack(fill="x", anchor="w")
    
    tools_buttons = [
        ("⚙️", "Configurações", lambda: None),
        ("❓", "Ajuda", lambda: None)
    ]
    
    for icon, texto, comando in tools_buttons:
        btn_container = tk.Frame(tools_section, bg="#00215b", height=35)
        btn_container.pack(fill="x", padx=8, pady=1)
        btn_container.pack_propagate(False)
        
        btn = tk.Frame(btn_container, bg="#00215b", cursor="hand2")
        btn.pack(fill="both", expand=True, padx=2)
        
        tk.Label(btn, text=icon, bg="#00215b", fg="#a0d2ff",
                font=("Arial", 12), width=3).pack(side="left", padx=(10, 0))
        
        tk.Label(btn, text=texto, bg="#00215b", fg="#e0e0e0",
                font=("Arial", 10), anchor="w").pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Efeitos hover para ferramentas
        def on_enter_tools(e, container=btn):
            container.config(bg="#00308b")
            for child in container.winfo_children():
                child.config(bg="#00308b")
        
        def on_leave_tools(e, container=btn):
            container.config(bg="#00215b")
            for child in container.winfo_children():
                if child.winfo_class() == 'Label':
                    if child['text'] in ["⚙️", "❓"]:
                        child.config(bg="#00215b", fg="#a0d2ff")
                    else:
                        child.config(bg="#00215b", fg="#e0e0e0")
        
        btn.bind("<Enter>", on_enter_tools)
        btn.bind("<Leave>", on_leave_tools)
    
    # === RODAPÉ DA SIDEBAR ===
    sidebar_footer = tk.Frame(sidebar, bg="#001a4d", height=60)
    sidebar_footer.pack(side="bottom", fill="x")
    sidebar_footer.pack_propagate(False)
    
    footer_content = tk.Frame(sidebar_footer, bg="#001a4d")
    footer_content.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(footer_content, text="v2.1.0", bg="#001a4d", 
            fg="#a0d2ff", font=("Arial", 8)).pack(pady=(2, 0))

    return sidebar