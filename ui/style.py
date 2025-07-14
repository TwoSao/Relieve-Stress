from enum import Enum
from typing import Dict, Any, Optional, Tuple

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"

# Оптимизированная система тем с кэшированием
CURRENT_THEME = {}
_THEME_CACHE = {}

LIGHT_THEME = {
    # Основные цвета - светлая тема с лучшим контрастом
    "COLOR_BG": "#F5F5F5",  # Светло-серый фон
    "COLOR_FRAME_BG": "#FFFFFF",  # Белый фон фреймов
    "COLOR_ACCENT": "#1976D2",  # Темно-синий акцент

    # Текст - темный для хорошей читаемости
    "COLOR_TEXT": "#1A1A1A",  # Почти черный текст
    "COLOR_TEXT_SECONDARY": "#666666",  # Темно-серый вторичный текст
    "COLOR_TEXT_DISABLED": "#999999",  # Серый отключенный текст

    # Кнопки - более темные для лучшей видимости
    "COLOR_BUTTON_BG": "#DCDCDC",  # Более темный серый фон кнопок
    "COLOR_BUTTON_HOVER": "#C0C0C0",  # Темнее при наведении
    "COLOR_BUTTON_ACTIVE": "#A8A8A8",  # Еще темнее при нажатии
    "COLOR_BUTTON_DISABLED": "#F0F0F0",  # Очень светлый отключенный

    # Поля ввода
    "COLOR_INPUT_BG": "#FFFFFF",  # Белый фон ввода
    "COLOR_INPUT_BORDER": "#CCCCCC",  # Серая граница
    "COLOR_INPUT_FOCUS": "#1976D2",  # Синяя граница при фокусе

    # Состояния
    "COLOR_SUCCESS": "#388E3C",  # Темно-зеленый успех
    "COLOR_WARNING": "#F57C00",  # Темно-оранжевое предупреждение
    "COLOR_ERROR": "#D32F2F",  # Темно-красная ошибка
    "COLOR_INFO": "#1976D2",  # Темно-синяя информация

    # Шрифты
    "FONT_MAIN": ("Segoe UI", 14),
    "FONT_TITLE": ("Segoe UI", 24, "bold"),
    "FONT_SUBTITLE": ("Segoe UI", 18, "bold"),
    "FONT_NORMAL": ("Segoe UI", 14),
    "FONT_MEDIUM": ("Segoe UI", 16),
    "FONT_SMALL": ("Segoe UI", 12),

    # Разделители
    "COLOR_DIVIDER": "#DDDDDD",
}

DARK_THEME = {
    # Основные цвета - темная тема
    "COLOR_BG": "#1a1a1a",  # Очень темный фон
    "COLOR_FRAME_BG": "#2b2b2b",  # Темно-серый фон фреймов
    "COLOR_ACCENT": "#64B5F6",  # Светло-синий акцент

    # Текст
    "COLOR_TEXT": "#FFFFFF",  # Белый текст
    "COLOR_TEXT_SECONDARY": "#B0B0B0",  # Светло-серый вторичный текст
    "COLOR_TEXT_DISABLED": "#666666",  # Серый отключенный текст

    # Кнопки
    "COLOR_BUTTON_BG": "#3a3a3a",  # Темно-серый фон кнопок
    "COLOR_BUTTON_HOVER": "#4a4a4a",  # Светлее при наведении
    "COLOR_BUTTON_ACTIVE": "#5a5a5a",  # Еще светлее при нажатии
    "COLOR_BUTTON_DISABLED": "#2a2a2a",  # Очень темный отключенный

    # Поля ввода
    "COLOR_INPUT_BG": "#3a3a3a",  # Темно-серый фон ввода
    "COLOR_INPUT_BORDER": "#555555",  # Серая граница
    "COLOR_INPUT_FOCUS": "#64B5F6",  # Синяя граница при фокусе

    # Состояния
    "COLOR_SUCCESS": "#66BB6A",  # Светло-зеленый успех
    "COLOR_WARNING": "#FFB74D",  # Светло-оранжевое предупреждение
    "COLOR_ERROR": "#EF5350",  # Светло-красная ошибка
    "COLOR_INFO": "#64B5F6",  # Светло-синяя информация

    # Шрифты
    "FONT_MAIN": ("Segoe UI", 14),
    "FONT_TITLE": ("Segoe UI", 24, "bold"),
    "FONT_SUBTITLE": ("Segoe UI", 18, "bold"),
    "FONT_NORMAL": ("Segoe UI", 14),
    "FONT_MEDIUM": ("Segoe UI", 16),
    "FONT_SMALL": ("Segoe UI", 12),

    # Разделители
    "COLOR_DIVIDER": "#555555",
}

