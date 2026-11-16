from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["service"] == "Jenkins CI/CD Pipeline Demo"
    assert "version" in body
