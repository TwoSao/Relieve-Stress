from enum import Enum
from typing import Dict, Any, Callable, List
from ui.style import ThemeType, ThemeManager as BaseThemeManager

class ThemeManager(BaseThemeManager):
    _observers: List[Callable] = []
    
    @classmethod
    def add_observer(cls, callback: Callable) -> None:
        """Добавляет наблюдателя для изменений темы"""
        cls._observers.append(callback)
    
    @classmethod
    def remove_observer(cls, callback: Callable) -> None:
        """Удаляет наблюдателя"""
        if callback in cls._observers:
            cls._observers.remove(callback)
    
    @classmethod
    def set_theme(cls, theme: ThemeType) -> None:
        """Устанавливает тему и уведомляет наблюдателей"""
        super().set_theme(theme)
        cls._notify_observers()
    
    @classmethod
    def _notify_observers(cls) -> None:
        """Уведомляет всех наблюдателей об изменении темы"""
        for callback in cls._observers:
            try:
                callback()
            except Exception as e:
                print(f"Error in theme observer: {e}")
    
    @classmethod
    def get_current_theme(cls) -> ThemeType:
        """Возвращает текущую тему"""
        from ui.style import get_current_theme_name
        theme_name = get_current_theme_name()
        return ThemeType.LIGHT if theme_name == "light" else ThemeType.DARK