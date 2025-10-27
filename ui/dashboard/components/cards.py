# ui/dashboard/components/cards.py
import tkinter as tk

def create_cards(parent):
    frame = tk.Frame(parent, bg="#ffffff")
    frame.pack(fill="x", pady=(0, 10))

    cards_data = [
        ("👥 Clientes", "128"),
        ("🏢 Empresas", "45"),
        ("📈 Consumo Médio", "3.240 kWh")
    ]

    for titulo, valor in cards_data:
        card = tk.Frame(frame, bg="#f1f5f9", width=250, height=100, highlightthickness=1,
                        highlightbackground="#d0d7de")
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

        tk.Label(card, text=titulo, bg="#f1f5f9", fg="#333",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Label(card, text=valor, bg="#f1f5f9", fg="#00215b",
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    return frame
