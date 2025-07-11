from ui.main_window import MainWindow
import customtkinter as ctk

def start_app():
    ctk.set_appearance_mode("blue")  # Можно "light"
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.center_window()
    app.iconbitmap("assets/icon.ico")
    app.mainloop()

if __name__ == "__main__":
    start_app()
