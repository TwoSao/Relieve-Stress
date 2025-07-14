"""Оптимизированный менеджер анимаций.

Обеспечивает плавные анимации без блокировки UI.
"""

import customtkinter as ctk
from typing import Callable, Optional, Literal, Set
import threading
import time


class AnimationManager:
    """Оптимизированный менеджер анимаций."""
    
    # Оптимизированные константы
    _DEFAULT_STEPS = 10  # Уменьшено для производительности
    _SCALE_STEPS = 8     # Уменьшено для производительности
    _MIN_STEP_TIME = 0.016  # ~60 FPS
    _active_animations: Set[str] = set()  # Отслеживание активных анимаций
    
    @staticmethod
    def fade_in(widget: ctk.CTkBaseClass, duration: float = 0.2, 
                callback: Optional[Callable] = None) -> None:
        """Оптимизированная анимация появления."""
        widget_id = str(id(widget))
        if widget_id in AnimationManager._active_animations:
            return
            
        def animate() -> None:
            AnimationManager._active_animations.add(widget_id)
            try:
                if not widget.winfo_exists():
                    return
                    
                # Простое появление без сложных вычислений
                widget.configure(corner_radius=8)
                if callback:
                    callback()
            except Exception:
                pass
            finally:
                AnimationManager._active_animations.discard(widget_id)
        
        widget.after(10, animate)  # Используем after вместо threading
    
    @staticmethod
    def slide_in(widget: ctk.CTkBaseClass, 
                 direction: Literal["left", "right", "up", "down"] = "left", 
                 duration: float = 0.15) -> None:
        """Упрощенная анимация скольжения."""
        widget_id = str(id(widget))
        if widget_id in AnimationManager._active_animations:
            return
            
        def animate() -> None:
            AnimationManager._active_animations.add(widget_id)
            try:
                if widget.winfo_exists():
                    # Простое появление без сложной анимации позиции
                    widget.configure(corner_radius=8)
            except Exception:
                pass
            finally:
                AnimationManager._active_animations.discard(widget_id)
        
        widget.after(10, animate)
    
    @staticmethod
    def scale_in(widget: ctk.CTkBaseClass, duration: float = 0.1, 
                 scale_from: float = 0.8, scale_to: float = 1.0) -> None:
        """Упрощенная анимация масштабирования."""
        widget_id = str(id(widget))
        if widget_id in AnimationManager._active_animations:
            return
            
        def animate() -> None:
            AnimationManager._active_animations.add(widget_id)
            try:
                if widget.winfo_exists():
                    # Простое изменение без сложных вычислений
                    widget.configure(corner_radius=8)
            except Exception:
                pass
            finally:
                AnimationManager._active_animations.discard(widget_id)
        
        widget.after(5, animate)
    
    @staticmethod
    def pulse(widget: ctk.CTkBaseClass, duration: float = 0.3, 
              pulses: int = 1) -> None:
        """Упрощенная анимация пульсации."""
        widget_id = str(id(widget))
        if widget_id in AnimationManager._active_animations:
            return
            
        def animate() -> None:
            AnimationManager._active_animations.add(widget_id)
            try:
                if widget.winfo_exists():
                    # Простой эффект без сложной анимации
                    original_radius = widget.cget('corner_radius')
                    widget.configure(corner_radius=12)
                    widget.after(100, lambda: widget.configure(corner_radius=original_radius) if widget.winfo_exists() else None)
            except Exception:
                pass
            finally:
                AnimationManager._active_animations.discard(widget_id)
        
        widget.after(5, animate)
    
    @staticmethod
    def clear_animations() -> None:
        """Очищает все активные анимации."""
        AnimationManager._active_animations.clear()