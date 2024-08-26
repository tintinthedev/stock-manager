import customtkinter as ctk
from tkinter import ttk
from add_client_to_spreadsheet_window import AddClientToSpreadsheetWindow
from database import Database


class ClientsSpreadsheetWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=200)
        self.title("Planilha de clientes")

        self.attributes("-topmost", True)

        self.create_widgets()

    def create_widgets(self):
        self.search_entry = ctk.CTkEntry(
            self, placeholder_text="Procurar cliente pelo nome"
        )
        self.search_entry.pack(pady=10, padx=20, fill="x")

        self.search_button = ctk.CTkButton(self, text="Procurar por nome")
        self.search_button.pack(pady=5, padx=20)

        self.add_client_button = ctk.CTkButton(
            self, text="Adicionar cliente", command=self.add_client
        )

        self.add_client_button.pack(pady=10, padx=20)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=20, fill="both", expand=True)

        self.create_table()

        self.refresh_table()

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
        client_creation_window = AddClientToSpreadsheetWindow()
        self.wait_window(client_creation_window)

        self.refresh_table()

    def refresh_table(self):
        # clearing the table before getting data
        self.table.delete(*self.table.get_children())

        clients = Database().get_clients()

        for client in clients:
            client_name = client["name"]
            client_debt = client["debt"]
            total_client_installments = client["total_installments"]
            paid_client_installments = client["paid_installments_date"]
            client_installments_left_to_pay = client["installments_left_to_pay_dates"]
            next_client_installment_payment_date = client[
                "next_installment_payment_date"
            ]

            client_installments_left_to_pay = "\n".join(client_installments_left_to_pay)

            self.table.insert(
                "",
                "end",
                values=(
                    client_name,
                    client_debt,
                    total_client_installments,
                    paid_client_installments,
                    client_installments_left_to_pay,
                    next_client_installment_payment_date,
                ),
            )
