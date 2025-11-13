# core/templates.py
import json
import os

TEMPLATES_PATH = os.path.join("data", "templates.json")
os.makedirs("data", exist_ok=True)

def load_templates():
    """Return dict of templates (name -> template dict)."""
    if not os.path.exists(TEMPLATES_PATH):
        return {}
    try:
        with open(TEMPLATES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_templates(templates: dict):
    """Overwrite the templates file."""
    with open(TEMPLATES_PATH, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)

def save_template(name: str, template: dict):
    templates = load_templates()
    templates[name] = template
    save_templates(templates)

def get_template(name: str):
    return load_templates().get(name)

def delete_template(name: str):
    templates = load_templates()
    if name in templates:
        del templates[name]
        save_templates(templates)
