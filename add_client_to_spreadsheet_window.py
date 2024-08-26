import customtkinter as ctk
from database import Database


class AddClientToSpreadsheetWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Adicionar novo cliente")
        self.geometry("500x500")

        self.attributes("-topmost", True)

        self.client_name = ctk.StringVar()
        self.client_debt = ctk.DoubleVar()
        self.client_installment_value = ctk.DoubleVar()
        self.client_total_installments_amount = ctk.IntVar()
        self.client_next_installment_date = ctk.StringVar()

        self.create_widgets()
        self.display_widgets()

    def create_widgets(self):
        self.client_name_entry_placehodler = ctk.CTkLabel(self, text="Nome do cliente")
        self.client_name_entry = ctk.CTkEntry(self, textvariable=self.client_name)

        self.client_debt_entry_placeholder = ctk.CTkLabel(
            self, text="Dívida do cliente"
        )
        self.client_debt_entry = ctk.CTkEntry(self, textvariable=self.client_debt)

        self.client_installment_value_placeholder = ctk.CTkLabel(
            self, text="Valor de cada parcela"
        )
        self.client_installment_value_entry = ctk.CTkEntry(
            self, textvariable=self.client_installment_value
        )

        self.client_total_installments_amount_placeholder = ctk.CTkLabel(
            self, text="Quantidade de parcelas"
        )
        self.client_total_installments_amount_entry = ctk.CTkEntry(
            self, textvariable=self.client_total_installments_amount
        )

        self.client_next_installment_date_placeholder = ctk.CTkLabel(
            self, text="Data da proxima parcela"
        )
        self.client_next_installment_date_entry = ctk.CTkEntry(
            self, textvariable=self.client_next_installment_date
        )

        self.add_client_to_spreadsheet_button = ctk.CTkButton(
            self, text="Adicionar cliente", command=self.add_client_to_spreadsheet
        )

    def display_widgets(self):
        self.client_name_entry_placehodler.pack()
        self.client_name_entry.pack()

        self.client_debt_entry_placeholder.pack()
        self.client_debt_entry.pack()

        self.client_installment_value_placeholder.pack()
        self.client_installment_value_entry.pack()

        self.client_total_installments_amount_placeholder.pack()
        self.client_total_installments_amount_entry.pack()

        self.client_next_installment_date_placeholder.pack()
        self.client_next_installment_date_entry.pack()

        self.add_client_to_spreadsheet_button.pack(pady=20)

    def add_client_to_spreadsheet(self):
        client_name = self.client_name.get()
        client_debt = self.client_debt.get()
        client_total_installments_amount = self.client_total_installments_amount.get()
        client_installment_value = self.client_installment_value.get()
        client_next_installment_date = self.client_next_installment_date.get()

        Database().create_client(
            client_name,
            client_debt,
            client_total_installments_amount,
            client_installment_value,
            client_next_installment_date,
        )

        self.destroy()
