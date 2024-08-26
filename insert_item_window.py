import customtkinter as ctk
from database import Database


class InsertItemWindow(ctk.CTkToplevel):
    def __init__(self, refresh_items_callback):
        """The refresh_items_callback is a function at the main window designed
        to refresh the main UI whenever items are deleted or created"""

        super().__init__()

        self.attributes("-topmost", True)

        self.width = 500
        self.height = 500

        self.title("Inserir novo item")
        self.geometry(self.get_centralized_geometry())

        self.item_name = ctk.StringVar()
        self.item_quantity = ctk.StringVar()
        self.item_image_path = ctk.StringVar()

        self.refresh_items_callback = refresh_items_callback

        self.create_widgets()
        self.display_widgets()

        self.mainloop()

    def get_centralized_geometry(self) -> str:
        screen_x_center = int(self.winfo_screenwidth() / 2)
        screen_y_center = int(self.winfo_screenheight() / 2)

        app_x_center = int(screen_x_center - (self.width / 2))
        app_y_center = int(screen_y_center - (self.height / 2))

        return f"{self.width}x{self.height}+{app_x_center}+{app_y_center}"

    def create_widgets(self):
        self.item_name_placeholder = ctk.CTkLabel(self, text="Nome do item")
        self.item_name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nome do item",
            width=200,
            textvariable=self.item_name,
        )

        self.item_quantity_placeholder = ctk.CTkLabel(self, text="Quantidade")
        self.item_quantity_entry = ctk.CTkEntry(
            self,
            placeholder_text="Quantidade",
            width=200,
            textvariable=self.item_quantity,
        )

        self.select_item_image_button = ctk.CTkButton(
            self, text="Selecionar imagem", command=self.select_item_image
        )

        self.create_item_button = ctk.CTkButton(
            self, text="Adicionar item", command=self.create_new_item
        )

    def display_widgets(self):
        self.item_name_placeholder.pack()
        self.item_name_entry.pack(pady=(0, 10))
        self.item_quantity_placeholder.pack()
        self.item_quantity_entry.pack()
        self.select_item_image_button.pack(pady=10)
        self.create_item_button.pack(pady=20)

    def select_item_image(self):
        image_path = ctk.filedialog.askopenfilename()

        if len(image_path) == 0:  # no file was selected
            return

        self.item_image_path.set(image_path)

    def create_new_item(self):
        item_name = self.item_name.get()
        item_quantity = int(self.item_quantity.get())
        item_image = self.item_image_path.get()

        Database().create_item(item_name, item_quantity, item_image)

        self.refresh_items_callback()

        self.destroy()
