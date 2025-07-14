"""Главный модуль приложения Relieve Stress.

Запускает приложение для снятия стресса с настройкой темы и иконки.
"""

from ui.main_window import MainWindow
import customtkinter as ctk


def start_app() -> None:
    """Оптимизированный запуск приложения."""
    try:
        # Оптимизированная настройка CustomTkinter
        ctk.set_appearance_mode("light")  # Фиксированная тема для стабильности
        ctk.set_default_color_theme("blue")
        
        # Создание и запуск главного окна
        app = MainWindow()
        
        # Обработка закрытия приложения
        def on_closing():
            try:
                # Принудительное сохранение настроек
                if hasattr(app, 'settings_manager'):
                    app.settings_manager.force_save()
                # Очистка анимаций
                from ui.animations.transitions import AnimationManager
                AnimationManager.clear_animations()
            except Exception as e:
                print(f"Ошибка при закрытии: {e}")
            finally:
                app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()
        
    except Exception as e:
        print(f"Критическая ошибка запуска: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    start_app()
