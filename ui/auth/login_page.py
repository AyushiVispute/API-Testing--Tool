import customtkinter as ctk
from tkinter import messagebox
from ui.auth.signup_page import SignupPage
from core.auth_db import validate_user


class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)

        self.on_login_success = on_login_success

        ctk.CTkLabel(self, text="Login", font=("Arial", 24, "bold")).pack(pady=20)

        # EMAIL
        ctk.CTkLabel(self, text="Email").pack()
        self.email_entry = ctk.CTkEntry(self, width=260)
        self.email_entry.pack(pady=6)

        # PASSWORD
        ctk.CTkLabel(self, text="Password").pack()
        self.password_entry = ctk.CTkEntry(self, show="*", width=260)
        self.password_entry.pack(pady=6)

        # Login Button
        ctk.CTkButton(self, text="Login", command=self.try_login).pack(pady=10)

        # Signup Redirect
        ctk.CTkButton(self, text="Create Account", command=self.open_signup).pack(pady=4)


    def try_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if validate_user(email, password):
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password!")


    def open_signup(self):
        signup_window = SignupPage(self.master)
        signup_window.grab_set()
