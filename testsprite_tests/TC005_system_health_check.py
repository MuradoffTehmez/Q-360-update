import requests

BASE_URL = "http://localhost:8000"

def test_system_health_check():
    url = f"{BASE_URL}/health/"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request to /health/ endpoint failed: {e}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response from /health/ is not valid JSON"

    assert isinstance(data, dict), "Response JSON should be an object"

    # Expected keys in health response for database and cache connectivity
    expected_keys = ["database", "cache"]

    for key in expected_keys:
        assert key in data, f"Health response missing expected key: '{key}'"

    # Check that database and cache statuses are reported as healthy (e.g., True or "ok")
    # Assuming that each key's value is a boolean or a string indicating status
    for key in expected_keys:
        value = data[key]
        if isinstance(value, bool):
            assert value is True, f"'{key}' health status expected True but got {value}"
        elif isinstance(value, str):
            assert value.lower() in ("ok", "healthy", "true"), f"'{key}' health status expected 'ok' or similar but got '{value}'"
        else:
            assert False, f"'{key}' health status has unexpected type: {type(value)}"

test_system_health_check()