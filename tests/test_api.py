from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model_ready"] is True


def test_prediction_endpoint() -> None:
    response = client.post("/api/v1/predict", json={"features": [1.2, 3.4, 5.6]})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["model"] == "knn"
    assert body["data"]["prediction"] == "class_1"
    assert body["data"]["k_neighbors"] == 5


def test_invalid_feature_count() -> None:
    response = client.post("/api/v1/predict", json={"features": [1.0, 2.0]})
    assert response.status_code == 422
