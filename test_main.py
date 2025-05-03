import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в API для расчета BMI"}


def test_calculate_bmi():
    """Тест расчета BMI"""
    # Нормальный запрос
    response = client.post("/calculate_bmi", json={"height": 180, "weight": 70})
    assert response.status_code == 200
    data = response.json()
    assert "bmi" in data
    assert data["bmi"] == 21.6  # 70 / (1.8^2) = 21.6
    assert data["category"] == "Нормальная масса тела"
    assert data["height"] == 180
    assert data["weight"] == 70

    # Проверка граничных значений роста
    response = client.post("/calculate_bmi", json={"height": 49, "weight": 70})
    assert response.status_code == 422

    response = client.post("/calculate_bmi", json={"height": 301, "weight": 70})
    assert response.status_code == 422

    # Проверка граничных значений веса
    response = client.post("/calculate_bmi", json={"height": 180, "weight": 1})
    assert response.status_code == 422

    response = client.post("/calculate_bmi", json={"height": 180, "weight": 701})
    assert response.status_code == 422

    # Проверка неверных типов данных
    response = client.post("/calculate_bmi", json={"height": "рост", "weight": 70})
    assert response.status_code == 422

    response = client.post("/calculate_bmi", json={"height": 180, "weight": "вес"})
    assert response.status_code == 422


def test_user_management():
    """Тест управления пользователями"""
    # Создание пользователя
    user_data = {
        "name": "Иван Иванов",
        "age": 30,
        "gender": "мужской",
        "bmi_data": {
            "bmi": 22.5,
            "category": "Нормальная масса тела",
            "height": 175,
            "weight": 69
        }
    }

    response = client.post("/users/user1", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь user1 создан успешно"}

    # Получение пользователя
    response = client.get("/users/user1")
    assert response.status_code == 200
    assert response.json()["name"] == "Иван Иванов"

    # Повторное создание того же пользователя
    response = client.post("/users/user1", json=user_data)
    assert response.status_code == 400

    # Получение несуществующего пользователя
    response = client.get("/users/nonexistent")
    assert response.status_code == 404
