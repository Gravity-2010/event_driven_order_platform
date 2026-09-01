from fastapi.testclient import TestClient
from order_service.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.json() == {"status": "ok"}
    assert response.status_code == 200

def test_create_order():
    response = client.post("/orders", json = {"customer_id": 123, "items": [{"product_id": 42, "quantity": 2}]})
    assert response.status_code == 201
    assert isinstance(response.json()["order_id"], int)
    assert response.json()["customer_id"] == 123