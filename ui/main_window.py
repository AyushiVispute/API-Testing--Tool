import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import time
import os


class ApiTesterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python API Tester")
        self.geometry("850x650")
        self.configure(bg="#f4f4f4")

        # --- URL & Method ---
        frame_top = tk.Frame(self, bg="#f4f4f4")
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="API URL:", bg="#f4f4f4").grid(row=0, column=0, padx=5)
        self.url_entry = tk.Entry(frame_top, width=60)
        self.url_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_top, text="Method:", bg="#f4f4f4").grid(row=0, column=2, padx=5)
        self.method = ttk.Combobox(frame_top, values=["GET", "POST", "PUT", "DELETE"], width=10)
        self.method.current(0)
        self.method.grid(row=0, column=3, padx=5)

        # --- Headers & Body ---
        tk.Label(self, text="Headers (JSON):", bg="#f4f4f4").pack()
        self.headers_text = tk.Text(self, height=5, width=95)
        self.headers_text.pack(pady=5)

        tk.Label(self, text="Body (JSON):", bg="#f4f4f4").pack()
        self.body_text = tk.Text(self, height=5, width=95)
        self.body_text.pack(pady=5)

        # --- Buttons ---
        frame_buttons = tk.Frame(self, bg="#f4f4f4")
        frame_buttons.pack(pady=5)

        send_btn = tk.Button(frame_buttons, text="Send Request", command=self.send_request, bg="#0078D7", fg="white")
        send_btn.grid(row=0, column=0, padx=10)

        clear_btn = tk.Button(frame_buttons, text="Clear", command=self.clear_fields)
        clear_btn.grid(row=0, column=1, padx=10)

        history_btn = tk.Button(frame_buttons, text="View History", command=self.view_history)
        history_btn.grid(row=0, column=2, padx=10)

        # --- Response ---
        tk.Label(self, text="Response:", bg="#f4f4f4").pack()
        self.response_text = tk.Text(self, height=15, width=95)
        self.response_text.pack(pady=5)

    # ---------------------------------------------
    def send_request(self):
        """Handles sending API requests and displaying results."""
        url = self.url_entry.get().strip()
        method = self.method.get().strip()
        headers_text = self.headers_text.get("1.0", tk.END).strip()
        body_text = self.body_text.get("1.0", tk.END).strip()

        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        try:
            headers = json.loads(headers_text) if headers_text else {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in headers")
            return

        try:
            data = json.loads(body_text) if body_text else None
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in body")
            return

        try:
            start = time.time()
            response = requests.request(method, url, headers=headers, json=data)
            elapsed = round(time.time() - start, 2)

            output = (
                f"Status: {response.status_code}\n"
                f"Time: {elapsed}s\n\n"
                f"Headers:\n{response.headers}\n\n"
                f"Body:\n{response.text}"
            )

            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, output)

            # Save history
            self.save_to_history(url, method, headers, data, response.text, response.status_code, elapsed)

        except Exception as e:
            messagebox.showerror("Request Failed", str(e))

    # ---------------------------------------------
    def save_to_history(self, url, method, headers, body, response, status, time_taken):
        """Saves request and response data to history.json."""
        history_path = os.path.join("data", "history.json")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)

        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        else:
            history = []

        entry = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
            "status": status,
            "response": response[:1000],  # truncate long response
            "time": time_taken
        }
        history.append(entry)

        with open(history_path, "w") as f:
            json.dump(history, f, indent=4)

    # ---------------------------------------------
    def view_history(self):
        """Displays all saved requests from history.json in a popup."""
        history_path = os.path.join("data", "history.json")
        if not os.path.exists(history_path):
            messagebox.showinfo("History", "No history found yet.")
            return

        try:
            with open(history_path, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to read history file.")
            return

        if not history:
            messagebox.showinfo("History", "No saved requests yet.")
            return

        # Popup window
        history_win = tk.Toplevel(self)
        history_win.title("Request History")
        history_win.geometry("700x500")
        history_win.configure(bg="#f9f9f9")

        tk.Label(history_win, text="Saved Request History", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=10)

        text_area = scrolledtext.ScrolledText(history_win, wrap=tk.WORD, width=85, height=25)
        text_area.pack(padx=10, pady=5)

        # Add all saved requests
        for i, entry in enumerate(history, start=1):
            text_area.insert(
                tk.END,
                f"{i}. {entry['method']} {entry['url']} | Status: {entry['status']} | Time: {entry['time']}s\n"
            )

        text_area.config(state=tk.DISABLED)

    # ---------------------------------------------
    def clear_fields(self):
        """Clears all input and output fields."""
        self.url_entry.delete(0, tk.END)
        self.headers_text.delete("1.0", tk.END)
        self.body_text.delete("1.0", tk.END)
        self.response_text.delete("1.0", tk.END)
