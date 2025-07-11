"""Менеджер анимаций для плавных переходов.

Обеспечивает различные типы анимаций для элементов интерфейса.
"""

import customtkinter as ctk
from typing import Callable, Optional, Literal
import threading
import time


class AnimationManager:
    """Менеджер для создания и управления анимациями."""
    
    # Константы для анимаций
    _DEFAULT_STEPS = 20
    _SCALE_STEPS = 15
    _MIN_STEP_TIME = 0.01  # Минимальное время шага
    
    @staticmethod
    def fade_in(widget: ctk.CTkBaseClass, duration: float = 0.3, 
                callback: Optional[Callable] = None) -> None:
        """Анимация плавного появления."""
        def animate() -> None:
            steps = AnimationManager._DEFAULT_STEPS
            step_time = max(duration / steps, AnimationManager._MIN_STEP_TIME)
            
            for i in range(steps + 1):
                if not widget.winfo_exists():
                    break
                    
                try:
                    # Простая анимация прозрачности через масштаб
                    scale = i / steps
                    widget.configure(corner_radius=max(1, int(8 * scale)))
                    time.sleep(step_time)
                except Exception:
                    break
            
            if callback:
                try:
                    callback()
                except Exception as e:
                    print(f"Ошибка в callback анимации: {e}")
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def slide_in(widget: ctk.CTkBaseClass, 
                 direction: Literal["left", "right", "up", "down"] = "left", 
                 duration: float = 0.3) -> None:
        """Анимация скольжения."""
        def animate() -> None:
            try:
                original_x = widget.winfo_x()
                original_y = widget.winfo_y()
            except Exception:
                return
            
            # Определяем начальную позицию
            offset = 100
            start_x, start_y = original_x, original_y
            
            if direction == "left":
                start_x -= offset
            elif direction == "right":
                start_x += offset
            elif direction == "up":
                start_y -= offset
            elif direction == "down":
                start_y += offset
            
            steps = AnimationManager._DEFAULT_STEPS
            step_time = max(duration / steps, AnimationManager._MIN_STEP_TIME)
            x_step = (original_x - start_x) / steps
            y_step = (original_y - start_y) / steps
            
            for i in range(steps + 1):
                if not widget.winfo_exists():
                    break
                    
                current_x = start_x + (x_step * i)
                current_y = start_y + (y_step * i)
                
                try:
                    widget.place(x=int(current_x), y=int(current_y))
                    time.sleep(step_time)
                except Exception:
                    break
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def scale_in(widget: ctk.CTkBaseClass, duration: float = 0.2, 
                 scale_from: float = 0.8, scale_to: float = 1.0) -> None:
        """Анимация масштабирования."""
        def animate() -> None:
            steps = AnimationManager._SCALE_STEPS
            step_time = max(duration / steps, AnimationManager._MIN_STEP_TIME)
            scale_diff = scale_to - scale_from
            
            for i in range(steps + 1):
                if not widget.winfo_exists():
                    break
                    
                current_scale = scale_from + (scale_diff * i / steps)
                
                try:
                    # Масштабирование через corner_radius
                    widget.configure(corner_radius=max(1, int(8 * current_scale)))
                    time.sleep(step_time)
                except Exception:
                    break
        
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def pulse(widget: ctk.CTkBaseClass, duration: float = 1.0, 
              pulses: int = 3) -> None:
        """Анимация пульсации."""
        def animate() -> None:
            pulse_duration = duration / pulses
            
            for _ in range(pulses):
                if not widget.winfo_exists():
                    break
                    
                # Увеличение
                AnimationManager.scale_in(widget, pulse_duration / 2, 1.0, 1.1)
                time.sleep(pulse_duration / 2)
                
                if not widget.winfo_exists():
                    break
                    
                # Уменьшение
                AnimationManager.scale_in(widget, pulse_duration / 2, 1.1, 1.0)
                time.sleep(pulse_duration / 2)
        
        threading.Thread(target=animate, daemon=True).start()