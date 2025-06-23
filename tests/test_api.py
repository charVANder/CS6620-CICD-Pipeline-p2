import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.api import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

## GET tests
def test_check_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["Status"] == "healthy"

def test_get_all_pkmn(client):
    response = client.get("/pokemon")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "pokemon" in data
    assert "count" in data
    assert data["count"] >= 3 # should be the initial sample pokemon data

def test_get_pokemon_by_id(client): # will grab 1st pkmn from the sample data set
    response = client.get("/pokemon")
    pokemon_list = json.loads(response.data)["pokemon"]
    assert len(pokemon_list) >= 1
    pokemon_id = pokemon_list[0]["id"]
    response = client.get(f'/pokemon/{pokemon_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == pokemon_id
    assert "name" in data
    assert "hp" in data

def test_get_nonexisting_pokemon(client):
    response = client.get("/pokemon/123456789")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "Error" in data


## POST tests
def test_create_pokemon(client):
    new_pkmn = {
        "name": "Squirtle",
        "level": 10,
        "type": "Water"
    }
    response = client.post('/pokemon', data=json.dumps(new_pkmn), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data
    assert data["name"] == "Squirtle"
    assert data["level"] == 10
    assert data["type"] == "Water"

def test_create_pokemon_missing_data(client):
    pkmn_missing_data = {"level": 3}
    response = client.post('/pokemon', data=json.dumps(pkmn_missing_data), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Error" in data

def test_create_pokemon_invalid_data(client):
    invalid_pkmn = {"name": "INVALID", "level": 1000} # 1000 is too high
    response = client.post('/pokemon', data=json.dumps(invalid_pkmn), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Error" in data

def test_create_pokemon_not_json(client):
    response = client.post('/pokemon', data="not a json")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Error" in data


## PUT tests
def test_update_pokemon(client):
    created_pkmn = {
        "name": "Eevee",
        "level": 25,
        "type": "Normal"
    }
    created_response = client.post('/pokemon', data=json.dumps(created_pkmn), content_type='application/json')
    assert created_response.status_code == 201
    pokemon_id = json.loads(created_response.data)["id"]

    updated_data = {
        "name": "Eevee UPDATED",
        "level": 30
    }
    response = client.put(f'/pokemon/{pokemon_id}', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Eevee UPDATED"
    assert data["level"] == 30

def test_update_nonexisting_pokemon(client):
    updated_data = {
        "name": "MISSINGNO",
        "level": 1
    }
    response = client.put(f'/pokemon/123456789', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "Error" in data


## DELETE tests
def test_delete_pokemon(client):
    created_pkmn = {
        "name": "Venasaur",
        "level": 36
    }
    created_response = client.post('/pokemon', data=json.dumps(created_pkmn), content_type='application/json')
    assert created_response.status_code == 201
    pokemon_id = json.loads(created_response.data)["id"]

    response = client.delete(f"/pokemon/{pokemon_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Note" in data

    # Making sure that it's really gone...
    get_response = client.get(f'/pokemon/{pokemon_id}')
    assert get_response.status_code == 404

def test_delete_nonexisting_pokemon(client):
    response = client.delete(f"/pokemon/123456789")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "Error" in data


## Tests for the battle functionality (why did I do this???)
def test_pokemon_attack(client):
    # Using one of the sample Pokemon
    response = client.get('/pokemon')
    pokemon_list = json.loads(response.data)["pokemon"]
    
    assert len(pokemon_list) >= 1
    pokemon_id = pokemon_list[0]["id"] # I think this is Pikachu
    
    attack_data = {"attack_name": "Thunderbolt", "damage": 75}
    response = client.post(f'/pokemon/{pokemon_id}/attack', data=json.dumps(attack_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Thunderbolt" in data["Note"]
    assert "pokemon" in data

def test_pokemon_take_damage(client):
    created_data = {"name": "DamageTest", "level": 10}
    created_response = client.post('/pokemon', data=json.dumps(created_data), content_type='application/json')
    pokemon_id = json.loads(created_response.data)["id"]
    original_hp = json.loads(created_response.data)["hp"]
    
    damage_data = {"amount": 25}
    response = client.post(f'/pokemon/{pokemon_id}/damage', data=json.dumps(damage_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["pokemon"]["hp"] < original_hp
    assert "took" in data["Note"] and "damage" in data["Note"]

def test_pokemon_heal(client):
    created_data = {"name": "HealTest", "level": 10}
    created_response = client.post('/pokemon', data=json.dumps(created_data), content_type='application/json')
    pokemon_id = json.loads(created_response.data)["id"]
    
    damage_data = {"amount": 30}
    client.post(f'/pokemon/{pokemon_id}/damage', data=json.dumps(damage_data), content_type='application/json')
    
    heal_data = {"amount": 15}
    response = client.post(f'/pokemon/{pokemon_id}/heal', data=json.dumps(heal_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "healed" in data["Note"]