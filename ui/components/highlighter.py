# ui/components/highlighter.py
import re
import tkinter as tk

def highlight_json(text_widget: tk.Text):
    content = text_widget.get("1.0", tk.END)
    # clear tags
    for tag in ("key","string","number","bool","null"):
        text_widget.tag_remove(tag, "1.0", tk.END)

    # config (colors chosen simply)
    text_widget.tag_configure("key", foreground="#795E26")
    text_widget.tag_configure("string", foreground="#0B610B")
    text_widget.tag_configure("number", foreground="#0000FF")
    text_widget.tag_configure("bool", foreground="#A52A2A")
    text_widget.tag_configure("null", foreground="#A52A2A")

    # keys: "key":
    for m in re.finditer(r'\"(.*?)\"\s*:', content):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        text_widget.tag_add("key", start, end)

    # strings
    for m in re.finditer(r'\"([^\\\"]*(?:\\.[^\\\"]*)*)\"', content):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        text_widget.tag_add("string", start, end)

    # numbers
    for m in re.finditer(r'\b-?\d+(\.\d+)?\b', content):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        text_widget.tag_add("number", start, end)

    # booleans
    for m in re.finditer(r'\b(true|false)\b', content, re.IGNORECASE):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        text_widget.tag_add("bool", start, end)

    # null
    for m in re.finditer(r'\bnull\b', content, re.IGNORECASE):
        start = "1.0 + %d chars" % m.start()
        end = "1.0 + %d chars" % m.end()
        text_widget.tag_add("null", start, end)
