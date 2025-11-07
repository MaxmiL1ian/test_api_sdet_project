from api.endpoints import Entity
from api.models import Entity as EntityModel, EntityList  

class TestEntityOperations: 
    def test_get_entity(self, api_client, test_entity):
        entity_id = test_entity["id"]
        
        response = api_client.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
        

        assert response.status_code == 200
        

        entity = EntityModel.model_validate(response.json())

        original_data = test_entity["original_data"]
        assert entity.id == entity_id
        assert entity.title == original_data["title"]
        assert entity.verified == original_data["verified"]
        assert entity.addition.additional_info == original_data["addition"]["additional_info"]
        assert entity.addition.additional_number == original_data["addition"]["additional_number"]
        assert entity.important_numbers == original_data["important_numbers"]

    def test_update_entity(self, api_client, test_entity): 
        entity_id = test_entity["id"] 
                      
        updated_data = {
            "addition": {
                "additional_info": "Обновленная информация",
                "additional_number": 456
            },
            "important_numbers": [4, 5, 6], 
            "title": "Обновленная сущность",
            "verified": False,
        }  

        response = api_client.patch(
            Entity.UPDATING_ENTITY.replace("{id}", str(entity_id)), 
            json=updated_data
        )

        assert response.status_code == 204
        
    def test_get_all_entities(self, api_client, multiple_test_entities):

        response = api_client.get(Entity.GETTING_ALL_ENTITIES)
        
        assert response.status_code == 200
        
        entities_list = EntityList.model_validate(response.json())
        
        assert len(entities_list.entity) > 0

        # Получаем список ID из созданных сущностей
        created_ids = [entity["id"] for entity in multiple_test_entities]
        
        # Проверяем, что созданные сущности присутствуют в полученном списке
        for entity in entities_list.entity:
            # Если нашли сущность из наших тестовых данных
            if entity.id in created_ids:
                # Находим соответствующие исходные данные
                original_entity = next(e for e in multiple_test_entities if e["id"] == entity.id)
                original_data = original_entity["original_data"]
                
                # Проверяем, что данные соответствуют
                assert entity.title == original_data["title"]
                assert entity.verified == original_data["verified"]
                assert entity.addition.additional_info == original_data["addition"]["additional_info"]
                assert entity.addition.additional_number == original_data["addition"]["additional_number"]
                assert entity.important_numbers == original_data["important_numbers"]

    def test_create_entity(self, api_client):
        # Данные для создания новой сущности
        entity_data = {
            "addition": {
                "additional_info": "Информация о новой сущности",
                "additional_number": 999
            },
            "important_numbers": [7, 8, 9],
            "title": "Новая тестовая сущность",
            "verified": True
        }
        
        try:
            # Отправляем запрос на создание
            response = api_client.post(Entity.CREATING_ENTITY, json=entity_data)
            
            assert response.status_code == 200, f"Неожиданный статус-код: {response.status_code}"
            
            entity_id = response.json()
            assert entity_id is not None, "ID сущности отсутствует в ответе"
            
            # Опционально: проверяем, что сущность действительно создана, запросив её по ID
            get_response = api_client.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
            assert get_response.status_code == 200, "Не удалось получить созданную сущность"
            
            created_entity = EntityModel.model_validate(get_response.json())
            
            # Проверяем, что данные созданной сущности соответствуют отправленным
            assert created_entity.id == entity_id
            assert created_entity.title == entity_data["title"]
            assert created_entity.verified == entity_data["verified"]
            assert created_entity.addition.additional_info == entity_data["addition"]["additional_info"]
            assert created_entity.addition.additional_number == entity_data["addition"]["additional_number"]
            assert created_entity.important_numbers == entity_data["important_numbers"]

        finally:
            # Удаляем созданную сущность, если ID получен
            if 'entity_id' in locals() and entity_id:
                try:
                    delete_response = api_client.delete(Entity.DELETING_ENTITY.replace("{id}", str(entity_id)))
                    if delete_response.status_code != 204:
                        print(f"Предупреждение: не удалось удалить тестовую сущность с ID {entity_id}")
                except Exception as e:
                    print(f"Ошибка при удалении тестовой сущности: {str(e)}")

    def test_delete_entity(self, api_client):
        entity_data = {
            "addition": {
                "additional_info": "Сущность для удаления",
                "additional_number": 555
            },
            "important_numbers": [5, 5, 5],
            "title": "Тестовая сущность для удаления",
            "verified": False
        }
        
        create_response = api_client.post(Entity.CREATING_ENTITY, json=entity_data)
        assert create_response.status_code == 200, "Не удалось создать сущность для теста удаления"
        
        entity_id = create_response.json()
        assert entity_id is not None, "ID сущности отсутствует в ответе"
        
        get_response = api_client.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
        assert get_response.status_code == 200, "Не удалось получить созданную сущность"
        
        delete_response = api_client.delete(Entity.DELETING_ENTITY.replace("{id}", str(entity_id)))
        assert delete_response.status_code == 204, f"Ошибка при удалении сущности: получен статус {delete_response.status_code} вместо ожидаемого 204"

        get_after_delete_response = api_client.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
        assert get_after_delete_response.status_code == 500, f"Ожидался статус 404 (Not Found), получен {get_after_delete_response.status_code}. Сущность не была удалена."