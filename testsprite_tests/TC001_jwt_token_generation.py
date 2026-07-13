import requests

def test_jwt_token_generation():
    base_url = "http://localhost:8000"
    endpoint = "/api/auth/token/"
    url = base_url + endpoint
    # Replace these credentials with valid ones for the test environment
    credentials = {
        "username": "testuser",
        "password": "testpassword"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=credentials, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    response_json = response.json()
    assert "access" in response_json, "Response JSON missing 'access' token"
    assert "refresh" in response_json, "Response JSON missing 'refresh' token"

    assert isinstance(response_json["access"], str) and len(response_json["access"]) > 0, "'access' token is empty or not a string"
    assert isinstance(response_json["refresh"], str) and len(response_json["refresh"]) > 0, "'refresh' token is empty or not a string"

test_jwt_token_generation()