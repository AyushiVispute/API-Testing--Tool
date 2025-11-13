# ui/main_window.py
import customtkinter as ctk
import tkinter as tk

from ui.pages.request_page import RequestPage
from ui.pages.history_page import HistoryPage
from ui.pages.settings_panel import SettingsPanel  # UPDATED NAME

from core.templates import load_templates, save_template, load_templates as _load_templates


# ------------------ Templates Manager ------------------
class TemplatesManager:
    """Helper for saving/loading/deleting templates."""
    def __init__(self, parent):
        self.parent = parent

    def ask_name_and_save(self, template):
        import tkinter.simpledialog as sd

        name = sd.askstring("Template Name", "Enter a name for this template:")
        if not name:
            return None

        save_template(name, template)
        return name

    def select_and_load(self, parent_window):
        templates = _load_templates()
        if not templates:
            tk.messagebox.showinfo("Templates", "No templates saved.")
            return None

        win = tk.Toplevel(parent_window)
        win.title("Load Template")
        win.geometry("400x300")

        lb = tk.Listbox(win)
        lb.pack(fill="both", expand=True, padx=8, pady=8)

        names = list(templates.keys())
        for n in names:
            lb.insert(tk.END, n)

        def on_load():
            sel = lb.curselection()
            if not sel:
                return None
            idx = sel[0]
            win.destroy()
            return templates[names[idx]]

        load_btn = ctk.CTkButton(win, text="Load Template", command=lambda: win.destroy())
        load_btn.pack(pady=8)

        win.wait_window()

        sel = lb.curselection()
        if not sel:
            return None
        return templates[names[sel[0]]]

    def open_manager(self, parent):
        templates = _load_templates()

        win = tk.Toplevel(parent)
        win.title("Templates Manager")
        win.geometry("500x350")

        lb = tk.Listbox(win)
        lb.pack(fill="both", expand=True, padx=10, pady=10)

        for name in templates.keys():
            lb.insert(tk.END, name)

        def delete_selected():
            sel = lb.curselection()
            if not sel:
                return
            name = lb.get(sel[0])
            from core.templates import delete_template
            delete_template(name)
            lb.delete(sel[0])

        ctk.CTkButton(win, text="Delete Selected", fg_color="#cc3333", command=delete_selected).pack(pady=10)


# ------------------ API Tester Main App ------------------
class ApiTesterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("API Tester")
        self.geometry("1000x700")
        self.minsize(900, 640)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="⚙  API Tester",
                     font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=20)

        # Main container for page switching
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")

        # Templates Manager
        self.templates_manager = TemplatesManager(self)

        # Pages dict
        self.pages = {
            "request": RequestPage(self.container, self.templates_manager),
            "history": HistoryPage(self.container),
            "settings": SettingsPanel(self.container, self.templates_manager)  # UPDATED
        }

        # Sidebar Buttons
        ctk.CTkButton(self.sidebar, text="Request", command=lambda: self.show_page("request")).grid(row=1, column=0, pady=10, padx=18)
        ctk.CTkButton(self.sidebar, text="History", command=lambda: self.show_page("history")).grid(row=2, column=0, pady=10, padx=18)
        ctk.CTkButton(self.sidebar, text="Settings", command=lambda: self.show_page("settings")).grid(row=3, column=0, pady=10, padx=18)

        # Exit App
        ctk.CTkButton(self.sidebar, text="Exit", fg_color="#cc3333",
                      command=self.destroy).grid(row=10, column=0, pady=20, padx=18)

        # Hide pages initially
        for page in self.pages.values():
            page.pack_forget()

        # Show default page
        self.show_page("request")

    # ------------------ Page Switcher ------------------
    def show_page(self, name: str):
        for page in self.pages.values():
            page.pack_forget()

        selected_page = self.pages.get(name)
        if selected_page:
            selected_page.pack(fill="both", expand=True)


# Run app directly
if __name__ == "__main__":
    app = ApiTesterApp()
    app.mainloop()
