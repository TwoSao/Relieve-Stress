import customtkinter as ctk
from ui.style import get_color, get_font

class Button(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        # Убираем кастомные параметры
        self.highlight = kwargs.pop("highlight", False)
        
        # Устанавливаем дефолтные значения
        defaults = {
            "fg_color": get_color("COLOR_ACCENT") if self.highlight else get_color("COLOR_BUTTON_BG"),
            "hover_color": get_color("COLOR_BUTTON_HOVER"),
            "text_color": get_color("COLOR_TEXT"),
            "font": get_font("FONT_NORMAL"),
            "corner_radius": 8
        }
        
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value
        
        super().__init__(master, **kwargs)
    
    def update_theme(self):
        # Обновляем все кнопки одинаково
        self.configure(
            fg_color=get_color("COLOR_ACCENT") if self.highlight else get_color("COLOR_BUTTON_BG"),
            hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT"),  # Всегда используем цвет текста из темы
            font=get_font("FONT_NORMAL")
        )