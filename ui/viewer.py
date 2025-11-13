# ui/viewer.py

import customtkinter as ctk
from ui.components.tree_viewer import build_json_tree


class ResponseRaw(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.textbox = ctk.CTkTextbox(self, wrap="word")
        self.textbox.pack(fill="both", expand=True, padx=8, pady=8)

    def update_text(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", text)

    def get_text(self):
        return self.textbox.get("1.0", "end")


class ResponseTree(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        try:
            self.tree = ctk.CTkTreeview(self)
        except:
            from tkinter import ttk
            self.tree = ttk.Treeview(self)

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def load_json(self, data):
        self.clear()
        build_json_tree(self.tree, "", data)

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
