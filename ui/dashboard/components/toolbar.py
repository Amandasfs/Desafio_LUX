import tkinter as tk

def create_toolbar(root, dashboard):
    toolbar = tk.Frame(root, bg="#00215b", height=50)
    toolbar.pack(fill="x")

    search_container = tk.Frame(toolbar, bg="#00215b")
    search_container.pack(side="left", padx=10)

    tk.Label(
        search_container,
        text="🔍",
        bg="#00215b",
        fg="white",
        font=("Arial", 12, "bold"),
    ).pack(side="left")

    search_entry = tk.Entry(search_container, width=30, font=("Arial", 11))
    search_entry.pack(side="left", padx=5, pady=10)

    def get_search_term():
        return search_entry.get().lower().strip()

    dashboard.get_search_term = get_search_term

    tk.Button(
        search_container,
        text="Buscar",
        bg="#004aad",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        command=dashboard.buscar,
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        search_container,
        text="Organizar",
        bg="#0066cc",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        command=dashboard.organizar_dados,
        cursor="hand2"
    ).pack(side="left", padx=5)

    return toolbar
