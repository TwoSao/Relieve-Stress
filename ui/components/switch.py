import customtkinter as ctk
from ui.style import CURRENT_THEME, get_color, get_font

class Switch(ctk.CTkSwitch):
    def __init__(self, master, text="", command=None, **kwargs):
        """
        Кастомный переключатель (Switch) с расширенными возможностями.
        
        Параметры:
            master: родительский виджет
            text: текст рядом с переключателем
            command: функция, вызываемая при изменении состояния
            **kwargs:
                - theme_aware: bool (True) - автоматическое обновление при смене темы
                - state: str ("normal"/"disabled") - начальное состояние
                - indicator_size: tuple (w,h) - размер переключателя
                - compact: bool (False) - компактный вариант
                - highlight: bool (False) - акцентный стиль
        """
        # Сохраняем параметры
        self.master = master
        self.theme_aware = kwargs.pop('theme_aware', True)
        self.highlight = kwargs.pop('highlight', False)
        compact = kwargs.pop('compact', False)

        # Настройки по умолчанию
        defaults = {
            'fg_color': get_color("COLOR_SWITCH_BG"),
            'progress_color': get_color("COLOR_SWITCH_FG"),
            'button_color': get_color("COLOR_SWITCH_BUTTON"),
            'button_hover_color': get_color("COLOR_SWITCH_BUTTON_HOVER"),
            'text_color': get_color("COLOR_TEXT"),
            'font': get_font("FONT_MAIN"),
            'border_width': 1,
            'border_color': get_color("COLOR_SWITCH_BORDER")
        }

        # Применяем defaults только если не указаны явно
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        # Сохраняем оригинальные цвета
        self.original_colors = {
            'fg': kwargs['fg_color'],
            'progress': kwargs['progress_color'],
            'button': kwargs['button_color'],
            'button_hover': kwargs['button_hover_color'],
            'text': kwargs['text_color'],
            'border': kwargs['border_color']
        }

        super().__init__(master, text=text, command=command, **kwargs)

        # Компактный режим
        if compact:
            self.configure(padx=5, pady=2)

        # Акцентный стиль
        if self.highlight:
            self.set_highlight(True)

        # Начальное состояние
        if kwargs.get('state') == 'disabled':
            self.disable_style()

        # Применяем текущую тему
        self.apply_theme()

    def apply_theme(self):
        """Применяет текущую тему к переключателю"""
        if self.theme_aware and not self.highlight:
            self.configure(
                fg_color=get_color("COLOR_SWITCH_BG"),
                progress_color=get_color("COLOR_SWITCH_FG"),
                button_color=get_color("COLOR_SWITCH_BUTTON"),
                button_hover_color=get_color("COLOR_SWITCH_BUTTON_HOVER"),
                text_color=get_color("COLOR_TEXT"),
                border_color=get_color("COLOR_SWITCH_BORDER")
            )

    def update_theme(self):
        """Обновляет виджет при смене темы"""
        self.apply_theme()
        if self.highlight:
            self.set_highlight(True)

    def reset_colors(self):
        """Сбрасывает цвета к изначальным (игнорируя тему)"""
        self.configure(
            fg_color=self.original_colors['fg'],
            progress_color=self.original_colors['progress'],
            button_color=self.original_colors['button'],
            button_hover_color=self.original_colors['button_hover'],
            text_color=self.original_colors['text'],
            border_color=self.original_colors['border']
        )

    def set_highlight(self, highlight=True):
        """Устанавливает/снимает акцентный стиль"""
        self.highlight = highlight
        if highlight:
            accent_color = "#2E86AB" if CURRENT_THEME.get("COLOR_BG") == "#F5F5F5" else "#3AAED8"
            self.configure(
                progress_color=accent_color,
                button_color="#FFFFFF",
                button_hover_color="#EEEEEE"
            )
        else:
            self.apply_theme()

    def disable_style(self):
        """Стиль для отключенного состояния"""
        self.configure(
            fg_color="#E0E0E0",
            progress_color="#B0B0B0",
            button_color="#F0F0F0",
            button_hover_color="#F0F0F0",
            text_color="#888888"
        )

    def enable(self):
        """Включает переключатель с восстановлением стилей"""
        self.configure(state="normal")
        self.update_theme()

    def disable(self):
        """Отключает переключатель с визуальными изменениями"""
        self.configure(state="disabled")
        self.disable_style()

    def toggle(self):
        """Переключает состояние"""
        self.set(not self.get())

    def set_value(self, value):
        """Устанавливает значение (True/False)"""
        self.set(value)

    def is_on(self):
        """Возвращает True если переключатель включен"""
        return self.get()