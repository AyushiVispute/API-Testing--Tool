# ui/pages/request_page.py

import customtkinter as ctk
import json
import tkinter as tk
from tkinter import messagebox

from core.api import send_request_async
from ui.components.toolbar import Toolbar
from ui.viewer import ResponseRaw, ResponseTree


class RequestPage(ctk.CTkFrame):
    def __init__(self, master, templates_manager):
        super().__init__(master)
        self.templates_manager = templates_manager

        # ---------------- TOP AREA ----------------
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(top_frame, text="URL:").pack(side="left", padx=5)
        self.url_entry = ctk.CTkEntry(top_frame, width=550)
        self.url_entry.pack(side="left", padx=5)

        ctk.CTkLabel(top_frame, text="Method:").pack(side="left", padx=5)
        self.method_box = ctk.CTkComboBox(top_frame, values=["GET", "POST", "PUT", "DELETE"], width=100)
        self.method_box.set("GET")
        self.method_box.pack(side="left", padx=5)

        # ---------------- HEADERS ----------------
        ctk.CTkLabel(self, text="Headers (JSON):").pack(anchor="w", padx=12)
        self.headers_text = ctk.CTkTextbox(self, width=850, height=90)
        self.headers_text.pack(padx=10, pady=5)

        # ---------------- BODY ----------------
        ctk.CTkLabel(self, text="Body (JSON):").pack(anchor="w", padx=12)
        self.body_text = ctk.CTkTextbox(self, width=850, height=120)
        self.body_text.pack(padx=10, pady=5)

        # ---------------- TOOLBAR ----------------
        self.toolbar = Toolbar(
            self,
            on_send=self.send_request,
            on_beautify=self.beautify_current,
            on_copy=self.copy_raw,
            on_save_template=self.save_current_template,
            on_load_template=self.load_template_dialog
        )
        self.toolbar.pack(fill="x", pady=5, padx=10)

        # ---------------- RESPONSE TABS ----------------
        self.response_tabs = ctk.CTkTabview(self)
        self.response_tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # RAW RESPONSE
        self.raw_tab = self.response_tabs.add("Raw")
        self.raw_viewer = ResponseRaw(self.raw_tab)
        self.raw_viewer.pack(fill="both", expand=True)

        # TREE VIEW
        self.tree_tab = self.response_tabs.add("Tree")
        self.tree_viewer = ResponseTree(self.tree_tab)
        self.tree_viewer.pack(fill="both", expand=True)

    # ===============================================================
    # SEND REQUEST  (🔥 SAFE JSON — NO ERRORS)
    # ===============================================================
    def send_request(self):
        url = self.url_entry.get().strip()
        method = self.method_box.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        # ----- SAFE HEADER PARSE -----
        try:
            headers_raw = self.headers_text.get("1.0", "end").strip()
            headers = json.loads(headers_raw) if headers_raw else {}
        except:
            headers = {}

        # ----- SAFE BODY PARSE (NO POPUP EVER) -----
        body_raw = self.body_text.get("1.0", "end").strip()
        try:
            body = json.loads(body_raw) if body_raw else None
        except:
            body = None

        # SEND REQ
        send_request_async(
            method=method,
            url=url,
            headers=headers,
            body=body,
            callback=self.display_response
        )

    # ===============================================================
    # DISPLAY RESPONSE
    # ===============================================================
    def display_response(self, data):
        if "error" in data:
            self.raw_viewer.update_text(f"Error:\n{data['error']}")
            self.tree_viewer.clear()
            return

        status = data["status"]
        headers_json = json.dumps(data["headers"], indent=4)
        body_text = data["body"]
        response_time = data["time"]

        full_output = (
            f"Status: {status}\n"
            f"Time: {response_time}s\n\n"
            f"Headers:\n{headers_json}\n\n"
            f"Body:\n{body_text}"
        )

        # Show raw
        self.raw_viewer.update_text(full_output)

        # Try JSON for tree view
        try:
            json_body = json.loads(body_text)
            self.tree_viewer.load_json(json_body)
        except:
            self.tree_viewer.clear()

    # ===============================================================
    # BEAUTIFY JSON BUTTON
    # ===============================================================
    def beautify_current(self):
        # Read text from body (CustomTkinter adds hidden characters)
        text = self.body_text.get("1.0", "end")

        # Sanitize: remove invisible characters
        cleaned = text.replace("\r", "").replace("\n", "").replace("\t", "").strip()

        if cleaned == "":
            return  # nothing to format

        try:
            parsed = json.loads(cleaned)
            pretty = json.dumps(parsed, indent=4)

            # Write formatted JSON
            self.body_text.delete("1.0", "end")
            self.body_text.insert("end", pretty)

        except Exception as e:
            # Invalid JSON → ignore silently
            return


    # ===============================================================
    # COPY RAW
    # ===============================================================
    def copy_raw(self):
        text = self.raw_viewer.get_text()
        self.clipboard_clear()
        self.clipboard_append(text)

    # ===============================================================
    # SAVE TEMPLATE
    # ===============================================================
    def save_current_template(self):
        template = {
            "url": self.url_entry.get(),
            "method": self.method_box.get(),
            "headers": self.headers_text.get("1.0", "end").strip(),
            "body": self.body_text.get("1.0", "end").strip(),
        }
        self.templates_manager.ask_name_and_save(template)

    # ===============================================================
    # LOAD TEMPLATE
    # ===============================================================
    def load_template_dialog(self):
        tpl = self.templates_manager.select_and_load(self)
        if tpl:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, tpl["url"])

            self.method_box.set(tpl["method"])

            self.headers_text.delete("1.0", "end")
            self.headers_text.insert("end", tpl["headers"])

            self.body_text.delete("1.0", "end")
            self.body_text.insert("end", tpl["body"])
