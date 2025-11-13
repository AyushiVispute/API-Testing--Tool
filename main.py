from ui.main_window import ApiTesterApp
import sys, os
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = ApiTesterApp()
    app.mainloop()
    

