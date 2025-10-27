# ui/dashboard/components/cards.py
import tkinter as tk
import os
import time
from threading import Thread
from services.parser_excel import carregar_dados_excel

class CardsSection:
    def __init__(self, parent, excel_path="./dados_brutos.xlsx"):
        self.parent = parent
        self.excel_path = excel_path
        self.last_modified = None

        # Frame principal
        self.frame = tk.Frame(parent, bg="#ffffff")
        self.frame.pack(fill="x", pady=(0, 10))

        # Cria os cards e guarda referência das labels
        self.cards = {}
        self.create_cards()

        # Atualiza uma vez no início
        self.update_cards()

        # Inicia monitoramento em segundo plano
        Thread(target=self.watch_excel_changes, daemon=True).start()

    # === Criação dos cards ===
    def create_cards(self):
        """Define os cards visuais"""
        cards_info = [
            ("🏢 Total de Empresas", "empresas", "#004aad"),
            ("👥 Total de Contatos", "clientes", "#007bff"),
        ]

        for titulo, key, color in cards_info:
            card = tk.Frame(self.frame, bg="#f1f5f9", width=250, height=100,
                            highlightthickness=1, highlightbackground="#d0d7de")
            card.pack(side="left", padx=10)
            card.pack_propagate(False)

            tk.Label(card, text=titulo, bg="#f1f5f9", fg="#333",
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

            valor_label = tk.Label(card, text="Carregando...", bg="#f1f5f9", fg=color,
                                   font=("Arial", 16, "bold"))
            valor_label.pack(anchor="w", padx=10, pady=(5, 0))

            self.cards[key] = valor_label

    # === Atualiza dados dos cards ===
    def update_cards(self):
        """Atualiza os valores com base no Excel"""
        try:
            clientes, empresas, _ = carregar_dados_excel(self.excel_path)

            num_empresas = len(empresas)
            num_clientes = len(clientes)

            # Atualiza valores no front
            self.cards["empresas"].config(text=str(num_empresas))
            self.cards["clientes"].config(text=str(num_clientes))

            print(f"🔁 Cards atualizados — Empresas: {num_empresas}, Contatos: {num_clientes}")

        except Exception as e:
            print(f"❌ Erro ao atualizar cards: {e}")

    # === Observa alterações no arquivo Excel ===
    def watch_excel_changes(self):
        """Monitora mudanças no arquivo Excel e atualiza automaticamente"""
        while True:
            try:
                if not os.path.exists(self.excel_path):
                    time.sleep(5)
                    continue

                mod_time = os.path.getmtime(self.excel_path)
                if self.last_modified is None:
                    self.last_modified = mod_time
                elif mod_time != self.last_modified:
                    self.last_modified = mod_time
                    print("📊 Planilha alterada — atualizando cards...")
                    self.parent.after(100, self.update_cards)

            except Exception as e:
                print(f"⚠️ Erro ao monitorar Excel: {e}")

            time.sleep(3)  # checa a cada 3 segundos


def create_cards(parent):
    """Função usada pelo dashboard para criar os cards dinamicamente"""
    return CardsSection(parent).frame
