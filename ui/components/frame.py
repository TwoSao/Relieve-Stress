import customtkinter as ctk
from ui.style import CURRENT_THEME, get_color

class Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """
        Кастомный Frame с автоматической поддержкой тем.

        Параметры:
            master: родительский виджет
            **kwargs: дополнительные параметры для CTkFrame:
                - fg_color: цвет фона (если не указан, берется из текущей темы)
                - theme_aware: bool (True) - автоматически обновлять цвета при смене темы
        """
        # Сохраняем ссылку на мастер для возможного обновления
        self.master = master

        # Если цвет не указан - берем из темы
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = get_color("COLOR_FRAME_BG")

        # Сохраняем оригинальные цвета для возможного сброса
        self.original_fg = kwargs.get("fg_color")
        self.original_bg = kwargs.get("bg_color", kwargs["fg_color"])

        # Включение автоматического обновления темы
        self.theme_aware = kwargs.pop("theme_aware", True)

        super().__init__(master, **kwargs)

        # Применяем текущую тему
        self.apply_theme()

    def apply_theme(self):
        """Применяет текущую цветовую тему к фрейму"""
        if self.theme_aware:
            self.configure(
                fg_color=get_color("COLOR_FRAME_BG"),
                bg_color=get_color("COLOR_FRAME_BG")
            )

    def reset_colors(self):
        """Сбрасывает цвета к изначальным значениям (игнорируя тему)"""
        self.configure(
            fg_color=self.original_fg,
            bg_color=self.original_bg
        )

    def update_theme(self):
        """Обновляет виджет при смене темы (вызывается извне)"""
        self.apply_theme()