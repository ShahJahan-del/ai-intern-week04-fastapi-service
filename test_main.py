from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model_loaded": True}

def test_predict_sentiment():
    response = client.post("/predict", json={"text": "This movie was absolutely fantastic!"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert "score" in response.json()