CURRENT_THEME = {}

LIGHT_THEME = {
    # Основные цвета
    "COLOR_BG": "#F5F5F5",  # Фон главного окна
    "COLOR_FRAME_BG": "#FFFFFF",  # Фон фреймов
    "COLOR_ACCENT": "#4A90E2",  # Акцентный цвет

    # Текст
    "COLOR_TEXT": "#000000",
    "COLOR_TEXT_SECONDARY": "#666666",
    "COLOR_TEXT_DISABLED": "#999999",

    # Кнопки
    "COLOR_BUTTON_BG": "#DDDDDD",
    "COLOR_BUTTON_HOVER": "#CCCCCC",
    "COLOR_BUTTON_ACTIVE": "#BBBBBB",
    "COLOR_BUTTON_DISABLED": "#EEEEEE",

    # Поля ввода
    "COLOR_INPUT_BG": "#FFFFFF",
    "COLOR_INPUT_BORDER": "#CCCCCC",
    "COLOR_INPUT_FOCUS": "#4A90E2",

    # Чекбоксы и переключатели
    "COLOR_CHECKBOX_FG": "#4A90E2",
    "COLOR_CHECKBOX_HOVER": "#3A7BC8",
    "COLOR_CHECKBOX_BORDER": "#AAAAAA",

    "COLOR_SWITCH_BG": "#E0E0E0",
    "COLOR_SWITCH_FG": "#4CAF50",
    "COLOR_SWITCH_BUTTON": "#FFFFFF",
    "COLOR_SWITCH_BUTTON_HOVER": "#F5F5F5",
    "COLOR_SWITCH_BORDER": "#B0B0B0",

    # Состояния
    "COLOR_SUCCESS": "#4CAF50",
    "COLOR_WARNING": "#FFC107",
    "COLOR_ERROR": "#F44336",
    "COLOR_INFO": "#2196F3",

    # Шрифты
    "FONT_MAIN": ("Arial", 14),
    "FONT_TITLE": ("Arial", 20, "bold"),
    "FONT_SUBTITLE": ("Arial", 16),
    "FONT_NORMAL": ("Arial", 14),
    "FONT_SMALL": ("Arial", 12),

    # Разделители
    "COLOR_DIVIDER": "#E0E0E0",

    # Тени
    "SHADOW_COLOR": "#40000000",
}

DARK_THEME = {
    # Основные цвета
    "COLOR_BG": "#2B2B2B",
    "COLOR_FRAME_BG": "#3A3A3A",
    "COLOR_ACCENT": "#5D9CEC",

    # Текст
    "COLOR_TEXT": "#FFFFFF",
    "COLOR_TEXT_SECONDARY": "#AAAAAA",
    "COLOR_TEXT_DISABLED": "#777777",

    # Кнопки
    "COLOR_BUTTON_BG": "#444444",
    "COLOR_BUTTON_HOVER": "#555555",
    "COLOR_BUTTON_ACTIVE": "#666666",
    "COLOR_BUTTON_DISABLED": "#333333",

    # Поля ввода
    "COLOR_INPUT_BG": "#333333",
    "COLOR_INPUT_BORDER": "#555555",
    "COLOR_INPUT_FOCUS": "#5D9CEC",

    # Чекбоксы и переключатели
    "COLOR_CHECKBOX_FG": "#5D9CEC",
    "COLOR_CHECKBOX_HOVER": "#4A8BD6",
    "COLOR_CHECKBOX_BORDER": "#666666",

    "COLOR_SWITCH_BG": "#444444",
    "COLOR_SWITCH_FG": "#4CAF50",
    "COLOR_SWITCH_BUTTON": "#FFFFFF",
    "COLOR_SWITCH_BUTTON_HOVER": "#EEEEEE",
    "COLOR_SWITCH_BORDER": "#666666",

    # Состояния
    "COLOR_SUCCESS": "#4CAF50",
    "COLOR_WARNING": "#FFA000",
    "COLOR_ERROR": "#F44336",
    "COLOR_INFO": "#2196F3",

    # Шрифты
    "FONT_MAIN": ("Arial", 14),
    "FONT_TITLE": ("Arial", 20, "bold"),
    "FONT_SUBTITLE": ("Arial", 16),
    "FONT_NORMAL": ("Arial", 14),
    "FONT_SMALL": ("Arial", 12),

    # Разделители
    "COLOR_DIVIDER": "#444444",

    # Тени
    "SHADOW_COLOR": "#40FFFFFF",
}

def set_theme(name: str):
    """Устанавливает текущую тему (light/dark)"""
    global CURRENT_THEME
    if name == "light":
        CURRENT_THEME.clear()
        CURRENT_THEME.update(LIGHT_THEME)
    elif name == "dark":
        CURRENT_THEME.clear()
        CURRENT_THEME.update(DARK_THEME)
    else:
        raise ValueError("Unknown theme name")

def get_color(name: str) -> str:
    """Возвращает цвет из текущей темы по имени"""
    return CURRENT_THEME.get(name, "#000000")

def get_font(name: str):
    """Возвращает шрифт из текущей темы по имени"""
    return CURRENT_THEME.get(name, ("Arial", 14))

def get_theme_colors() -> dict:
    """Возвращает все цвета текущей темы"""
    return {k: v for k, v in CURRENT_THEME.items() if k.startswith("COLOR_")}

def get_fonts() -> dict:
    """Возвращает все шрифты текущей темы"""
    return {k: v for k, v in CURRENT_THEME.items() if k.startswith("FONT_")}