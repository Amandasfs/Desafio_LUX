# ui/screens/token_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from .dashboard_window import DashboardWindow

class TokenScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Acesso - Gerenciamento de Contatos")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        
        # Centralizar a janela
        self.root.eval('tk::PlaceWindow . center')
        
        # Criar canvas para o gradiente
        self.canvas = tk.Canvas(root, width=350, height=250, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Criar gradiente azul
        self.create_gradient()
        
        # Frame principal com fundo transparente
        main_frame = tk.Frame(self.canvas, bg='#00215b', padx=30, pady=30)
        self.canvas.create_window(175, 125, window=main_frame)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Acesso ao Sistema", 
            bg='#00215b',
            fg="white", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame, 
            text="Insira seu token de acesso", 
            bg='#00215b',
            fg="white", 
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Frame do campo de entrada
        entry_frame = tk.Frame(main_frame, bg='#00215b')
        entry_frame.pack(fill="x", pady=10)
        
        # Campo de token
        self.token_entry = tk.Entry(
            entry_frame, 
            show="•", 
            font=("Arial", 11),
            width=25,
            bg="white",
            relief="flat",
            justify="center"
        )
        self.token_entry.pack(pady=5, ipady=8)
        
        # Botão de login BRANCO
        self.login_button = tk.Button(
            main_frame,
            text="Entrar",
            command=self.validar_token,
            bg="#FFFFFF",
            fg="#00215b",
            font=("Arial", 10, "bold"),
            width=15,
            height=1,
            border=0,
            relief="flat",
            cursor="hand2",
            activebackground="#f0f0f0",
            activeforeground="#00215b"
        )
        self.login_button.pack(pady=20)
        
        # Texto de ajuda
        help_label = tk.Label(
            main_frame,
            text="Digite o token fornecido para acessar o sistema.",
            bg='#00215b',
            fg="white",
            font=("Arial", 8)
        )
        help_label.pack()
        
        # Bind Enter key para facilitar login
        self.token_entry.bind('<Return>', lambda e: self.validar_token())
        
        # Focar no campo de entrada
        self.token_entry.focus()

    def create_gradient(self):
        """Cria um gradiente azul partindo de #00215b"""
        width = 350
        height = 250
        
        # Cores do gradiente
        color1 = "#00215b"  # Azul escuro original
        color2 = "#003080"  # Azul médio
        color3 = "#0040a0"  # Azul mais claro
        
        # Criar gradiente vertical
        for i in range(height):
            # Interpolação das cores
            if i < height/2:
                # Primeira metade: color1 para color2
                ratio = i / (height/2)
                r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
                g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[3:5], 16) * ratio)
                b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
            else:
                # Segunda metade: color2 para color3
                ratio = (i - height/2) / (height/2)
                r = int(int(color2[1:3], 16) * (1 - ratio) + int(color3[1:3], 16) * ratio)
                g = int(int(color2[3:5], 16) * (1 - ratio) + int(color3[3:5], 16) * ratio)
                b = int(int(color2[5:7], 16) * (1 - ratio) + int(color3[5:7], 16) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def validar_token(self):
        token = self.token_entry.get().strip()
        if token == "1234":
            # Feedback visual de sucesso
            self.login_button.config(bg="#e8f5e8", fg="#0f9d58", text="✓ Entrando...")
            self.root.update()
            self.root.after(500, self.abrir_dashboard)
        else:
            messagebox.showerror(
                "Erro de Autenticação", 
                "Token inválido!\n\nPor favor, verifique suas credenciais e tente novamente."
            )
            # Limpar campo e focar novamente
            self.token_entry.delete(0, tk.END)
            self.token_entry.focus()

    def abrir_dashboard(self):
        self.root.destroy()
        dashboard_root = tk.Tk()
        DashboardWindow(dashboard_root)
        dashboard_root.mainloop()