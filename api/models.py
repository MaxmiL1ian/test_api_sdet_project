from pydantic import BaseModel
from typing import List, Optional

# Модель для вложенного объекта 'addition'
class Addition(BaseModel):
    additional_info: str
    additional_number: int

# Основная модель для корневого объекта
class Entity(BaseModel):
    addition: Addition
    id: Optional[int] = None  # ID теперь опциональный
    important_numbers: List[int]
    title: str
    verified: bool

# Модель для списка сущностей (корневая структура)
class EntityList(BaseModel):
    entity: List[Entity]
