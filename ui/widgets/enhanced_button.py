"""Улучшенная кнопка с анимациями.

Обеспечивает дополнительные визуальные эффекты и анимации.
"""

import customtkinter as ctk
from typing import Optional, Callable, Any
from ui.style import get_color, get_font
from ui.animations.transitions import AnimationManager


class EnhancedButton(ctk.CTkButton):
    """Улучшенная кнопка с поддержкой анимаций и тем."""
    
    def __init__(self, parent: ctk.CTkBaseClass, hover_animation: bool = True, 
                 pulse_on_click: bool = False, **kwargs):
        """Инициализирует улучшенную кнопку.
        
        Args:
            parent: Родительский элемент
            hover_animation: Включить анимацию при наведении
            pulse_on_click: Включить пульсацию при нажатии
        """
        self.hover_animation = hover_animation
        self.pulse_on_click = pulse_on_click
        self._original_command = kwargs.get('command')
        
        # Применяем стандартные стили
        self._apply_default_styles(kwargs)
        
        # Заменяем команду для добавления анимации
        if self.pulse_on_click and self._original_command:
            kwargs['command'] = self._enhanced_command
        
        super().__init__(parent, **kwargs)
        self._setup_hover_effects()
    
    def _apply_default_styles(self, kwargs: dict) -> None:
        """Применяет стандартные стили к кнопке."""
        defaults = {
            'fg_color': get_color("COLOR_BUTTON_BG"),
            'hover_color': get_color("COLOR_BUTTON_HOVER"),
            'text_color': get_color("COLOR_TEXT"),
            'font': get_font("FONT_NORMAL"),
            'corner_radius': 8,
            'border_width': 0
        }
        
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value
    
    def _setup_hover_effects(self) -> None:
        """Настраивает эффекты наведения."""
        if self.hover_animation:
            self.bind("<Enter>", self._on_hover_enter)
            self.bind("<Leave>", self._on_hover_leave)
    
    def _on_hover_enter(self, event) -> None:
        """Обработчик наведения мыши."""
        if self.hover_animation and self.cget('state') != 'disabled':
            AnimationManager.scale_in(self, duration=0.1, scale_from=1.0, scale_to=1.05)
    
    def _on_hover_leave(self, event) -> None:
        """Обработчик ухода мыши."""
        if self.hover_animation and self.cget('state') != 'disabled':
            AnimationManager.scale_in(self, duration=0.1, scale_from=1.05, scale_to=1.0)
    
    def _enhanced_command(self) -> None:
        """Улучшенная команда с анимацией."""
        if self.pulse_on_click:
            AnimationManager.pulse(self, duration=0.3, pulses=1)
        
        if self._original_command:
            try:
                self._original_command()
            except Exception as e:
                print(f"Ошибка в команде кнопки: {e}")
    
    def update_theme(self) -> None:
        """Обновляет тему кнопки."""
        self.configure(
            fg_color=get_color("COLOR_BUTTON_BG"),
            hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL")
        )
    
    def set_loading(self, loading: bool = True) -> None:
        """Устанавливает состояние загрузки."""
        if loading:
            self.configure(state='disabled', text='Загрузка...')
            AnimationManager.pulse(self, duration=2.0, pulses=10)
        else:
            self.configure(state='normal')
    
    def flash_success(self) -> None:
        """Мигание зелёным цветом (успех)."""
        original_color = self.cget('fg_color')
        self.configure(fg_color=get_color("COLOR_SUCCESS"))
        self.after(200, lambda: self.configure(fg_color=original_color))
    
    def flash_error(self) -> None:
        """Мигание красным цветом (ошибка)."""
        original_color = self.cget('fg_color')
        self.configure(fg_color=get_color("COLOR_ERROR"))
        self.after(200, lambda: self.configure(fg_color=original_color))