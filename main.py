"""Главный модуль приложения Relieve Stress.

Запускает приложение для снятия стресса с настройкой темы и иконки.
"""

from ui.main_window import MainWindow
import customtkinter as ctk


def start_app() -> None:
    """Инициализирует и запускает приложение."""
    # Настройка внешнего вида CustomTkinter
    ctk.set_appearance_mode("system")  # Автоматическая тема
    ctk.set_default_color_theme("blue")
    
    # Создание и запуск главного окна
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    start_app()
