import pytest
import requests

from boxing.utils.api_utils import get_random, RANDOM_ORG_URL

RANDOM_NUMBER = 0.42

@pytest.fixture
def mock_random_org(mocker):
    # Patch requests.get to return a mock response with our desired random number.
    mock_response = mocker.Mock()
    mock_response.text = f"{RANDOM_NUMBER}"
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org):
    """Test retrieving a random number from random.org."""
    result = get_random()
    # Assert that the result is the mocked random number
    assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"
    # Ensure that the correct URL and timeout were used
    requests.get.assert_called_once_with(RANDOM_ORG_URL, timeout=5)

def test_get_random_request_failure(mocker):
    """Test handling of a request failure when calling random.org."""
    # Simulate a request failure
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))
    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

def test_get_random_timeout(mocker):
    """Test handling of a timeout when calling random.org."""
    # Simulate a timeout
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

def test_get_random_invalid_response(mock_random_org):
    """Test handling of an invalid response from random.org."""
    # Simulate an invalid response (non-numeric)
    mock_random_org.text = "invalid_response"
    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()
