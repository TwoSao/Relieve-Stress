import customtkinter as ctk
from ui.style import CURRENT_THEME, get_color, get_font

class Checkbox(ctk.CTkCheckBox):
    def __init__(self, master, **kwargs):
        """
        Кастомный Checkbox с расширенной функциональностью.

        Параметры:
            master: родительский виджет
            **kwargs:
                - theme_aware: bool (True) - автоматическое обновление при смене темы
                - compact: bool (False) - компактный вариант (меньшие отступы)
                - state: str ("normal"/"disabled") - начальное состояние
                - indicator_size: int (18) - размер индикатора
        """
        # Сохраняем настройки
        self.master = master
        self.theme_aware = kwargs.pop('theme_aware', True)
        compact = kwargs.pop('compact', False)

        # Настройки по умолчанию
        defaults = {
            'fg_color': get_color("COLOR_CHECKBOX_FG"),
            'hover_color': get_color("COLOR_CHECKBOX_HOVER"),
            'border_color': get_color("COLOR_CHECKBOX_HOVER"),
            'text_color': get_color("COLOR_TEXT"),
            'font': get_font("FONT_MAIN"),
            'corner_radius': 4,
            'border_width': 1,
            'indicator_size': 18
        }

        # Применяем defaults только если не указаны явно
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        # Сохраняем оригинальные цвета
        self.original_colors = {
            'fg': kwargs['fg_color'],
            'hover': kwargs['hover_color'],
            'border': kwargs['border_color'],
            'text': kwargs['text_color']
        }

        super().__init__(master, **kwargs)

        # Компактный режим
        if compact:
            self.configure(padx=5, pady=2)

        # Начальное состояние
        if kwargs.get('state') == 'disabled':
            self.disable_style()

    def apply_theme(self):
        """Применяет текущую тему к чекбоксу"""
        if self.theme_aware:
            self.configure(
                fg_color=get_color("COLOR_CHECKBOX_FG"),
                hover_color=get_color("COLOR_CHECKBOX_HOVER"),
                border_color=get_color("COLOR_CHECKBOX_HOVER"),
                text_color=get_color("COLOR_TEXT")
            )

    def update_theme(self):
        """Обновляет виджет при смене темы"""
        self.apply_theme()

    def reset_colors(self):
        """Сбрасывает цвета к изначальным (игнорируя тему)"""
        self.configure(
            fg_color=self.original_colors['fg'],
            hover_color=self.original_colors['hover'],
            border_color=self.original_colors['border'],
            text_color=self.original_colors['text']
        )

    def disable_style(self):
        """Стиль для отключенного состояния"""
        self.configure(
            fg_color="#CCCCCC",
            hover_color="#CCCCCC",
            border_color="#AAAAAA",
            text_color="#888888"
        )

    def enable(self):
        """Включает чекбокс с восстановлением стилей"""
        self.configure(state="normal")
        self.update_theme()

    def disable(self):
        """Отключает чекбокс с визуальными изменениями"""
        self.configure(state="disabled")
        self.disable_style()

    def toggle(self):
        """Переключает состояние чекбокса"""
        current = self.get()
        self.select() if not current else self.deselect()

    def set_value(self, value):
        """Устанавливает значение (True/False)"""
        self.select() if value else self.deselect()