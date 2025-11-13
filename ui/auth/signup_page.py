import customtkinter as ctk
from tkinter import messagebox
from core.auth_db import add_user


class SignupPage(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create Account")
        self.geometry("350x370")

        ctk.CTkLabel(self, text="Signup", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(self, text="Email").pack()
        self.email_entry = ctk.CTkEntry(self, width=240)
        self.email_entry.pack(pady=6)

        ctk.CTkLabel(self, text="Password").pack()
        self.password_entry = ctk.CTkEntry(self, show="*", width=240)
        self.password_entry.pack(pady=6)

        ctk.CTkLabel(self, text="Confirm Password").pack()
        self.confirm_entry = ctk.CTkEntry(self, show="*", width=240)
        self.confirm_entry.pack(pady=6)

        ctk.CTkButton(self, text="Sign Up", command=self.signup).pack(pady=12)


    def signup(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields required!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if add_user(email, password):
            messagebox.showinfo("Success", "Account created! You can now login.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Email already exists!")
