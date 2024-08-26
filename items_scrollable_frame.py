import customtkinter as ctk

from item import Item


class ItemsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.items_count = 0
        self.item_relx = 0
        self.item_rely = 0

        self.columns_quantity = 4
        self.current_item_row = 0
        self.current_item_column = 0

        self.bind_mouse_scroll()

    def configure_grid(self):
        """Reconfigures the frame grid based on the amount of items on it"""

        rows_quantity = int(self.items_count / self.columns_quantity) + 1

        for i in range(self.columns_quantity):
            self.columnconfigure(i, weight=1, uniform="a")

        for i in range(rows_quantity):
            self.rowconfigure(i, weight=1, uniform="a")

    def add_item(self, item: Item):
        self.items_count += 1
        self.configure_grid()

        if self.items_count % 4 != 0:
            item.grid(
                column=self.current_item_column,
                row=self.current_item_row,
                pady=10,
                padx=10,
            )

            self.current_item_column += 1
        else:
            item.grid(
                column=self.current_item_column,
                row=self.current_item_row,
                pady=10,
                padx=10,
            )
            self.current_item_column = 0
            self.current_item_row += 1

    def bind_mouse_scroll(self):
        """Bind mouse scroll event to the frame"""
        self.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.bind_all("<Button-4>", self._on_mouse_wheel)  # For Linux
        self.bind_all("<Button-5>", self._on_mouse_wheel)  # For Linux

    def _on_mouse_wheel(self, event):
        """Scroll the frame using the mouse wheel"""
        if event.num == 4 or event.delta > 0:
            self._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self._parent_canvas.yview_scroll(1, "units")
