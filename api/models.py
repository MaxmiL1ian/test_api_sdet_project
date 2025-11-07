from pydantic import BaseModel
from typing import List

# Модель для вложенного объекта 'addition'
class Addition(BaseModel):
    additional_info: str
    additional_number: int

# Основная модель для корневого объекта
class Entity(BaseModel):
    addition: Addition
    id: int
    important_numbers: List[int]
    title: str
    verified: bool

# Модель для списка сущностей (корневая структура)
class EntityList(BaseModel):
    entity: List[Entity]