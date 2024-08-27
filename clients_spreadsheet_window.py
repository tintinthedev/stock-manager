import customtkinter as ctk
from tkinter import ttk
from add_client_to_spreadsheet_window import AddClientToSpreadsheetWindow
from database import Database
from CTkTable import *


class ClientsSpreadsheetWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

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

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(expand=True, fill="both")
        self.create_table()

    def create_table(self):
        table_rows = (
            Database().count_clients() + 1
        )  # adding one because of the table head

        # these first values are the table head
        table_values = [
            [
                "NOME",
                "DÍVIDA",
                "PARCELAS TOTAIS",
                "PARCELAS EFETIVADAS",
                "PARCELAS EM ABERTO",
                "PRÓXIMA PARCELA",
            ],
        ]

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

            paid_client_installments = "\n".join(paid_client_installments)
            client_installments_left_to_pay = "\n".join(client_installments_left_to_pay)

            client_table_row = [
                client_name,
                client_debt,
                total_client_installments,
                paid_client_installments,
                client_installments_left_to_pay,
                next_client_installment_payment_date,
            ]

            table_values.append(client_table_row)

        # clearing possible old data from table by deleting the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.table = CTkTable(
            self.table_frame, column=6, row=table_rows, values=table_values
        )

        self.table.pack(expand=True, fill="both")

    def add_client(self):
        client_creation_window = AddClientToSpreadsheetWindow()
        self.wait_window(client_creation_window)  # waiting for the window to close

        self.create_table()
