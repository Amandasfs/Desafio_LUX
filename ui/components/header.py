# ui/dashboard/components/header.py
import tkinter as tk

def create_header(root):
    # Header principal
    header = tk.Frame(root, bg="#00215b", height=120)
    header.pack(fill="x")
    
    # Barra de destaque no topo
    top_bar = tk.Frame(header, bg="#00a8ff", height=4)
    top_bar.pack(fill="x")
    
    # Container principal responsivo
    header_content = tk.Frame(header, bg="#00215b", height=116)
    header_content.pack(fill="both", expand=True, padx=20, pady=0)  # Padding lateral responsivo
    
    # Grid responsivo para organizar as seções
    header_content.grid_columnconfigure(0, weight=1)  # Lado esquerdo
    header_content.grid_columnconfigure(1, weight=2)  # Centro
    header_content.grid_columnconfigure(2, weight=1)  # Lado direito
    header_content.grid_rowconfigure(0, weight=1)
    
    # === LADO ESQUERDO - LOGO E TÍTULO (Responsivo) ===
    left_section = tk.Frame(header_content, bg="#00215b")
    left_section.grid(row=0, column=0, sticky="w", padx=(0, 20))
    
    def update_left_section():
        # Obter largura atual do header
        header_width = header_content.winfo_width()
        
        if header_width < 800:  # Telas pequenas
            # Layout compacto
            for widget in left_section.winfo_children():
                widget.destroy()
            
            compact_container = tk.Frame(left_section, bg="#00215b")
            compact_container.pack(anchor="w")
            
            # Logo e título na mesma linha
            logo_title_frame = tk.Frame(compact_container, bg="#00215b")
            logo_title_frame.pack(anchor="w")
            
            tk.Label(logo_title_frame, text="⚡", bg="#00215b", fg="#00a8ff",
                    font=("Arial", 20, "bold")).pack(side="left", padx=(0, 8))
            
            title_frame = tk.Frame(logo_title_frame, bg="#00215b")
            title_frame.pack(side="left")
            
            tk.Label(title_frame, text="DESAFIO LUX", 
                    fg="#00a8ff", bg="#00215b",
                    font=("Arial", 10, "bold")).pack(anchor="w")
            
            tk.Label(title_frame, text="SISTEMA", 
                    fg="white", bg="#00215b", 
                    font=("Arial", 14, "bold")).pack(anchor="w")
                    
        elif header_width < 1200:  # Telas médias
            for widget in left_section.winfo_children():
                widget.destroy()
            
            medium_container = tk.Frame(left_section, bg="#00215b")
            medium_container.pack(anchor="w")
            
            logo_container = tk.Frame(medium_container, bg="#00215b")
            logo_container.pack(side="left", padx=(0, 15))
            
            tk.Label(logo_container, text="⚡", bg="#00215b", fg="#00a8ff",
                    font=("Arial", 22, "bold")).pack(side="left", padx=(0, 10))
            
            text_container = tk.Frame(logo_container, bg="#00215b")
            text_container.pack(side="left")
            
            tk.Label(text_container, text="DESAFIO LUX", 
                    fg="#00a8ff", bg="#00215b",
                    font=("Arial", 10, "bold")).pack(anchor="w")
            
            tk.Label(text_container, text="SISTEMA GERENCIADOR", 
                    fg="white", bg="#00215b", 
                    font=("Arial", 16, "bold")).pack(anchor="w")
                    
        else:  # Telas grandes
            for widget in left_section.winfo_children():
                widget.destroy()
            
            large_container = tk.Frame(left_section, bg="#00215b")
            large_container.pack(anchor="w")
            
            logo_container = tk.Frame(large_container, bg="#00215b")
            logo_container.pack(side="left", padx=(0, 20))
            
            tk.Label(logo_container, text="⚡", bg="#00215b", fg="#00a8ff",
                    font=("Arial", 24, "bold")).pack(side="left", padx=(0, 15))
            
            text_container = tk.Frame(logo_container, bg="#00215b")
            text_container.pack(side="left")
            
            tk.Label(text_container, text="DESAFIO LUX", 
                    fg="#00a8ff", bg="#00215b",
                    font=("Arial", 11, "bold")).pack(anchor="w")
            
            tk.Label(text_container, text="SISTEMA DE GERENCIAMENTO DE CONTATOS", 
                    fg="white", bg="#00215b", 
                    font=("Arial", 18, "bold")).pack(anchor="w", pady=(2, 0))
    

    # === LADO DIREITO - USUÁRIO (Responsivo) ===
    right_section = tk.Frame(header_content, bg="#00215b")
    right_section.grid(row=0, column=2, sticky="e")
    
    def update_right_section():
        header_width = header_content.winfo_width()
        
        for widget in right_section.winfo_children():
            widget.destroy()
        
        if header_width < 600:  # Layout muito compacto
            compact_user = tk.Frame(right_section, bg="#00308b", padx=8, pady=6)
            compact_user.pack()
            
            tk.Label(compact_user, text="👤", bg="#00308b", fg="white",
                    font=("Arial", 12)).pack()
            
            status_indicator = tk.Frame(compact_user, bg="#00ff88", width=6, height=6)
            status_indicator.pack(pady=(2, 0))
            status_indicator.pack_propagate(False)
            
        elif header_width < 900:  # Layout compacto
            compact_user = tk.Frame(right_section, bg="#00308b", padx=10, pady=6)
            compact_user.pack()
            
            user_icon_frame = tk.Frame(compact_user, bg="#00308b")
            user_icon_frame.pack(side="left", padx=(0, 8))
            
            tk.Label(user_icon_frame, text="👤", bg="#00308b", fg="white",
                    font=("Arial", 12)).pack()
            
            user_info_frame = tk.Frame(compact_user, bg="#00308b")
            user_info_frame.pack(side="left")
            
            tk.Label(user_info_frame, text="A. FREITAS", 
                    fg="white", bg="#00308b",
                    font=("Arial", 10, "bold")).pack()
            
            status_frame = tk.Frame(user_info_frame, bg="#00308b")
            status_frame.pack()
            
            status_indicator = tk.Frame(status_frame, bg="#00ff88", width=6, height=6)
            status_indicator.pack(side="left", padx=(0, 3))
            status_indicator.pack_propagate(False)
            
            tk.Label(status_frame, text="●", 
                    fg="#00ff88", bg="#00308b",
                    font=("Arial", 8)).pack(side="left")
                    
        else:  # Layout completo
            full_user = tk.Frame(right_section, bg="#00308b", padx=15, pady=8)
            full_user.pack()
            
            user_icon_frame = tk.Frame(full_user, bg="#00308b")
            user_icon_frame.pack(side="left", padx=(0, 10))
            
            tk.Label(user_icon_frame, text="👤", bg="#00308b", fg="white",
                    font=("Arial", 14)).pack()
            
            user_info_frame = tk.Frame(full_user, bg="#00308b")
            user_info_frame.pack(side="left")
            
            tk.Label(user_info_frame, text="REALIZADOR", 
                    fg="#a0d2ff", bg="#00308b",
                    font=("Arial", 8, "bold")).pack(anchor="e")
            
            tk.Label(user_info_frame, text="AMANDA DE FREITAS", 
                    fg="white", bg="#00308b",
                    font=("Arial", 11, "bold")).pack(anchor="e", pady=(2, 0))
            
            status_frame = tk.Frame(user_info_frame, bg="#00308b")
            status_frame.pack(anchor="e", pady=(5, 0))
            
            status_indicator = tk.Frame(status_frame, bg="#00ff88", width=8, height=8)
            status_indicator.pack(side="left", padx=(0, 5))
            status_indicator.pack_propagate(False)
            
            tk.Label(status_frame, text="Online", 
                    fg="#00ff88", bg="#00308b",
                    font=("Arial", 8, "bold")).pack(side="left")
    
    # Função para atualizar todo o header
    def update_header():
        update_left_section()
        update_right_section()
    
    # Atualização inicial
    header_content.update_idletasks()
    update_header()
    
    # Bind para redimensionamento
    def on_configure(event):
        update_header()
    
    header_content.bind("<Configure>", on_configure)
    
    return header