class ThemeManager:
    _themes = {
        ThemeType.LIGHT: LIGHT_THEME,
        ThemeType.DARK: DARK_THEME
    }
    
    @classmethod
    def set_theme(cls, theme: ThemeType) -> None:
        """Устанавливает текущую тему"""
        global CURRENT_THEME
        if theme not in cls._themes:
            raise ValueError(f"Unknown theme: {theme}")
        CURRENT_THEME.clear()
        CURRENT_THEME.update(cls._themes[theme])
    
    @classmethod
    def add_custom_theme(cls, name: str, theme_data: Dict[str, Any]) -> None:
        """Добавляет пользовательскую тему"""
        cls._themes[name] = theme_data

def set_theme(name: str) -> None:
    """Оптимизированная установка темы с кэшированием."""
    global _THEME_CACHE
    
    # Проверяем кэш
    if name in _THEME_CACHE and CURRENT_THEME == _THEME_CACHE[name]:
        return  # Тема уже установлена
    
    theme_map = {"light": ThemeType.LIGHT, "dark": ThemeType.DARK}
    if name not in theme_map:
        print(f"Неизвестная тема: {name}, используется светлая")
        name = "light"
    
    try:
        ThemeManager.set_theme(theme_map[name])
        _THEME_CACHE[name] = CURRENT_THEME.copy()
    except Exception as e:
        print(f"Ошибка установки темы: {e}")
        # Fallback к светлой теме
        ThemeManager.set_theme(ThemeType.LIGHT)

def get_color(name: str) -> str:
    """Оптимизированное получение цвета с fallback."""
    if not CURRENT_THEME:
        set_theme("light")
    
    color = CURRENT_THEME.get(name)
    if color is None:
        # Fallback цвета для критических элементов
        fallback_colors = {
            "COLOR_BG": "#F5F5F5",
            "COLOR_TEXT": "#1A1A1A",
            "COLOR_BUTTON_BG": "#DCDCDC",
            "COLOR_FRAME_BG": "#FFFFFF"
        }
        color = fallback_colors.get(name, "#000000")
        print(f"Цвет {name} не найден, используется fallback: {color}")
    
    return color

def get_font(name: str):
    """Оптимизированное получение шрифта с fallback."""
    if not CURRENT_THEME:
        set_theme("light")
    
    font = CURRENT_THEME.get(name)
    if font is None:
        # Fallback шрифты
        fallback_fonts = {
            "FONT_TITLE": ("Segoe UI", 24, "bold"),
            "FONT_NORMAL": ("Segoe UI", 14),
            "FONT_SMALL": ("Segoe UI", 12)
        }
        font = fallback_fonts.get(name, ("Segoe UI", 14))
        print(f"Шрифт {name} не найден, используется fallback: {font}")
    
    return font

def get_theme_colors() -> Dict[str, str]:
    """Возвращает все цвета текущей темы"""
    return {k: v for k, v in CURRENT_THEME.items() if k.startswith("COLOR_")}

def get_fonts() -> Dict[str, tuple]:
    """Возвращает все шрифты текущей темы"""
    return {k: v for k, v in CURRENT_THEME.items() if k.startswith("FONT_")}

def get_current_theme_name() -> Optional[str]:
    """Возвращает имя текущей темы"""
    for theme_type, theme_data in ThemeManager._themes.items():
        if CURRENT_THEME == theme_data:
            return theme_type.value if isinstance(theme_type, ThemeType) else theme_type
    return None

def clear_theme_cache() -> None:
    """Очищает кэш тем (для отладки)."""
    global _THEME_CACHE
    _THEME_CACHE.clear()

def get_theme_info() -> dict:
    """Возвращает информацию о текущей теме для отладки."""
    return {
        "current_theme_name": get_current_theme_name(),
        "colors_count": len([k for k in CURRENT_THEME.keys() if k.startswith("COLOR_")]),
        "fonts_count": len([k for k in CURRENT_THEME.keys() if k.startswith("FONT_")]),
        "cache_size": len(_THEME_CACHE)
    }

# Оптимизированная инициализация
try:
    if not CURRENT_THEME:
        set_theme("light")
except Exception as e:
    print(f"Ошибка инициализации темы: {e}")
    # Минимальная тема для работоспособности
    CURRENT_THEME.update({
        "COLOR_BG": "#F5F5F5",
        "COLOR_TEXT": "#1A1A1A",
        "COLOR_BUTTON_BG": "#DCDCDC",
        "COLOR_FRAME_BG": "#FFFFFF",
        "FONT_NORMAL": ("Segoe UI", 14)
    })