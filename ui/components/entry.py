import customtkinter as ctk
from ui.style import CURRENT_THEME, get_color, get_font

class Entry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        # Забираем placeholder из kwargs, чтобы не передавать его в CTkEntry
        self.placeholder = kwargs.pop('placeholder', "")
        self.placeholder_color = get_color("COLOR_TEXT_SECONDARY")
        self.default_text_color = get_color("COLOR_TEXT")

        self.master = master
        self.theme_aware = kwargs.pop('theme_aware', True)
        self._previous_state = 'normal'

        # Настройки по умолчанию
        defaults = {
            'fg_color': get_color("COLOR_INPUT_BG"),
            'border_color': get_color("COLOR_INPUT_BORDER"),
            'text_color': self.default_text_color,
            'font': get_font("FONT_MAIN"),
            'border_width': 1,
            'corner_radius': 4
        }

        # Применяем defaults только если не указаны явно
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        super().__init__(master, **kwargs)

        # Подключаем обработчики событий для placeholder
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        # Если поле пустое, показываем placeholder
        self._add_placeholder()

        # Начальное состояние
        if kwargs.get('state') == 'disabled':
            self.disable_style()
        elif kwargs.get('state') == 'readonly':
            self.set_readonly(True)

        # Применяем текущую тему
        self.apply_theme()

        # Настройка валидации
        if 'validate' in kwargs and 'validate_command' in kwargs:
            self.configure(validate=kwargs['validate'],
                           validatecommand=kwargs['validate_command'])

    def _add_placeholder(self, event=None):
        if not super().get():
            super().insert(0, self.placeholder)
            self.configure(text_color=self.placeholder_color)

    def _clear_placeholder(self, event=None):
        if super().get() == self.placeholder:
            super().delete(0, "end")
            self.configure(text_color=self.default_text_color)

    # Переопределяем get и set, чтобы не возвращать placeholder как текст
    def get(self):
        text = super().get()
        if text == self.placeholder:
            return ""
        return text.strip()

    def set(self, text):
        super().delete(0, "end")
        if text:
            super().insert(0, text)
            self.configure(text_color=self.default_text_color)
        else:
            self._add_placeholder()
    def apply_theme(self):
        """Применяет текущую тему к полю ввода"""
        if self.theme_aware:
            self.configure(
                fg_color=get_color("COLOR_INPUT_BG"),
                border_color=get_color("COLOR_INPUT_BORDER"),
                text_color=get_color("COLOR_TEXT"),
                placeholder_text_color=get_color("COLOR_TEXT_SECONDARY")
            )

    def update_theme(self):
        """Обновляет виджет при смене темы"""
        self.apply_theme()

    def reset_colors(self):
        """Сбрасывает цвета к изначальным (игнорируя тему)"""
        self.configure(
            fg_color=self.original_colors['fg'],
            border_color=self.original_colors['border'],
            text_color=self.original_colors['text'],
            placeholder_text_color=self.original_colors['placeholder']
        )

    def set(self, text):
        """Устанавливает текст в поле"""
        self.delete(0, 'end')
        self.insert(0, text)

    def get(self):
        """Возвращает текст из поля (с удалением лишних пробелов)"""
        return super().get().strip()

    def clear(self):
        """Очищает поле ввода"""
        self.set("")

    def disable_style(self):
        """Стиль для отключенного состояния"""
        self._previous_state = self.cget('state')
        self.configure(
            state='disabled',
            fg_color="#F0F0F0",
            border_color="#D0D0D0",
            text_color="#888888"
        )

    def enable(self):
        """Включает поле ввода с восстановлением стилей"""
        self.configure(state=self._previous_state)
        self.update_theme()

    def disable(self):
        """Отключает поле ввода с визуальными изменениями"""
        self.disable_style()

    def set_readonly(self, readonly=True):
        """Устанавливает режим 'только для чтения'"""
        self._previous_state = 'readonly' if readonly else 'normal'
        self.configure(state='readonly' if readonly else 'normal')
        if readonly:
            self.configure(
                fg_color="#F8F8F8",
                border_color="#E0E0E0"
            )
        else:
            self.update_theme()

    def set_error_style(self, is_error=True):
        """Устанавливает/снимает стиль ошибки"""
        if is_error:
            self.configure(border_color="#FF4444")
        else:
            self.apply_theme()

    def set_success_style(self, is_success=True):
        """Устанавливает/снимает стиль успеха"""
        if is_success:
            self.configure(border_color="#44FF44")
        else:
            self.apply_theme()

    def add_trailing_icon(self, icon, command=None):
        """Добавляет иконку в конец поля"""
        # Реализация зависит от используемой библиотеки иконок
        pass