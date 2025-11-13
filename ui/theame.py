# ui/theame.py
import customtkinter as ctk

def setup_theme():
    """Apply default theme settings (System / Light / Dark)."""
    try:
        ctk.set_appearance_mode("System")  # respects OS theme by default
        ctk.set_default_color_theme("blue")
    except Exception:
        # if customtkinter isn't available or fails, ignore silently
        pass

def toggle_theme():
    """Toggle between Light and Dark appearance modes."""
    try:
        current = ctk.get_appearance_mode()
        if isinstance(current, str) and current.lower() == "dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
    except Exception:
        pass
