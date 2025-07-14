"""Менеджер настроек приложения.

Обеспечивает сохранение и загрузку пользовательских настроек.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class AppSettings:
    """Класс для хранения настроек приложения."""
    theme: str = "light"                    # Тема оформления
    window_width: int = 900                 # Ширина окна
    window_height: int = 650                # Высота окна
    animations_enabled: bool = False        # Отключены для производительности
    auto_save: bool = True                  # Автосохранение
    groq_api_key: str = ""                  # API ключ Groq для AI ассистента
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует настройки в словарь."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppSettings':
        """Создаёт объект настроек из словаря."""
        # Фильтруем только существующие поля
        valid_fields = {k: v for k, v in data.items() if hasattr(cls, k)}
        return cls(**valid_fields)


class SettingsManager:
    """Менеджер для управления настройками приложения."""
    
    def __init__(self, config_file: str = "config/settings.json"):
        """Инициализирует менеджер настроек."""
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)
        self.settings = AppSettings()
        self._save_pending = False  # Оптимизация: отложенное сохранение
        self.load_settings()
    
    def load_settings(self) -> None:
        """Загружает настройки из файла."""
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.settings = AppSettings.from_dict(data)
        except (json.JSONDecodeError, TypeError, FileNotFoundError) as e:
            print(f"Ошибка загрузки настроек: {e}")
            self.settings = AppSettings()
    
    def save_settings(self) -> None:
        """Сохраняет настройки в файл."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings.to_dict(), f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получает значение настройки."""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Оптимизированное установка значения настройки."""
        if hasattr(self.settings, key):
            old_value = getattr(self.settings, key)
            if old_value != value:  # Сохраняем только при изменении
                setattr(self.settings, key, value)
                self._delayed_save()
        else:
            print(f"Неизвестная настройка: {key}")
    
    def _delayed_save(self) -> None:
        """Отложенное сохранение для производительности."""
        if not self._save_pending:
            self._save_pending = True
            # Отлагаем сохранение на 500мс для батчинга
            import threading
            threading.Timer(0.5, self._perform_save).start()
    
    def _perform_save(self) -> None:
        """Выполняет фактическое сохранение."""
        self._save_pending = False
        self.save_settings()
    
    def reset_to_defaults(self) -> None:
        """Сбрасывает настройки к значениям по умолчанию."""
        self.settings = AppSettings()
        self.save_settings()
    
    def force_save(self) -> None:
        """Принудительное сохранение (например, при выходе)."""
        if self._save_pending:
            self._perform_save()
        else:
            self.save_settings()