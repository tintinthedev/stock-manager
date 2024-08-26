from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
import bson.binary
from typing import TypedDict
import datetime


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
    installments_left_to_pay: int


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
        next_installment_payment_date: datetime.date,
    ):

        self.clients_database.insert_one(
            {
                "name": name,
                "debt": debt,
                "total_installments": total_installments,
                "individual_installment_value": individual_installment_value,
                "next_installment_payment_date": next_installment_payment_date,
                "paid_installments": 0,
                "installments_left_to_pay": total_installments,
            }
        )

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
