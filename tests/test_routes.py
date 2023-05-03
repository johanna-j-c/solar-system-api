def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [] 

def test_get_one_planet(client, one_planet):
    response = client.get(f"/planets/{one_planet.id}")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == one_planet.id
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["radius"] == one_planet.radius

def test_get_planet_with_no_data(client):
    response = client.get(f"/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404

def test_get_all_planets_with_valid_data(client, multiple_planets):
    response = client.get(f"/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["id"] == multiple_planets[0].id
    assert response_body[0]["name"] == multiple_planets[0].name
    assert response_body[0]["description"] == multiple_planets[0].description
    assert response_body[0]["radius"] == multiple_planets[0].radius
    assert response_body[1]["id"] == multiple_planets[1].id
    assert response_body[1]["name"] == multiple_planets[1].name
    assert response_body[1]["description"] == multiple_planets[1].description
    assert response_body[1]["radius"] == multiple_planets[1].radius

def test_create_one_planet(client):
    response = client.post("/planets", json={
        "name": "Yoshi",
        "description": "Adorable and egg filled planet.",
        "radius": "7,156.9 mi"
    })

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Planet Yoshi successfully created."
