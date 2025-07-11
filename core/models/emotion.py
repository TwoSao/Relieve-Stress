"""Модели данных для эмоций и советов.

Определяет структуры данных для эмоций и соответствующих советов.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EmotionAdvice:
    """Класс для хранения совета по эмоции."""
    emotion: str      # Название эмоции
    advice: str       # Совет по работе с эмоцией
    quote: str        # Мотивирующая цитата
    action: str       # Конкретное действие


@dataclass(frozen=True)
class Emotion:
    """Класс для определения эмоции с её характеристиками."""
    name: str                # Название эмоции
    color: str               # Цвет для отображения
    advice: List[str]        # Список советов
    quotes: List[str]        # Список цитат
    actions: List[str]       # Список действий