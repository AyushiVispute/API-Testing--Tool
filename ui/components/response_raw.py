# ui/components/response_raw.py
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk
import json
from ui.components.highlighter import highlight_json

class ResponseRaw(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Tab-like: show raw and may coordinate with ResponseTree externally
        self.raw_text = scrolledtext.ScrolledText(self, height=16, wrap=tk.WORD)
        self.raw_text.pack(fill="both", expand=True)

        # Keep reference to tree widget if provided
        self.tree_widget = None

    def add_tree_widget(self, tree_widget):
        self.tree_widget = tree_widget

    def set_text(self, text):
        self.raw_text.configure(state="normal")
        self.raw_text.delete("1.0", tk.END)
        self.raw_text.insert(tk.END, text)
        self.raw_text.see(tk.END)
        highlight_json(self.raw_text)
        self.raw_text.configure(state="normal")

    def get_text(self):
        return self.raw_text.get("1.0", tk.END)

    def beautify(self):
        txt = self.get_text()
        # try to find body json part
        try:
            if "Body:\n" in txt:
                head, body = txt.split("Body:\n", 1)
                parsed = json.loads(body.strip())
                pretty = json.dumps(parsed, indent=4, ensure_ascii=False)
                new = head + "Body:\n" + pretty
            else:
                parsed = json.loads(txt.strip())
                new = json.dumps(parsed, indent=4, ensure_ascii=False)
            self.set_text(new)
        except Exception:
            # nothing to beautify
            return

    def copy_to_clipboard(self):
        text = self.get_text()
        if not text.strip():
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
        except Exception:
            pass
