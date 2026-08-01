from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "document_path" in data
    assert data["version"] == "0.1.0"
