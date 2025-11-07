from api.endpoints import Entity
from api.models import Entity as EntityModel  

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