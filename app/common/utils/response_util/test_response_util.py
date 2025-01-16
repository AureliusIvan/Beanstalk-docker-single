import pytest
from fastapi.testclient import TestClient
from .response_util import create_error_response
import logging


# Setup the test client
@pytest.fixture
def client():
    from fastapi import FastAPI
    app = FastAPI()

    # Create an endpoint to test the error response
    @app.get("/test_error")
    async def test_error():
        status_code = 500
        message = "Internal Server Error"
        return create_error_response(status_code, message)

    return TestClient(app)


def test_create_error_response(client):
    # Call the endpoint that uses the create_error_response function
    response = client.get("/test_error")

    # Check if the status code is as expected
    assert response.status_code == 500

    # Check if the content matches the expected format
    content = response.json()
    assert content["code"] == 500
    assert content["message"] == "Internal Server Error"

    # Check if the log contains the expected error message
    with pytest.raises(Exception):
        logger = logging.getLogger("your_module")
        # Capture the logs
        with pytest.capture_logs() as captured:
            # Call the function again to trigger the error logging
            client.get("/test_error")

        # Check if the error is logged properly
        assert "Error: Internal Server Error" in captured.text
        assert "Traceback" in captured.text
