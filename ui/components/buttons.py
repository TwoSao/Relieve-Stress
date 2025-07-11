import customtkinter as ctk
from ui.style import CURRENT_THEME, get_color, get_font

class Button(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        """
        Кастомная кнопка с автоматической поддержкой тем и дополнительными функциями.

        Параметры:
            master: родительский виджет
            **kwargs: дополнительные параметры CTkButton:
                - theme_aware: bool (True) - автоматическое обновление при смене темы
                - highlight: bool (False) - выделенная кнопка (для акцентных действий)
                - disable: bool (False) - создать кнопку в выключенном состоянии
        """
        # Сохраняем ссылку на мастер
        self.master = master

        # Настройки по умолчанию из темы
        defaults = {
            "fg_color": get_color("COLOR_BUTTON_BG"),
            "hover_color": get_color("COLOR_BUTTON_HOVER"),
            "text_color": get_color("COLOR_TEXT"),
            "font": get_font("FONT_MAIN"),
            "border_width": 1,
            "border_color": get_color("COLOR_BUTTON_HOVER"),
            "corner_radius": 6
        }

        # Обработка специальных параметров
        self.theme_aware = kwargs.pop("theme_aware", True)
        self.highlight = kwargs.pop("highlight", False)
        disable = kwargs.pop("disable", False)

        # Применяем настройки по умолчанию, если не указаны явно
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        # Сохраняем оригинальные цвета для сброса
        self.original_colors = {
            "fg": kwargs["fg_color"],
            "hover": kwargs["hover_color"],
            "text": kwargs["text_color"],
            "border": kwargs.get("border_color", kwargs["fg_color"])
        }

        super().__init__(master, **kwargs)

        # Настройка выделенной кнопки
        if self.highlight:
            self.configure(
                fg_color=self._get_highlight_color(),
                hover_color=self._get_highlight_hover_color()
            )

        # Отключение если нужно
        if disable:
            self.disable()

        # Применяем текущую тему
        self.apply_theme()

    def _get_highlight_color(self):
        """Возвращает цвет для выделенной кнопки на основе текущей темы"""
        return "#2E86AB" if CURRENT_THEME.get("COLOR_BG") == "#F5F5F5" else "#3AAED8"

    def _get_highlight_hover_color(self):
        """Возвращает hover-цвет для выделенной кнопки"""
        return "#1F6F8C" if CURRENT_THEME.get("COLOR_BG") == "#F5F5F5" else "#2A8DB8"

    def apply_theme(self):
        """Применяет текущую цветовую тему к кнопке"""
        if self.theme_aware and not self.highlight:
            self.configure(
                fg_color=get_color("COLOR_BUTTON_BG"),
                hover_color=get_color("COLOR_BUTTON_HOVER"),
                text_color=get_color("COLOR_TEXT"),
                border_color=get_color("COLOR_BUTTON_HOVER")
            )

    def reset_colors(self):
        """Сбрасывает цвета к изначальным значениям (игнорируя тему)"""
        self.configure(
            fg_color=self.original_colors["fg"],
            hover_color=self.original_colors["hover"],
            text_color=self.original_colors["text"],
            border_color=self.original_colors["border"]
        )

    def update_theme(self):
        """Обновляет кнопку при смене темы"""
        self.apply_theme()
        if self.highlight:
            self.configure(
                fg_color=self._get_highlight_color(),
                hover_color=self._get_highlight_hover_color()
            )

    def enable(self):
        """Включает кнопку с восстановлением цветов"""
        self.configure(state="normal")
        self.update_theme()

    def disable(self):
        """Отключает кнопку с визуальными изменениями"""
        self.configure(
            state="disabled",
            fg_color="#CCCCCC" if CURRENT_THEME.get("COLOR_BG") == "#F5F5F5" else "#555555",
            text_color="#888888"
        )

    def set_highlight(self, highlight=True):
        """Устанавливает/снимает выделенное состояние кнопки"""
        self.highlight = highlight
        if highlight:
            self.configure(
                fg_color=self._get_highlight_color(),
                hover_color=self._get_highlight_hover_color()
            )
        else:
            self.apply_theme()