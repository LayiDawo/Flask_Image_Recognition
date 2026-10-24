"""Automated tests for the Flask application's HTTP routes."""

from io import BytesIO
from PIL import Image
from unittest.mock import patch


def test_valid_image_upload(client):
    """Verify that a valid image produces the expected prediction."""

    image = Image.new("RGB", (224, 224), color="white")
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    with patch("app.predict_result", return_value=4):
        response = client.post(
            "/prediction",
            data={"file": (image_bytes, "test_image.jpg")},
            content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b">4</h2>" in response.data
    assert b"File cannot be processed" not in response.data

def test_home_page(client):
    """Verify that the Flask home page loads successfully."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hand Sign Digit Language Detection" in response.data

def test_invalid_image_upload(client):
    """Verify that invalid image data produces an error message."""

    invalid_image = BytesIO(b"this is not a valid image")

    response = client.post(
        "/prediction",
        data={"file": (invalid_image, "invalid.jpg")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data
