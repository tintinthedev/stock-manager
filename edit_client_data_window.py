import customtkinter as ctk
from database import Database


class EditClientDataWindow(ctk.CTkToplevel):
    def __init__(self, client_data):
        super().__init__()

        self.attributes("-topmost", True)
        self.geometry("500x750")

        self.title("Editar informações do cliente")

        self.client_data = client_data

        self.client_name = ctk.StringVar(value=self.client_data[0])
        self.client_debt = ctk.DoubleVar(value=self.client_data[1])
        self.client_installment_value = ctk.DoubleVar(value=self.client_data[2])
        self.client_total_installments_amount = ctk.IntVar(value=self.client_data[3])
        self.client_paid_installments = ctk.StringVar(value=self.client_data[4])
        self.client_installments_left_to_pay = ctk.StringVar(value=self.client_data[5])
        self.client_next_installment_date = ctk.StringVar(value=self.client_data[6])
        self.client_id = self.client_data[7]

        self.create_widgets()
        self.display_widgets()

    def create_widgets(self):
        self.client_name_entry_placehodler = ctk.CTkLabel(self, text="Nome do cliente")
        self.client_name_entry = ctk.CTkEntry(
            self, textvariable=self.client_name, width=250
        )

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

        self.client_paid_installments_placeholder = ctk.CTkLabel(
            self, text="Parcelas pagas"
        )
        self.client_paid_installments_dates_textbox = ctk.CTkTextbox(self, height=110)
        self.client_paid_installments_dates_textbox.insert(
            "end", self.client_paid_installments.get()
        )

        self.client_installments_left_to_pay_placeholder = ctk.CTkLabel(
            self, text="Parcelas em aberto"
        )
        self.client_installments_left_to_pay_textbox = ctk.CTkTextbox(self, height=110)
        self.client_installments_left_to_pay_textbox.insert(
            "end", self.client_installments_left_to_pay.get()
        )

        self.client_next_installment_date_placeholder = ctk.CTkLabel(
            self, text="Data da proxima parcela"
        )
        self.client_next_installment_date_entry = ctk.CTkEntry(
            self, textvariable=self.client_next_installment_date
        )

        self.save_client_data_button = ctk.CTkButton(
            self, text="Salvar alterações", command=self.save_client_data_to_database
        )

        self.delete_client_button = ctk.CTkButton(
            self,
            text="Deletar dados do cliente",
            command=self.delete_client,
            fg_color="#aa4433",
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

        self.client_paid_installments_placeholder.pack()
        self.client_paid_installments_dates_textbox.pack()

        self.client_installments_left_to_pay_placeholder.pack()
        self.client_installments_left_to_pay_textbox.pack()

        self.client_next_installment_date_placeholder.pack()
        self.client_next_installment_date_entry.pack()

        self.save_client_data_button.pack(pady=20)

        self.delete_client_button.pack()

    def save_client_data_to_database(self):
        client_name = self.client_name.get()
        client_debt = self.client_debt.get()
        client_individual_installment_value = self.client_installment_value.get()
        client_total_installments_amount = self.client_total_installments_amount.get()
        client_paid_installments = self.client_paid_installments_dates_textbox.get(
            "1.0", ctk.END
        )
        client_installments_left_to_pay = (
            self.client_installments_left_to_pay_textbox.get("1.0", ctk.END)
        )
        client_next_installment_payment_date = self.client_next_installment_date.get()

        # formatting the dates to an array of dates
        client_installments_left_to_pay = client_installments_left_to_pay.split("\n")
        client_paid_installments = client_paid_installments.split("\n")

        client_data = {
            "name": client_name,
            "debt": client_debt,
            "individual_installment_value": client_individual_installment_value,
            "total_installments": client_total_installments_amount,
            "installments_left_to_pay_dates": client_installments_left_to_pay,
            "paid_installments_date": client_paid_installments,
            "next_installment_payment_date": client_next_installment_payment_date,
            "client_id": self.client_id,
        }

        Database().edit_client(client_data)

        self.destroy()

    def delete_client(self):
        Database().delete_client(self.client_id)

        self.destroy()
