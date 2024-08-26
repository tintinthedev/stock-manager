import os.path
import customtkinter as ctk
from database import Database
from insert_item_window import InsertItemWindow
from item import Item
from items_scrollable_frame import ItemsScrollableFrame
import random
import string
import globals


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.width = 1050
        self.height = 600

        self.geometry(self.get_centralized_geometry())
        self.minsize(1050, 600)
        self.title("Gerenciador de estoque")

        self.create_widgets()
        self.display_widgets()

        self.refresh_items()

        self.protocol("WM_DELETE_WINDOW", self.on_close_callback)

        self.mainloop()

    def get_centralized_geometry(self) -> str:
        screen_x_center = int(self.winfo_screenwidth() / 2)
        screen_y_center = int(self.winfo_screenheight() / 2)

        app_x_center = int(screen_x_center - (self.width / 2))
        app_y_center = int(screen_y_center - (self.height / 2))

        return f"{self.width}x{self.height}+{app_x_center}+{app_y_center}"

    def create_widgets(self):
        self.add_new_item_button = ctk.CTkButton(
            self,
            text="Adicionar novo item",
            command=lambda: InsertItemWindow(self.refresh_items),
        )

    def display_widgets(self):
        self.add_new_item_button.place(relx=0.98, rely=0.01, anchor="ne")

    def on_close_callback(self):
        try:
            item_images = os.listdir(globals.item_images_folder)

            for image in item_images:
                image_path = os.path.join(globals.item_images_folder, image)

                os.remove(image_path)

        except OSError:
            print("Error while deleting item images")

        self.destroy()

    def refresh_items(self):
        for widget in self.winfo_children():
            widget.destroy()

        if (
            Database().database_items.count_documents({}) == 0
        ):  # items database is empty
            self.no_items_warn_label = ctk.CTkLabel(
                self, text="Nenhum item encontrado.", font=("", 25)
            )
            self.add_items_button = ctk.CTkButton(
                self,
                text="Adicionar item",
                command=lambda: InsertItemWindow(self.refresh_items),
            )

            self.no_items_warn_label.pack(pady=20)
            self.add_items_button.pack()

        else:
            # creating the "add new item" button
            self.create_widgets()
            self.display_widgets()

            # displaying database items
            database_items = Database().get_items()

            items_scrollable_frame = ItemsScrollableFrame(self)
            items_scrollable_frame.pack(expand=True, fill="both", pady=50)

            for item in database_items:
                item_name = item["name"]
                item_quantity = item["quantity"]
                item_id = item["_id"]
                item_image = item["image"]

                # random name for the item image
                image_file_name = f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}.jpg"

                if not os.path.exists(globals.item_images_folder):
                    os.makedirs(globals.item_images_folder)

                with open(f"{globals.item_images_folder}/{image_file_name}", "wb") as f:
                    f.write(item_image)

                item = Item(
                    items_scrollable_frame,
                    name=item_name,
                    quantity=item_quantity,
                    image=f"{globals.item_images_folder}/{image_file_name}",
                    item_id=item_id,
                    refresh_items_callback=self.refresh_items,
                )

                items_scrollable_frame.add_item(item)


App()
