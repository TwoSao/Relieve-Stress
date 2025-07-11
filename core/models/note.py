from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Note:
    id: str
    text: str
    category: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_favorite: bool = False
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_favorite': self.is_favorite
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        return cls(
            id=data['id'],
            text=data['text'],
            category=data['category'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            is_favorite=data.get('is_favorite', False)
        )