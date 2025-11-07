from api.endpoints import Entity
from api.models import Entity as EntityModel, EntityList  
import time

class TestEntityOperations: 
    def test_get_entity(self, api_client, test_entity):
        entity_id = test_entity["id"]
        
        response = api_client.get(Entity.GETTING_ENTITY.replace("{id}", str(entity_id)))
        

        assert response.status_code == 200
        

        entity = EntityModel.model_validate(response.json())

        assert entity.id == entity_id
        assert entity.title == test_entity["original_data"]["title"]
        assert entity.verified == test_entity["original_data"]["verified"]
        assert entity.addition.additional_info == test_entity["original_data"]["addition"]["additional_info"]
        assert entity.addition.additional_number == test_entity["original_data"]["addition"]["additional_number"]
        assert entity.important_numbers == test_entity["original_data"]["important_numbers"]

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
