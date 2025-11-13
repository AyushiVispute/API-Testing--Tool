# ui/pages/settings_panel.py
import customtkinter as ctk
from ui.theame import toggle_theme
from core.templates import load_templates, delete_template

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, templates_manager):
        super().__init__(master)
        self.master = master
        self.templates_manager = templates_manager

        ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=12)

        ctk.CTkButton(self, text="Toggle Theme", command=toggle_theme).pack(pady=8)

        ctk.CTkButton(self, text="Clear All History", fg_color="#cc3333", command=self.clear_history).pack(pady=8)

        ctk.CTkButton(self, text="Manage Templates", command=self.manage_templates).pack(pady=8)

    def clear_history(self):
        import os
        from core.history import DB_PATH, init_db

        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()

    def manage_templates(self):
        self.templates_manager.open_manager(self)
