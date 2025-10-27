from tkinter import ttk

def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background="white", foreground="#333",
                    rowheight=25, fieldbackground="white", font=('Arial', 10))
    style.configure("Treeview.Heading", background="#00215b", foreground="white",
                    relief="flat", font=('Arial', 11, 'bold'))
    style.map("Treeview.Heading", background=[('active', '#00308b')])
