import customtkinter as ctk
from add_client_to_spreadsheet_window import AddClientToSpreadsheetWindow
from database import Database
from CTkTable import *
from edit_client_data_window import EditClientDataWindow


class ClientsSpreadsheetWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("900x500")
        self.attributes("-topmost", True)

        self.title("Planilha de clientes")

        self.attributes("-topmost", True)

        self.client_name = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.search_client_by_name_placeholder = ctk.CTkLabel(
            self, text="Procurar cliente pelo nome"
        )
        self.search_client_by_name_placeholder.pack()

        self.search_entry = ctk.CTkEntry(self, textvariable=self.client_name)
        self.search_entry.pack(padx=20, fill="x")

        self.search_client_by_name_button = ctk.CTkButton(
            self,
            text="Procurar por nome",
            command=lambda: self.search_client_by_name(self.client_name.get()),
        )
        self.search_client_by_name_button.pack(pady=5, padx=20)

        self.add_client_button = ctk.CTkButton(
            self, text="Adicionar cliente", command=self.add_client
        )

        self.add_client_button.pack(pady=10, padx=20)

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(expand=True, fill="both")
        self.create_table()

    def format_clients_data_row_to_table(self, clients):
        formatted_client_rows = []

        for client in clients:
            client_name = client["name"]
            client_debt = client["debt"]
            individual_installment_value = client["individual_installment_value"]
            total_client_installments = client["total_installments"]
            paid_client_installments = client["paid_installments_date"]
            client_installments_left_to_pay = client["installments_left_to_pay_dates"]
            next_client_installment_payment_date = client[
                "next_installment_payment_date"
            ]
            client_id = client["_id"]

            paid_client_installments = "\n".join(paid_client_installments)
            client_installments_left_to_pay = "\n".join(client_installments_left_to_pay)

            client_table_row = [
                client_name,
                client_debt,
                individual_installment_value,
                total_client_installments,
                paid_client_installments,
                client_installments_left_to_pay,
                next_client_installment_payment_date,
                client_id,
            ]

            formatted_client_rows.append(client_table_row)

        return formatted_client_rows

    def create_table(self, clients=None):
        table_rows = (
            Database().count_clients() + 1 if clients is None else len(clients) + 1
        )  # adding one because of the table head

        # these first values are the table head
        table_values = [
            [
                "NOME",
                "DÍVIDA",
                "VALOR DE CADA PARCELA",
                "PARCELAS TOTAIS",
                "PARCELAS EFETIVADAS",
                "PARCELAS EM ABERTO",
                "PRÓXIMA PARCELA",
                "ID",
            ],
        ]

        # if there are clients passed as a parameter, only show their data
        # otherwise, show data of every client
        if clients is not None:
            formatted_table_rows = self.format_clients_data_row_to_table(clients)

            for table_row in formatted_table_rows:
                table_values.append(table_row)
        else:
            clients = Database().get_clients()

            formatted_table_rows = self.format_clients_data_row_to_table(clients)

            for table_row in formatted_table_rows:
                table_values.append(table_row)

        # clearing possible old data from table by deleting the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.table = CTkTable(
            self.table_frame,
            column=len(table_values[0]),
            row=table_rows,
            values=table_values,
            command=lambda table_click_data: self.edit_client(table_click_data),
        )

        self.table.pack(expand=True, fill="both", pady=20)

    def add_client(self):
        client_creation_window = AddClientToSpreadsheetWindow()
        self.wait_window(client_creation_window)  # waiting for the window to close

        self.create_table()

    def edit_client(self, table_click_data):
        clicked_row = table_click_data["row"]

        clicked_row_data = self.table.get_row(clicked_row)

        edit_client_data_window = EditClientDataWindow(client_data=clicked_row_data)

        self.wait_window(edit_client_data_window)

        # re-creating the table to show updated data
        self.create_table()

    def search_client_by_name(self, client_name):
        # if no name is provided, just bring all clients to the table
        if client_name == "":
            self.create_table()
            return

        found_clients = Database().get_client_by_name(client_name)

        all_clients = []

        for client in found_clients:
            all_clients.append(client)

        self.create_table(all_clients)
