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

# Основная модель для корневого объекта
class Entitys(BaseModel):
    id: int
    title: str
    verified: bool
    addition: Addition
    important_numbers: List[int]

# Модель для списка сущностей (корневая структура)
class EntitysList(BaseModel):
    entity: List[Entitys]