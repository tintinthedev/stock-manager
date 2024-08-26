import customtkinter as ctk
from tkinter import ttk


class ClientsSpreadsheetWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.attributes("-topmost", True)

        self.create_widgets()

    def create_widgets(self):
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by client name")
        self.search_entry.pack(pady=10, padx=20, fill="x")

        self.search_button = ctk.CTkButton(self, text="Search")
        self.search_button.pack(pady=5, padx=20)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=20, fill="both", expand=True)

        self.create_table()

        # Add/Edit client info form
        self.client_name_entry = ctk.CTkEntry(self, placeholder_text="Client Name")
        self.client_name_entry.pack(pady=5, padx=20, fill="x")

        self.client_debt_entry = ctk.CTkEntry(self, placeholder_text="Client Debt")
        self.client_debt_entry.pack(pady=5, padx=20, fill="x")

        self.add_client_button = ctk.CTkButton(
            self, text="Add Client", command=self.add_client
        )
        self.add_client_button.pack(pady=10, padx=20)

    def create_table(self):
        self.table = ttk.Treeview(
            self.table_frame,
            columns=(
                "Nome",
                "Dívida",
                "Parcelas totais",
                "Parcelas efetivadas",
                "Parcelas em aberto",
                "Data da próxima parcela",
            ),
            show="headings",
        )
        self.table.pack(fill="both", expand=True)

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)

    def add_client(self):
        # Add client info to the table
        name = self.client_name_entry.get()
        debt = self.client_debt_entry.get()
        # Dummy data for illustration; you would use actual data
        self.table.insert("", "end", values=(name, debt, "0", "0", "None", "None"))
