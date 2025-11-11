from api.client import ApiClient
from api.endpoints import Entity
from api.models import Entity as EntityModel, EntityList


class EntityClient(ApiClient):
    """
    Клиент для работы с API сущностей.
    Предоставляет методы для выполнения операций CRUD с сущностями.
    """

    def create_entity(self, entity_data):
        """
        Создает новую сущность.
        
        Args:
            entity_data (EntityModel): Данные сущности для создания.
            
        Returns:
            int: ID созданной сущности.
            None: Если создание не удалось.
        """
        # Преобразуем модель в словарь
        data_dict = entity_data.model_dump() if isinstance(entity_data, EntityModel) else entity_data
        response = self.post(Entity.CREATING_ENTITY, json=data_dict)
        
        # Проверяем статус-код ответа
        if response.status_code != 200:
            return None
            
        # Возвращаем ID созданной сущности
        return response.json()
    
    def get_entity(self, entity_id):
        """
        Получает сущность по ID.
        
        Args:
            entity_id (int): ID сущности.
            
        Returns:
            EntityModel: Объект сущности, если она найдена.
            None: Если сущность не найдена.
        """
        response = self.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
        
        if response.status_code != 200:
            return None
        
        # Десериализуем ответ в модель сущности
        return EntityModel.model_validate(response.json())
    
    def get_all_entities(self):
        """
        Получает список всех сущностей.
        
        Returns:
            EntityList: Список всех сущностей.
            None: В случае ошибки.
        """
        response = self.get(Entity.GETTING_ALL_ENTITIES)
        
        if response.status_code != 200:
            return None
        
        # Десериализуем ответ в список сущностей
        return EntityList.model_validate(response.json())
    
    def update_entity(self, entity_id, entity_data):
        """
        Обновляет существующую сущность.
        
        Args:
            entity_id (int): ID сущности для обновления.
            entity_data (EntityModel): Новые данные сущности.
            
        Returns:
            bool: True, если обновление прошло успешно, иначе False.
        """
        # Преобразуем модель в словарь
        data_dict = entity_data.model_dump() if isinstance(entity_data, EntityModel) else entity_data
        response = self.patch(
            Entity.UPDATING_ENTITY.replace("{id}", str(entity_id)),
            json=data_dict
        )
        
        # Проверяем статус-код ответа
        if response.status_code != 204:
            return False
            
        return True
    
    def delete_entity(self, entity_id):
        """
        Удаляет сущность по ID.
        
        Args:
            entity_id (int): ID сущности для удаления.
            
        Returns:
            bool: True, если удаление прошло успешно, иначе False.
        """
        try:
            response = self.delete(Entity.DELETING_ENTITY.replace("{id}", str(entity_id)))
            
            # Проверяем статус-код ответа
            if response.status_code != 204:
                print(f"Предупреждение: не удалось удалить сущность с ID {entity_id}")
                return False
                
            return True
        except Exception as e:
            print(f"Ошибка при удалении сущности: {str(e)}")
            return False
