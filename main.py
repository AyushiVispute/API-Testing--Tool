import customtkinter as ctk
from core.auth_db import init_auth_db
from ui.auth.login_page import LoginPage
from ui.main_window import ApiTesterApp


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("API Tester - Login")
        self.geometry("420x360")

        init_auth_db()

        self.login_page = LoginPage(self, self.open_main_app)
        self.login_page.pack(fill="both", expand=True)

    def open_main_app(self):
        self.login_page.destroy()
        self.destroy()  # Close the login window

        # Start main API Tester
        app = ApiTesterApp()
        app.mainloop()


if __name__ == "__main__":
    App().mainloop()


