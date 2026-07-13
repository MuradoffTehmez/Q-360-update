import requests

BASE_URL = "http://localhost:8000"
TOKEN_URL = f"{BASE_URL}/api/auth/token/"
TOKEN_REFRESH_URL = f"{BASE_URL}/api/auth/token/refresh/"
TIMEOUT = 30

# Use example valid credentials; replace with actual valid test credentials as needed
VALID_USERNAME = "testuser"
VALID_PASSWORD = "testpassword"


def test_jwt_token_refresh():
    try:
        # Step 1: Obtain initial JWT tokens via /api/auth/token/
        auth_payload = {
            "username": VALID_USERNAME,
            "password": VALID_PASSWORD
        }
        auth_response = requests.post(TOKEN_URL, json=auth_payload, timeout=TIMEOUT)
        assert auth_response.status_code == 200, f"Token generation failed: {auth_response.text}"
        auth_data = auth_response.json()
        assert "access" in auth_data, "No access token in response"
        assert "refresh" in auth_data, "No refresh token in response"
        refresh_token = auth_data["refresh"]

        # Step 2: Use the refresh token to get a new access token
        refresh_payload = {
            "refresh": refresh_token
        }
        refresh_response = requests.post(TOKEN_REFRESH_URL, json=refresh_payload, timeout=TIMEOUT)
        assert refresh_response.status_code == 200, f"Token refresh failed: {refresh_response.text}"
        refresh_data = refresh_response.json()
        assert "access" in refresh_data, "No new access token returned"
        new_access_token = refresh_data["access"]
        assert isinstance(new_access_token, str) and len(new_access_token) > 0, "Invalid new access token"

    except requests.exceptions.RequestException as e:
        assert False, f"Request failed: {e}"


test_jwt_token_refresh()