# 🛠️ Руководство по разработке Relieve Stress

## 📋 Содержание
- [Архитектура проекта](#архитектура-проекта)
- [Стандарты кодирования](#стандарты-кодирования)
- [Добавление новых функций](#добавление-новых-функций)
- [Тестирование](#тестирование)
- [Оптимизация](#оптимизация)

## 🏗️ Архитектура проекта

### Принципы архитектуры:
1. **Модульность** - каждый компонент имеет четко определенную ответственность
2. **Разделение слоев** - логика отделена от представления
3. **Расширяемость** - легко добавлять новые функции
4. **Поддерживаемость** - код легко читается и модифицируется

### Слои приложения:

#### Core Layer (Ядро)
- **models/** - Модели данных (dataclasses)
- **services/** - Бизнес-логика и сервисы
- **utils/** - Вспомогательные утилиты

#### UI Layer (Интерфейс)
- **views/** - Представления (экраны приложения)
- **widgets/** - Кастомные виджеты
- **components/** - Базовые UI компоненты
- **animations/** - Система анимаций
- **themes/** - Управление темами

#### Config Layer (Конфигурация)
- **settings.py** - Менеджер настроек
- **settings.json** - Файл конфигурации

## 📝 Стандарты кодирования

### Общие принципы:
1. **PEP 8** - следуем стандартам Python
2. **Type Hints** - используем типизацию везде где возможно
3. **Docstrings** - документируем все публичные методы
4. **Комментарии** - объясняем сложную логику

### Именование:
```python
# Классы - PascalCase
class EmotionService:
    pass

# Методы и переменные - snake_case
def get_emotion_advice(self, emotion_name: str) -> Optional[EmotionAdvice]:
    pass

# Константы - UPPER_SNAKE_CASE
_DEFAULT_COLOR = "#CCCCCC"

# Приватные методы - начинаются с _
def _init_emotions(self) -> Dict[str, Emotion]:
    pass
```

### Структура файлов:
```python
"""Краткое описание модуля.

Подробное описание функциональности модуля.
"""

# Импорты стандартных библиотек
import json
from typing import Dict, List, Optional

# Импорты сторонних библиотек
import customtkinter as ctk

# Локальные импорты
from core.models.emotion import Emotion
from ui.style import get_color


class MyClass:
    """Описание класса."""
    
    # Константы класса
    _CONSTANT_VALUE = "value"
    
    def __init__(self, param: str):
        """Инициализация класса."""
        self.param = param
    
    def public_method(self) -> str:
        """Публичный метод."""
        return self._private_method()
    
    def _private_method(self) -> str:
        """Приватный метод."""
        return self.param
```

## ➕ Добавление новых функций

### Добавление новой эмоции:

1. **Обновите EmotionService:**
```python
# В core/services/emotion_service.py
_EMOTION_COLORS = {
    # ... существующие эмоции
    "Новая эмоция": "#FF5733"
}

# В методе _init_emotions добавьте:
"Новая эмоция": Emotion(
    name="Новая эмоция",
    color=self._EMOTION_COLORS["Новая эмоция"],
    advice=["Совет 1", "Совет 2"],
    quotes=["Цитата 1"],
    actions=["Действие 1"]
)
```

2. **Обновите EmotionWheelView:**
```python
# В ui/views/emotion_wheel_view.py
_EMOTION_EMOJIS: Dict[str, str] = {
    # ... существующие эмоции
    "Новая эмоция": "😊"
}
```

### Добавление нового представления:

1. **Создайте класс представления:**
```python
# ui/views/my_new_view.py
from ui.views.base_view import BaseView

class MyNewView(BaseView):
    def setup_ui(self) -> None:
        """Настройка интерфейса."""
        # Ваш код здесь
        pass
    
    def update_theme(self) -> None:
        """Обновление темы."""
        # Ваш код здесь
        pass
```

2. **Добавьте в главное окно:**
```python
# В ui/main_window.py
def show_my_new_view(self):
    """Показывает новое представление."""
    from ui.views.my_new_view import MyNewView
    
    self.clear_content()
    self.my_new_view = MyNewView(self.content_frame)
    self.my_new_view.pack(fill="both", expand=True, padx=10, pady=10)
    self.current_view = self.my_new_view
```

### Добавление нового виджета:

```python
# ui/widgets/my_widget.py
import customtkinter as ctk
from typing import Optional, Callable
from ui.style import get_color, get_font

class MyWidget(ctk.CTkFrame):
    """Описание виджета."""
    
    def __init__(self, parent: ctk.CTkBaseClass, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Настройка интерфейса."""
        self.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=8
        )
        # Остальной код
    
    def update_theme(self) -> None:
        """Обновление темы."""
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
```

## 🧪 Тестирование

### Ручное тестирование:
1. Проверьте все основные функции
2. Протестируйте смену тем
3. Убедитесь в корректности анимаций
4. Проверьте сохранение настроек

### Тестирование производительности:
1. Мониторьте использование памяти
2. Проверьте плавность анимаций
3. Тестируйте на разных разрешениях экрана

## ⚡ Оптимизация

### Рекомендации по оптимизации:

1. **Ленивая загрузка:**
```python
# Загружайте представления только при необходимости
def show_view(self):
    if not hasattr(self, 'my_view'):
        from ui.views.my_view import MyView
        self.my_view = MyView(self.content_frame)
```

2. **Кэширование:**
```python
# Кэшируйте часто используемые данные
@property
def cached_data(self):
    if not hasattr(self, '_cached_data'):
        self._cached_data = self._load_data()
    return self._cached_data
```

3. **Оптимизация анимаций:**
```python
# Используйте разумные значения для анимаций
AnimationManager.fade_in(widget, duration=0.2)  # Не слишком долго
```

4. **Управление памятью:**
```python
# Очищайте ресурсы при необходимости
def cleanup(self):
    for widget in self.widgets:
        widget.destroy()
    self.widgets.clear()
```

### Профилирование:
```python
import cProfile
import pstats

def profile_function():
    # Ваш код для профилирования
    pass

# Запуск профилирования
cProfile.run('profile_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)
```

## 🔧 Отладка

### Логирование:
```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Использование
logger.debug("Отладочная информация")
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
```

### Обработка ошибок:
```python
def safe_method(self):
    """Метод с безопасной обработкой ошибок."""
    try:
        # Потенциально опасный код
        result = self.risky_operation()
        return result
    except SpecificException as e:
        logger.error(f"Специфическая ошибка: {e}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return None
```

## 📦 Сборка и распространение

### Создание исполняемого файла:
```bash
# Установка PyInstaller
pip install pyinstaller

# Создание exe файла
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py

# Создание с дополнительными файлами
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --add-data "config;config" main.py
```

### Создание установщика:
Используйте Inno Setup или NSIS для создания установщика Windows.

## 🤝 Вклад в проект

### Процесс разработки:
1. Создайте ветку для новой функции: `git checkout -b feature/new-feature`
2. Внесите изменения и протестируйте их
3. Зафиксируйте изменения: `git commit -m "Добавлена новая функция"`
4. Отправьте ветку: `git push origin feature/new-feature`
5. Создайте Pull Request

### Стандарты коммитов:
```
feat: добавлена новая функция
fix: исправлена ошибка
docs: обновлена документация
style: изменения в стилях (без изменения логики)
refactor: рефакторинг кода
test: добавлены тесты
chore: обновление зависимостей или конфигурации
```

---

**Удачной разработки! 🚀**