# test_acceptance_edge_cases.py

from io import BytesIO
import pytest
from threading import Thread

# Helper function for concurrent image uploads
def upload_image(client, img_data):
    """
    Helper function to upload an image within a thread.
    - Purpose: Enables concurrent uploads for testing multithreaded scenarios.
    - Usage: Called in separate threads during concurrent tests.
    """
    client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

# 1. Edge Case: Uploading a Large Image File
def test_edge_case_large_image_upload(client):
    """
    Test uploading a large image to see how the system handles large file sizes.
    - Scenario: Simulates a file upload with a large image (e.g., 10 MB).
    - Expected Behavior: System should handle the file and return a valid prediction response.
    """
    large_img_data = BytesIO(b"large_image_data" * 10**6)  # Simulating a large image
    large_img_data.name = "large_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (large_img_data, large_img_data.name)},
        content_type="multipart/form-data"
    )

    # Assert that the system can process large image files
    assert b"Prediction" in response.data  # Adjust based on actual prediction content

# 2. Edge Case: Uploading an Image with Missing or Incorrect Metadata
def test_edge_case_invalid_metadata(client):
    """
    Test uploading an image with missing or incorrect metadata.
    - Scenario: Upload an image without any metadata or with invalid metadata.
    - Expected Behavior: System processes the image regardless of metadata issues.
    """
    img_data = BytesIO(b"image_with_no_metadata")
    img_data.name = "image_no_metadata.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    # Assert that the system processes the image even without metadata
    assert b"Prediction" in response.data  # Adjust based on actual behavior

# 3. Edge Case: Uploading an Image with Non-Standard File Extensions

def test_edge_case_non_standard_image_extensions(client):
    """Verify that a valid WebP image can be uploaded and processed."""
    from io import BytesIO
    from unittest.mock import patch
    from PIL import Image

    image = Image.new("RGB", (224, 224), color="white")
    image_bytes = BytesIO()
    image.save(image_bytes, format="WEBP")
    image_bytes.seek(0)

    with patch("app.predict_result", return_value=4):
        response = client.post(
            "/prediction",
            data={"file": (image_bytes, "test_image.webp")},
            content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert b">4</h2>" in response.data
    assert b"File cannot be processed." not in response.data

# 4. Edge Case: Uploading a Sequence of Images for Multi-Step Processing
def test_edge_case_sequential_image_uploads(client):
    """
    Test uploading a sequence of images that trigger multi-step processing.
    - Scenario: Simulate sequential uploads of multiple images.
    - Expected Behavior: Each upload should trigger a separate valid prediction response.
    """
    img_data1 = BytesIO(b"first_image_data")
    img_data1.name = "first_image.jpg"

    img_data2 = BytesIO(b"second_image_data")
    img_data2.name = "second_image.jpg"

    # First upload
    response1 = client.post(
        "/prediction",
        data={"file": (img_data1, img_data1.name)},
        content_type="multipart/form-data"
    )

    # Second upload
    response2 = client.post(
        "/prediction",
        data={"file": (img_data2, img_data2.name)},
        content_type="multipart/form-data"
    )

    # Ensure that each upload processed correctly
    assert b"Prediction" in response1.data
    assert b"Prediction" in response2.data

# 5. Edge Case: Uploading with Unexpected Headers
def test_edge_case_unexpected_headers(client):
    """
    Test uploading an image with unexpected headers.
    - Scenario: Simulate sending headers not expected by the system.
    - Expected Behavior: System should still process the file without errors.
    """
    img_data = BytesIO(b"valid_image_data")
    img_data.name = "unexpected_headers_image.jpg"

    # Simulate uploading with unexpected headers
    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data",
        headers={"X-Unexpected-Header": "value"}
    )

    # Assert that the upload is still processed correctly despite the unexpected header
    assert b"Prediction" in response.data

# 6. Edge Case: Uploading an Image with HTTP/2

def test_edge_case_text_file_upload(client):
    """Verify that uploading a text file returns an error message."""
    from io import BytesIO

    text_file = BytesIO(b"This is a text file, not an image.")

    response = client.post(
        "/prediction",
        data={"file": (text_file, "notes.txt")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
