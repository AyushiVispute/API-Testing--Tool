# ui/components/toolbar.py

import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, on_send, on_beautify, on_copy, on_save_template, on_load_template):
        super().__init__(master, fg_color="transparent")

        self.send_btn = ctk.CTkButton(self, text="Send", width=120, command=on_send)
        self.send_btn.pack(side="left", padx=5, pady=5)

        self.beautify_btn = ctk.CTkButton(self, text="Beautify JSON", width=140, command=on_beautify)
        self.beautify_btn.pack(side="left", padx=5)

        self.copy_btn = ctk.CTkButton(self, text="Copy Response", width=150, command=on_copy)
        self.copy_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(self, text="Save Request as Template", width=200, command=on_save_template)
        self.save_btn.pack(side="left", padx=5)

        self.load_btn = ctk.CTkButton(self, text="Load Template", width=150, command=on_load_template)
        self.load_btn.pack(side="left", padx=5)
