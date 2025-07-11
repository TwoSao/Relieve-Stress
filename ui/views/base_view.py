import customtkinter as ctk
from abc import ABC, abstractmethod
from ui.animations.transitions import AnimationManager

class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.animation_manager = AnimationManager()
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        pass
    
    @abstractmethod
    def update_theme(self):
        """Обновление темы виджетов"""
        pass
    
    def show_with_animation(self, animation_type: str = "fade"):
        """Показывает представление с анимацией"""
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        if animation_type == "fade":
            self.animation_manager.fade_in(self)
        elif animation_type == "slide":
            self.animation_manager.slide_in(self)
        elif animation_type == "scale":
            self.animation_manager.scale_in(self)