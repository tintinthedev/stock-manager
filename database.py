from pymongo import MongoClient
from bson.objectid import ObjectId
import bson.binary


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://randomthecoder1557:PHWXHGBz3822bh6u@tintin-cluster.cm5rl.mongodb.net/?retryWrites=true&w=majority&appName=tintin-cluster"
        )

        self.database = self.client.rita_database

        self.database_items = self.database.items

    def create_item(self, name: str, quantity: int, image_path: str):
        with open(image_path, "rb") as item_image_file:
            encoded_item_image = bson.binary.Binary(item_image_file.read())

        self.database_items.insert_one({
            "name": name,
            "quantity": quantity,
            "image": encoded_item_image,
        })

    def get_items(self):
        return self.database_items.find()

    def edit_item(self, item_id: ObjectId, new_item):
        self.database_items.update_one({"_id": item_id}, new_item)

    def delete_item(self, item_id: ObjectId):
        self.database_items.delete_one({"_id": item_id})
