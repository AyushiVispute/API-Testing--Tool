## ⭐ INTERNSHIP PROJECT – API Testing Tool (Python Desktop Application)
A modern API testing application built during my internship using Python & CustomTkinter.

📸 Screenshots

![Home Screenshot](assets/screenshots/home.png)
![Settings](assets/screenshots/settings.png)

✨ Features

Send GET, POST, PUT, DELETE requests

Add custom headers and JSON body

Beautify JSON input/output

View responses in:

Raw JSON

Formatted JSON

Pretty Tree View

Maintain request history using SQLite

Save & load custom templates

Copy response to clipboard

Clean and modern UI made with CustomTkinter

Handles long API responses without freezing the UI

## 🛠️ Tech Stack

Python 3

CustomTkinter (UI)

Requests (HTTP client)

SQLite (history & user database)

JSON / Tkinter TreeView (response view)

API-Testing--Tool/
│── assets/
│   └── icons/                # UI icons
│
│── core/
│   ├── api.py                # API request handling
│   ├── auth_db.py            # user db operations
│   ├── history.py            # request history logic
│   ├── templates.py          # template management
│   └── __pycache__/          # compiled Python files
│
│── data/
│   ├── history.db            # SQLite history database
│   ├── templates.json        # user-saved request templates
│   └── users.db              # user login database
│
│── ui/
│   └── (all UI screens/widgets)
│
│── main.py                   # main entry point of the app
│── requirements.txt          # dependencies
│── README.md
│── .gitignore

##  Install dependencies
pip install -r requirements.txt
   ▶️How to Run the Application
    python main.py