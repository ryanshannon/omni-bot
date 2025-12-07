import pytest
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_latest_brief():
    """Test the latest brief endpoint returns placeholder content."""
    response = client.get("/brief/latest")
    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert "format" in data
    assert "generated_at" in data

    assert data["format"] == "markdown"
    assert "AI Research Brief" in data["content"]
    assert "Placeholder" in data["content"]
