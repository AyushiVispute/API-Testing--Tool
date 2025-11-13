import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter as ctk
import json

# IMPORTS USING YOUR EXACT FILE NAMES
from core.api import send_request_async
from core.history import init_db, save_history, get_all_history, get_history_by_id
from ui.viewer import save_response_to_file
from ui.theame import setup_theme, toggle_theme


class ApiTesterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        setup_theme()
        init_db()

        self.title("API Tester")
        self.geometry("1000x700")
        self.minsize(900, 640)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="⚙  API Tester",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=20)

        ctk.CTkButton(self.sidebar, text="Request",
                      command=self.show_request_tab).grid(row=1, column=0, pady=10)
        ctk.CTkButton(self.sidebar, text="History",
                      command=self.show_history_tab).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self.sidebar, text="Settings",
                      command=self.show_settings_tab).grid(row=3, column=0, pady=10)

        ctk.CTkButton(self.sidebar, text="Exit",
                      fg_color="#cc3333", command=self.destroy).grid(row=7, column=0, pady=20)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")

        # Initialize tabs
        self.request_tab()
        self.history_tab()
        self.settings_tab()

        self.show_request_tab()

    # ---------------- REQUEST TAB ----------------
    def request_tab(self):
        self.req_frame = ctk.CTkFrame(self.container)

        ctk.CTkLabel(self.req_frame, text="Send API Request",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # URL + Method row
        top = ctk.CTkFrame(self.req_frame)
        top.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(top, text="URL:").grid(row=0, column=0)
        self.url_entry = ctk.CTkEntry(top, width=550)
        self.url_entry.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(top, text="Method:").grid(row=0, column=2)
        self.method_box = ctk.CTkOptionMenu(top, values=["GET", "POST", "PUT", "DELETE"])
        self.method_box.set("GET")
        self.method_box.grid(row=0, column=3, padx=5)

        # Headers
        ctk.CTkLabel(self.req_frame, text="Headers (JSON):").pack(anchor="w", padx=10)
        self.headers = tk.Text(self.req_frame, height=6, width=100)
        self.headers.pack(padx=10, pady=5)

        # Body
        ctk.CTkLabel(self.req_frame, text="Body (JSON):").pack(anchor="w", padx=10)
        self.body = tk.Text(self.req_frame, height=6, width=100)
        self.body.pack(padx=10, pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(self.req_frame)
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="Send", command=self.send_request).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="Clear", command=self.clear_all).grid(row=0, column=1, padx=6)
        ctk.CTkButton(btn_frame, text="Save Response",
                      command=lambda: save_response_to_file(self.response.get("1.0", tk.END))).grid(row=0, column=2, padx=6)

        # Response
        ctk.CTkLabel(self.req_frame, text="Response:").pack(anchor="w", padx=10)
        self.response = scrolledtext.ScrolledText(self.req_frame, height=16)
        self.response.pack(fill="both", expand=True, padx=10, pady=5)

    # -------------- SEND REQUEST --------------
    def send_request(self):
        url = self.url_entry.get().strip()
        method = self.method_box.get()

        # SAFE JSON PARSING
        try:
            headers_text = self.headers.get("1.0", tk.END).strip()
            headers = json.loads(headers_text) if headers_text else {}

            body_text = self.body.get("1.0", tk.END).strip()
            body = json.loads(body_text) if body_text else None
        except:
            messagebox.showerror("Error", "Invalid JSON in headers/body.")
            return

        # 🔥 Auto-add headers (fix GitHub & many APIs)
        headers.setdefault("User-Agent", "API-Tester-App/1.0")
        headers.setdefault("Accept", "application/json")

        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.response.delete("1.0", tk.END)
        self.response.insert(tk.END, "⏳ Sending request...\n")

        send_request_async(method, url, headers, body, self.show_response)

    # -------------- DISPLAY RESPONSE --------------
    def show_response(self, result):
        self.response.delete("1.0", tk.END)

        if "error" in result:
            self.response.insert(tk.END, f"❌ {result['error']}")
            return

        text = (
            f"Status: {result['status']}\n"
            f"Time: {result['time']}s\n\n"
            f"Headers:\n{json.dumps(result['headers'], indent=2)}\n\n"
            f"Body:\n{result['body']}"
        )

        self.response.insert(tk.END, text)

        # SAFE JSON for saving to history
        headers_text = self.headers.get("1.0", tk.END).strip()
        body_text = self.body.get("1.0", tk.END).strip()

        try:
            parsed_headers = json.loads(headers_text) if headers_text else {}
        except:
            parsed_headers = {}

        try:
            parsed_body = json.loads(body_text) if body_text else None
        except:
            parsed_body = None

        save_history(
            self.url_entry.get(),
            self.method_box.get(),
            parsed_headers,
            parsed_body,
            result["body"],
            result["status"],
            result["time"]
        )

    def clear_all(self):
        self.url_entry.delete(0, tk.END)
        self.headers.delete("1.0", tk.END)
        self.body.delete("1.0", tk.END)
        self.response.delete("1.0", tk.END)

    # ---------------- HISTORY TAB ----------------
    def history_tab(self):
        self.hist_frame = ctk.CTkFrame(self.container)

        ctk.CTkLabel(self.hist_frame, text="Request History",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.hist_list = tk.Listbox(self.hist_frame, height=20)
        self.hist_list.pack(fill="both", expand=True, padx=10)

        ctk.CTkButton(self.hist_frame, text="Refresh",
                      command=self.load_history).pack(pady=5)
        ctk.CTkButton(self.hist_frame, text="Load Selected",
                      command=self.load_selected_request).pack(pady=5)

    def load_history(self):
        self.hist_list.delete(0, tk.END)
        for row in get_all_history():
            self.hist_list.insert(
                tk.END,
                f"{row[0]}. {row[2]} {row[1]} | Status {row[3]} | {row[4]}s"
            )

    def load_selected_request(self):
        selection = self.hist_list.curselection()
        if not selection:
            return

        row_id = get_all_history()[selection[0]][0]
        data = get_history_by_id(row_id)

        if not data:
            return

        _, url, method, headers_json, body_json, *_ = data

        self.show_request_tab()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

        self.method_box.set(method)
        self.headers.delete("1.0", tk.END)
        self.headers.insert(tk.END, headers_json or "")
        self.body.delete("1.0", tk.END)
        self.body.insert(tk.END, body_json or "")

    # ---------------- SETTINGS TAB ----------------
    def settings_tab(self):
        self.settings_frame = ctk.CTkFrame(self.container)

        ctk.CTkLabel(self.settings_frame, text="Settings",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

        ctk.CTkButton(self.settings_frame, text="Toggle Theme",
                      command=toggle_theme).pack(pady=10)

    # ---------------- TAB SWITCHING ----------------
    def show_request_tab(self):
        self._hide_tabs()
        self.req_frame.pack(fill="both", expand=True)

    def show_history_tab(self):
        self._hide_tabs()
        self.hist_frame.pack(fill="both", expand=True)
        self.load_history()

    def show_settings_tab(self):
        self._hide_tabs()
        self.settings_frame.pack(fill="both", expand=True)

    def _hide_tabs(self):
        for frame in [
            getattr(self, "req_frame", None),
            getattr(self, "hist_frame", None),
            getattr(self, "settings_frame", None)
        ]:
            if frame:
                frame.pack_forget()
