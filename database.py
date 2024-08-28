from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
import bson.binary
from typing import TypedDict
import datetime
import re


class Item(TypedDict):
    name: str
    quantity: int
    image: bson.binary.Binary


class Client(TypedDict):
    name: str
    debt: float
    total_installments: int
    individual_installment_value: float
    next_installment_payment_date: float
    installments_left_to_pay_date: list[str]
    paid_installments_dates: list[str]


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://randomthecoder1557:PHWXHGBz3822bh6u@tintin-cluster.cm5rl.mongodb.net/?retryWrites=true&w=majority&appName=tintin-cluster"
        )

        self.database = self.client.rita_database

        self.database_items: Collection[Item] = self.database.items

        self.clients_database: Collection[Client] = self.database.clients

    def create_client(
        self,
        name: str,
        debt: float,
        total_installments: int,
        individual_installment_value: float,
        next_installment_payment_date: str,
    ):

        next_installment_payment_date_values = next_installment_payment_date.split("/")
        next_installment_payment_day = int(next_installment_payment_date_values[0])
        next_installment_payment_month = int(next_installment_payment_date_values[1])
        next_installment_payment_year = int(next_installment_payment_date_values[2])

        next_installment_payment_date_as_date = datetime.date(
            next_installment_payment_year,
            next_installment_payment_month,
            next_installment_payment_day,
        )

        installments_left_to_pay = []

        installments_left_to_pay.append(next_installment_payment_date)

        for i in range(1, total_installments):
            next_installment_date = (
                next_installment_payment_date_as_date + datetime.timedelta(days=30 * i)
            )

            next_installment_day = next_installment_date.day
            next_installment_month = next_installment_date.month
            next_installment_year = next_installment_date.year

            next_installment_date = f"{next_installment_day}/{next_installment_month}/{next_installment_year}"

            installments_left_to_pay.append(next_installment_date)

        self.clients_database.insert_one(
            {
                "name": name,
                "debt": debt,
                "total_installments": total_installments,
                "individual_installment_value": individual_installment_value,
                "next_installment_payment_date": next_installment_payment_date,
                "paid_installments_date": [],
                "installments_left_to_pay_dates": installments_left_to_pay,
            }
        )

    def get_clients(self):
        return self.clients_database.find()

    def count_clients(self):
        return self.clients_database.count_documents({})

    def edit_client(self, client_data):
        client_id = client_data["client_id"]
        client_name = client_data["name"]
        client_debt = client_data["debt"]
        client_individual_installment_value = client_data[
            "individual_installment_value"
        ]
        client_total_installments = client_data["total_installments"]
        client_next_installment_payment_date = client_data[
            "next_installment_payment_date"
        ]
        client_installments_left_to_pay = client_data["installments_left_to_pay_dates"]
        client_paid_installments = client_data["paid_installments_date"]

        self.clients_database.update_one(
            {"_id": client_id},
            {
                "$set": {
                    "name": client_name,
                    "debt": client_debt,
                    "total_installments": client_total_installments,
                    "individual_installment_value": client_individual_installment_value,
                    "next_installment_payment_date": client_next_installment_payment_date,
                    "paid_installments_date": client_paid_installments,
                    "installments_left_to_pay_dates": client_installments_left_to_pay,
                }
            },
        )

    def delete_client(self, client_id):
        self.clients_database.delete_one({"_id": client_id})

    def get_client_by_name(self, client_name):
        escaped_client_name = re.escape(client_name)

        client_name_pattern = re.compile(escaped_client_name, re.IGNORECASE)

        found_clients = self.clients_database.find({"name": client_name_pattern})

        return found_clients

    def create_item(self, name: str, quantity: int, image_path: str):
        with open(image_path, "rb") as item_image_file:
            encoded_item_image = bson.binary.Binary(item_image_file.read())

        self.database_items.insert_one(
            {
                "name": name,
                "quantity": quantity,
                "image": encoded_item_image,
            }
        )

    def get_items(self):
        return self.database_items.find()

    def edit_item(self, item_id: ObjectId, new_item):
        self.database_items.update_one({"_id": item_id}, new_item)

    def delete_item(self, item_id: ObjectId):
        self.database_items.delete_one({"_id": item_id})
