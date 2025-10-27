# main.py
from ui.screens.token_screen import TokenScreen
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenScreen(root)
    root.mainloop()
