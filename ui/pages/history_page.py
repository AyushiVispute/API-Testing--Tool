# ui/pages/history_page.py
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from core.history import get_all_history, get_history_by_id

class HistoryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text="Request History", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.listbox = tk.Listbox(self, height=20)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=6)

        ctk.CTkButton(btn_frame, text="Refresh", command=self.load_history).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="Load Selected", command=self.load_selected).grid(row=0, column=1, padx=6)

        self.load_history()

    def load_history(self):
        self.listbox.delete(0, tk.END)
        rows = get_all_history()
        for r in rows:
            # r: (id, method, url, status, time_taken, timestamp)
            self.listbox.insert(tk.END, f"{r[0]}. {r[2]} [{r[1]}] | Status: {r[3]} | {r[4]}s")

    def load_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Select", "Please select an entry.")
            return
        idx = sel[0]
        row_id = get_all_history()[idx][0]
        row = get_history_by_id(row_id)
        if not row:
            messagebox.showerror("Error", "Entry not found.")
            return
        # row order from history.py: (id, url, method, headers, body, status, response, time_taken, timestamp)
        _, url, method, headers_json, body_json, *_ = row
        # populate Request page fields
        self.master.pages["request"].url_entry.delete(0, tk.END)
        self.master.pages["request"].url_entry.insert(0, url)
        self.master.pages["request"].method_box.set(method)
        self.master.pages["request"].headers.delete("1.0", tk.END)
        self.master.pages["request"].headers.insert(tk.END, headers_json or "")
        self.master.pages["request"].body.delete("1.0", tk.END)
        self.master.pages["request"].body.insert(tk.END, body_json or "")
        # switch tab
        self.master.show_page("request")
