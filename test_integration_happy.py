"""Integration tests for successful image prediction."""

from pathlib import Path


def test_successful_prediction(client):
    """Verify that a valid image produces a prediction through Flask."""

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
