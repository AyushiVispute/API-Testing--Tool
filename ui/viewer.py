# ui/viewer.py
import json
from tkinter import filedialog, messagebox

def save_response_to_file(response_text):
    """
    Prompt user to save the response displayed in the UI.
    Tries to save prettified JSON if possible, otherwise saves as plain text.
    """
    if not response_text or not response_text.strip():
        messagebox.showinfo("Info", "No response to save.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
    )
    if not path:
        return

    try:
        # try to parse as JSON and pretty-print
        try:
            parsed = json.loads(response_text)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, ensure_ascii=False, indent=4)
        except Exception:
            # fallback: save raw text
            with open(path, "w", encoding="utf-8") as f:
                f.write(response_text)
        messagebox.showinfo("Saved", f"Response saved to {path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")
