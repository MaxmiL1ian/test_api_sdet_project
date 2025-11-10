import random
from api.models import Entity, Addition

def create_entity_model(
    title=None, 
    verified=None, 
    important_numbers=None, 
    additional_info=None, 
    additional_number=None,
    entity_id=None
):
    """
    Создает объект модели Entity с заданными или случайными параметрами
    
    Args:
        title (str, optional): Название сущности
        verified (bool, optional): Флаг проверки
        important_numbers (list, optional): Список важных чисел
        additional_info (str, optional): Дополнительная информация
        additional_number (int, optional): Дополнительное число
        entity_id (int, optional): ID сущности, передаётся только при обновлении
        
    Returns:
        Entity: Объект модели Entity
    """
    # Используем переданные значения или значения по умолчанию
    entity_title = title if title is not None else "Тестовая сущность"
    entity_verified = verified if verified is not None else True
    entity_important_numbers = important_numbers if important_numbers is not None else [1, 2, 3]
    entity_additional_info = additional_info if additional_info is not None else "Тестовая информация"
    entity_additional_number = additional_number if additional_number is not None else random.randint(100, 999)
    
    # Создаем объект Addition для вложенной структуры
    addition = Addition(
        additional_info=entity_additional_info,
        additional_number=entity_additional_number
    )
    
    # Параметры для создания Entity
    entity_params = {
        "addition": addition,
        "important_numbers": entity_important_numbers,
        "title": entity_title,
        "verified": entity_verified,
    }
    
    # Добавляем ID только при обновлении сущности
    # При создании ID присваивается на сервере
    if entity_id is not None:
        entity_params["id"] = entity_id
    
    # Создаем объект Entity
    return Entity(**entity_params)
