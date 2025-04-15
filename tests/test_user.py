from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={"email": "unknown@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "Alena Kurlova",
        "email": "a.kurlowa@mail.com"
    }

    response = client.post("/api/v1/user", json=new_user)
    
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)
    
    check_response = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert check_response.status_code == 200
    assert check_response.json()["id"] == user_id

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        "name": "Gleb Ivanov",
        "email": users[0]["email"]
    }
    
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    email_to_delete = users[0]["email"]

    response = client.delete("/api/v1/user", params={"email": email_to_delete})
    assert response.status_code == 204

    check_response = client.get("/api/v1/user", params={"email": email_to_delete})
    assert check_response.status_code == 404