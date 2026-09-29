"""Focused tests for prediction API behavior."""

from io import BytesIO

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from app.api import routes
from app.main import app

client = TestClient(app)


class FakeModel:
    def predict(self, image: np.ndarray) -> tuple[str, float]:
        assert image.shape == (224, 224, 3)
        return "Healthy", 0.97


def test_predict_returns_classification(monkeypatch) -> None:
    monkeypatch.setattr(routes, "get_model", lambda: FakeModel())
    image_bytes = BytesIO()
    Image.new("RGB", (32, 32), color="green").save(image_bytes, format="PNG")

    response = client.post(
        "/predict", files={"file": ("leaf.png", image_bytes.getvalue(), "image/png")}
    )

    assert response.status_code == 200
    assert response.json()["predicted_class"] == "Healthy"
    assert response.json()["accepted"] is True


def test_predict_rejects_non_image(monkeypatch) -> None:
    monkeypatch.setattr(routes, "get_model", lambda: FakeModel())

    response = client.post("/predict", files={"file": ("leaf.txt", b"not an image")})

    assert response.status_code == 400


def test_health_reports_missing_model(monkeypatch) -> None:
    def unavailable_model():
        raise routes.ModelNotReadyError("model files are missing")

    monkeypatch.setattr(routes, "get_model", unavailable_model)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "degraded", "model_loaded": False}