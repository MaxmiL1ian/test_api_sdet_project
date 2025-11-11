from api.models import Entity, Addition

def create_entity_model(
    title="Тестовая сущность", 
    verified=True, 
    important_numbers=[1, 2, 3], 
    additional_info="Тестовая информация", 
    additional_number=123,
    entity_id=None
):
    """
    Создает объект модели Entity с заданными или случайными параметрами
    
    Args:
        title (str): Название сущности, по умолчанию "Тестовая сущность"
        verified (bool): Флаг проверки, по умолчанию True
        important_numbers (list): Список важных чисел, по умолчанию [1, 2, 3]
        additional_info (str): Дополнительная информация, по умолчанию "Тестовая информация"
        additional_number (int): Дополнительное число, по умолчанию 123
        entity_id (int): ID сущности, передаётся только при обновлении
        
    Returns:
        Entity: Объект модели Entity
    """
    # Создаем объект Entity напрямую
    entity = Entity(
        addition=Addition(
            additional_info=additional_info,
            additional_number=additional_number
        ),
        important_numbers=important_numbers,
        title=title,
        verified=verified
    )
    
    # Добавляем ID только при обновлении сущности
    if entity_id is not None:
        entity.id = entity_id
    
    return entity
