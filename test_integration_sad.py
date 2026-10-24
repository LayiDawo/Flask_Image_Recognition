"""Integration tests for invalid prediction requests."""


def test_missing_file(client):
    """Verify that a missing uploaded file produces an error message."""

    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
