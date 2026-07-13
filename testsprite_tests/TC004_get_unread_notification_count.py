import requests

BASE_URL = "http://localhost:8000"
AUTH_TOKEN_ENDPOINT = "/api/auth/token/"
UNREAD_COUNT_ENDPOINT = "/api/unread-count/"
TIMEOUT = 30

def test_get_unread_notification_count():
    # Replace these credentials with valid test user credentials
    username = "testuser"
    password = "testpassword"

    # Step 1: Obtain JWT access token
    auth_url = BASE_URL + AUTH_TOKEN_ENDPOINT
    auth_payload = {"username": username, "password": password}
    try:
        auth_response = requests.post(auth_url, json=auth_payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Authentication request failed: {e}"
    assert auth_response.status_code == 200, f"Authentication failed with status {auth_response.status_code}"
    auth_data = auth_response.json()
    assert "access" in auth_data and isinstance(auth_data["access"], str), "Access token not found in auth response"

    access_token = auth_data["access"]

    # Step 2: Call the unread-count endpoint with Authorization header
    unread_count_url = BASE_URL + UNREAD_COUNT_ENDPOINT
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(unread_count_url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to /api/unread-count/ failed: {e}"

    # Step 3: Validate response
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, dict), "Response is not a JSON object"
    assert "unread_count" in response_json, "Response JSON does not contain 'unread_count'"
    assert isinstance(response_json["unread_count"], int), "'unread_count' is not an integer"
    assert response_json["unread_count"] >= 0, "'unread_count' should be zero or positive integer"

test_get_unread_notification_count()