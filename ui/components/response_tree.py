# ui/components/response_tree.py
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from ui.components.tree_viewer import build_json_tree

class ResponseTree(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(side="left", fill="both", expand=True)
        self.scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scroll.set)

    def populate(self, data):
        # clear
        for i in self.tree.get_children():
            self.tree.delete(i)
        if data is None:
            return
        build_json_tree(self.tree, data)
