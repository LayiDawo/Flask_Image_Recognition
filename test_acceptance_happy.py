# test_acceptance_happy.py

from io import BytesIO
import pytest

def test_acceptance_successful_upload(client):
    """Verify that a real hand-sign image produces a prediction."""

    from pathlib import Path

    image_path = (
        Path(__file__).parent
        / "test_images"
        / "4"
        / "Sign 4 (92).jpeg"
    )

    with image_path.open("rb") as image_file:
        response = client.post(
            "/prediction",
            data={"file": (image_file, "sign_4.jpeg")},
            content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"File cannot be processed." not in response.data



def test_acceptance_valid_large_image(client):
    """Verify that a large valid image can be processed successfully."""
    from io import BytesIO
    from PIL import Image
    from unittest.mock import patch

    image = Image.new("RGB", (1200, 1200), color="white")
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    with patch("app.predict_result", return_value=4):
        response = client.post(
            "/prediction",
            data={"file": (image_bytes, "large_image.jpg")},
            content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert b">4</h2>" in response.data
    assert b"File cannot be processed." not in response.data


def test_acceptance_valid_image_size_upload(client):
    """Verify that images with unusual dimensions are resized and processed."""
    from io import BytesIO
    from PIL import Image
    from unittest.mock import patch

    image = Image.new("RGB", (640, 480), color="white")
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    with patch("app.predict_result", return_value=5):
        response = client.post(
            "/prediction",
            data={"file": (image_bytes, "different_size.jpg")},
            content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert b">5</h2>" in response.data
    assert b"File cannot be processed." not in response.data
