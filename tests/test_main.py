from fastapi.testclient import TestClient
from models.db import db
from models.models import Sheep

from main import app

client = TestClient(app)

# Test to read a specific sheep
def test_read_sheep():
    response = client.get("/sheep/1")  
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe",
    }

# Test to add a new sheep to the database
def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Suffolk",
        "breed": "Suffolk",
        "sex": "ewe",
    }
    
    # Send a POST request to the endpoint a
    response = client.post("/sheep", json=new_sheep_data)
    
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201
    
    # Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep_data

    # Verify that the sheep was actually added to the database
    # by retrieving the new sheep by ID
    response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert response.status_code == 200
    assert response.json() == new_sheep_data

def test_delete_sheep():
    #  add a new sheep to delete
    new_sheep_data = {
        "id": 8,
        "name": "Remy",
        "breed": "Merino",
        "sex": "ewe",
    }
    client.post("/sheep", json=new_sheep_data)

    # Delete the newly added sheep
    response = client.delete("/sheep/8")
    assert response.status_code == 204

    # Verify it was deleted
    response = client.get("/sheep/8")
    assert response.status_code == 404


def test_update_sheep():
    # add a new sheep to update
    new_sheep_data = {
        "id": 9,
        "name": "Finn",
        "breed": "Suffolk",
        "sex": "ram",
    }
    client.post("/sheep", json=new_sheep_data)

    # Update the newly added sheep
    updated_sheep_data = {
        "id": 9,
        "name": "Finnigan",
        "breed": "Suffolk",
        "sex": "ram",
    }
    response = client.put("/sheep/9", json=updated_sheep_data)
    assert response.status_code == 200
    assert response.json() == updated_sheep_data

    # Verify the update
    response = client.get("/sheep/9")
    assert response.status_code == 200
    assert response.json() == updated_sheep_data

def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Ensure there’s at least one sheep in the list