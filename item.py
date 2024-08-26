import customtkinter as ctk
from database import Database
from bson.objectid import ObjectId
from PIL import Image, ImageTk


class Item(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        name: str,
        quantity: int,
        image: str,
        item_id: ObjectId,
        refresh_items_callback,
    ):
        """The refresh_items_callback is a function at the main window designed
        to refresh the main UI whenever items are deleted or created"""

        super().__init__(parent, fg_color="#222222")

        self.item_name = name
        self.quantity = quantity
        self.item_id = item_id
        self.item_image_path = image

        self.refresh_items_callback = refresh_items_callback

        self.default_buttons_font = ("", 22)
        self.default_button_styles = {
            "fg_color": "#777777",
            "hover_color": "#444444",
        }

        self.tkinter_item_image = None

        # item layout
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")

        self.create_widgets()
        self.display_widgets()

        self.display_item_image()

    def create_widgets(self):
        self.item_image_canvas = ctk.CTkCanvas(
            self,
            width=100,
            height=100,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.item_name_label = ctk.CTkLabel(self, text=self.item_name)

        self.quantity_label = ctk.CTkLabel(self, text=f"Quantidade: {self.quantity}")

        self.buttons_frame = ctk.CTkFrame(self)

        self.increase_quantity_btn = ctk.CTkButton(
            self.buttons_frame,
            **self.default_button_styles,
            text="+",
            width=40,
            command=lambda: self.change_quantity("increase"),
            text_color="#45ffa8",
            font=("", 22)
        )

        self.decrease_quantity_btn = ctk.CTkButton(
            self.buttons_frame,
            **self.default_button_styles,
            text="-",
            width=40,
            command=lambda: self.change_quantity("decrease"),
            text_color="#fc5861",
            font=("", 22)
        )

        self.delete_item_btn = ctk.CTkButton(
            self.buttons_frame,
            text="X",
            text_color="#ff5511",
            width=40,
            **self.default_button_styles,
            command=self.delete_item,
        )

    def display_widgets(self):
        self.item_image_canvas.grid(column=0, columnspan=2, row=0, rowspan=3)
        self.item_name_label.grid(column=2, row=0, columnspan=2)
        self.quantity_label.grid(column=2, row=1, columnspan=2)

        self.buttons_frame.grid(column=2, columnspan=3, row=2)

        self.increase_quantity_btn.pack(side="left", padx=(4, 0))
        self.decrease_quantity_btn.pack(side="left", padx=5)
        self.delete_item_btn.pack(side="left")

    def display_item_image(self):
        item_image = Image.open(self.item_image_path)

        item_image = item_image.resize((100, 100))

        self.tkinter_item_image = ImageTk.PhotoImage(item_image)

        self.item_image_canvas.create_image(
            0,
            0,
            image=self.tkinter_item_image,
            anchor="nw",
        )

    def delete_item(self):
        Database().delete_item(self.item_id)

        self.refresh_items_callback()

    def change_quantity(self, change_type: str):
        if change_type == "increase":
            self.quantity += 1

            edited_item = {"$set": {"quantity": self.quantity}}

            Database().edit_item(self.item_id, edited_item)

            self.quantity_label.configure(text=f"Quantidade: {self.quantity}")
        else:
            if self.quantity > 0:
                self.quantity -= 1

                edited_item = {"$set": {"quantity": self.quantity}}

                Database().edit_item(self.item_id, edited_item)

                self.quantity_label.configure(text=f"Quantidade: {self.quantity}")
