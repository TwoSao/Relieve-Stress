from enum import Enum
from typing import Dict, Any, Optional, Tuple

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"

CURRENT_THEME = {}

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
    "FONT_SMALL": ("Segoe UI", 12),

    # Разделители
    "COLOR_DIVIDER": "#DDDDDD",
}

DARK_THEME = {
    # Основные цвета - темная тема
    "COLOR_BG": "#121212",  # Очень темный фон
    "COLOR_FRAME_BG": "#1E1E1E",  # Темно-серый фон фреймов
    "COLOR_ACCENT": "#64B5F6",  # Светло-синий акцент

    # Текст
    "COLOR_TEXT": "#FFFFFF",  # Белый текст
    "COLOR_TEXT_SECONDARY": "#B0B0B0",  # Светло-серый вторичный текст
    "COLOR_TEXT_DISABLED": "#666666",  # Серый отключенный текст

    # Кнопки
    "COLOR_BUTTON_BG": "#2C2C2C",  # Темно-серый фон кнопок
    "COLOR_BUTTON_HOVER": "#3C3C3C",  # Светлее при наведении
    "COLOR_BUTTON_ACTIVE": "#4C4C4C",  # Еще светлее при нажатии
    "COLOR_BUTTON_DISABLED": "#1A1A1A",  # Очень темный отключенный

    # Поля ввода
    "COLOR_INPUT_BG": "#2C2C2C",  # Темно-серый фон ввода
    "COLOR_INPUT_BORDER": "#404040",  # Серая граница
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
    "FONT_SMALL": ("Segoe UI", 12),

    # Разделители
    "COLOR_DIVIDER": "#404040",
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
    """Устанавливает текущую тему (light/dark)"""
    theme_map = {"light": ThemeType.LIGHT, "dark": ThemeType.DARK}
    if name not in theme_map:
        raise ValueError(f"Unknown theme name: {name}")
    ThemeManager.set_theme(theme_map[name])

def get_color(name: str) -> str:
    """Возвращает цвет из текущей темы по имени"""
    if not CURRENT_THEME:
        set_theme("light")  # Default theme
    return CURRENT_THEME.get(name, "#000000")

def get_font(name: str):
    """Возвращает шрифт из текущей темы по имени"""
    if not CURRENT_THEME:
        set_theme("light")  # Default theme
    return CURRENT_THEME.get(name, ("Arial", 14))

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

# Initialize with light theme by default
if not CURRENT_THEME:
    set_theme("light")