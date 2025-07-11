"""Сервис для работы с эмоциями и советами.

Обеспечивает доступ к базе эмоций и соответствующим советам.
"""

import random
from typing import Dict, List, Optional
from core.models.emotion import Emotion, EmotionAdvice


class EmotionService:
    """Сервис для управления эмоциями и получения советов."""
    
    # Константы для цветов эмоций
    _EMOTION_COLORS = {
        "Злость": "#FF6B6B",
        "Грусть": "#4ECDC4",
        "Усталость": "#95E1D3",
        "Радость": "#FFE66D",
        "Тревога": "#A8E6CF",
        "Спокойствие": "#D4A5A5"
    }
    
    _DEFAULT_COLOR = "#CCCCCC"
    
    def __init__(self):
        """Инициализирует сервис с предопределёнными эмоциями."""
        self._emotions = self._init_emotions()
    
    def _init_emotions(self) -> Dict[str, Emotion]:
        """Создаёт словарь эмоций с соответствующими советами."""
        return {
            "Злость": Emotion(
                name="Злость",
                color=self._EMOTION_COLORS["Злость"],
                advice=["Сделайте глубокий вдох", "Посчитайте до 10", "Выйдите на свежий воздух"],
                quotes=["Гнев - это кислота, которая может причинить больше вреда сосуду, в котором хранится, чем всему, на что она вылита"],
                actions=["Сожмите и разожмите кулаки 10 раз", "Напишите о своих чувствах"]
            ),
            "Грусть": Emotion(
                name="Грусть",
                color=self._EMOTION_COLORS["Грусть"],
                advice=["Позвольте себе почувствовать эмоцию", "Поговорите с близким человеком", "Займитесь любимым делом"],
                quotes=["Слёзы - это слова, которые сердце не может произнести"],
                actions=["Послушайте спокойную музыку", "Обнимите подушку или домашнее животное"]
            ),
            "Усталость": Emotion(
                name="Усталость",
                color=self._EMOTION_COLORS["Усталость"],
                advice=["Отдохните 15 минут", "Выпейте воды", "Сделайте лёгкую растяжку"],
                quotes=["Отдых - это не награда за завершённую работу, а необходимость для продолжения"],
                actions=["Закройте глаза на 5 минут", "Сделайте 10 глубоких вдохов"]
            ),
            "Радость": Emotion(
                name="Радость",
                color=self._EMOTION_COLORS["Радость"],
                advice=["Поделитесь радостью с другими", "Запишите этот момент", "Насладитесь моментом"],
                quotes=["Счастье не в том, чтобы делать то, что хочешь, а в том, чтобы хотеть то, что делаешь"],
                actions=["Улыбнитесь своему отражению", "Позвоните близкому человеку"]
            ),
            "Тревога": Emotion(
                name="Тревога",
                color=self._EMOTION_COLORS["Тревога"],
                advice=["Сосредоточьтесь на настоящем моменте", "Используйте технику 5-4-3-2-1", "Практикуйте медитацию"],
                quotes=["Тревога - это процентная ставка, которую вы платите за занятые неприятности"],
                actions=["Назовите 5 вещей, которые видите", "Сделайте дыхательное упражнение 4-7-8"]
            ),
            "Спокойствие": Emotion(
                name="Спокойствие",
                color=self._EMOTION_COLORS["Спокойствие"],
                advice=["Сохраните это состояние", "Практикуйте благодарность", "Наслаждайтесь моментом"],
                quotes=["В спокойствии кроется сила"],
                actions=["Медитируйте 5 минут", "Запишите 3 вещи, за которые благодарны"]
            )
        }
    
    def get_emotions(self) -> List[str]:
        """Возвращает список всех доступных эмоций."""
        return list(self._emotions.keys())
    
    def get_emotion_advice(self, emotion_name: str) -> Optional[EmotionAdvice]:
        """Возвращает случайный совет для указанной эмоции."""
        emotion = self._emotions.get(emotion_name)
        if not emotion:
            return None
        
        return EmotionAdvice(
            emotion=emotion_name,
            advice=random.choice(emotion.advice),
            quote=random.choice(emotion.quotes),
            action=random.choice(emotion.actions)
        )
    
    def get_emotion_color(self, emotion_name: str) -> str:
        """Возвращает цвет для указанной эмоции."""
        return self._EMOTION_COLORS.get(emotion_name, self._DEFAULT_COLOR)