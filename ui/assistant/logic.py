from openai import OpenAI, RateLimitError, AuthenticationError, APIError, OpenAIError
from typing import List, Dict
import json
import os
import time
from datetime import datetime


class AssistantLogic:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)  # Новый стиль клиента
        self.model = model
        self.last_request_time = 0
        self.min_interval = 3  # Минимальный интервал между запросами (сек)

        self.conversation_history: List[Dict] = []

        self.assistant_instructions = (
            "Ты ассистент в приложении для снятия стресса. "
            "Будь дружелюбным, поддерживающим и понимающим. "
            "Помогай пользователям справляться со стрессом, предлагая техники релаксации, "
            "дыхательные упражнения и позитивные утверждения. Избегай медицинских советов."
        )

        os.makedirs("data/assistant", exist_ok=True)

    def get_response(self, user_message: str) -> str:
        now = time.time()

        # Защита от спама
        if now - self.last_request_time < self.min_interval:
            wait_time = round(self.min_interval - (now - self.last_request_time), 1)
            return f"⏳ Пожалуйста, подожди {wait_time} секунд перед следующим сообщением."

        self.last_request_time = now
        self._add_to_history("user", user_message)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.assistant_instructions},
                    *self._format_history()
                ],
                temperature=0.7
            )

            assistant_reply = response.choices[0].message.content
            self._add_to_history("assistant", assistant_reply)
            self._save_conversation()
            return assistant_reply

        except RateLimitError:
            return "🚫 Превышен лимит запросов. Подожди немного и попробуй снова."

        except AuthenticationError:
            return "🔐 Ошибка авторизации. Убедись, что API ключ правильный."

        except APIError:
            return "⚠️ Ошибка на сервере OpenAI. Попробуй позже."

        except OpenAIError as e:
            print(f"Ошибка OpenAI: {e}")
            return "❗ Ошибка при обращении к OpenAI API."

        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            return "❌ Непредвиденная ошибка. Попробуй позже."

    def _add_to_history(self, role: str, content: str):
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def _format_history(self) -> List[Dict]:
        return [
            {"role": item["role"], "content": item["content"]}
            for item in self.conversation_history[-6:]  # Последние 3 вопроса-ответа
        ]

    def _save_conversation(self):
        filename = f"data/assistant/conversation_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")
