import requests

API_URL = "http://api:5000"


def test_add_user():
    response = requests.post(f"{API_URL}/users", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "membership_type": "student"
    })
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["membership_type"] == "student"


def test_borrow_item():
    user_response = requests.post(f"{API_URL}/users", json={
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "membership_type": "student"
    })
    user_id = user_response.json()["user_id"]

    borrow_response = requests.post(f"{API_URL}/items/1/borrow", json={
        "user_id": user_id,
        "item_type": "book"
    })
    assert borrow_response.status_code == 200
    data = borrow_response.json()
    assert data["status"] == "borrowed"
    assert data["user_id"] == user_id


def test_return_item():
    user_response = requests.post(f"{API_URL}/users", json={
        "name": "Jake Doe",
        "email": "jake.doe@example.com",
        "membership_type": "student"
    })
    user_id = user_response.json()["user_id"]

    requests.post(f"{API_URL}/items/1/borrow", json={
        "user_id": user_id,
        "item_type": "book"
    })

    return_response = requests.post(f"{API_URL}/items/1/return", json={
        "user_id": user_id
    })
    assert return_response.status_code == 200
    data = return_response.json()
    assert data["status"] == "available"


def test_user_history():
    user_response = requests.post(f"{API_URL}/users", json={
        "name": "James Doe",
        "email": "james.doe@example.com",
        "membership_type": "student"
    })
    user_id = user_response.json()["user_id"]

    requests.post(f"{API_URL}/items/1/borrow", json={
        "user_id": user_id,
        "item_type": "book"
    })
    requests.post(f"{API_URL}/items/1/return", json={
        "user_id": user_id
    })

    history_response = requests.get(f"{API_URL}/users/{user_id}/history")
    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history) > 0
    assert history[0]["item_id"] == 1
    assert history[0]["item_type"] == "book"
