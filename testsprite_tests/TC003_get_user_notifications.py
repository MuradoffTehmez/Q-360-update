import requests

BASE_URL = "http://localhost:8000"
AUTH_TOKEN_ENDPOINT = "/api/auth/token/"
NOTIFICATIONS_ENDPOINT = "/api/notifications/"
TIMEOUT = 30

USERNAME = "testuser"
PASSWORD = "testpassword"


def test_get_user_notifications():
    try:
        # Obtain JWT tokens first
        auth_resp = requests.post(
            BASE_URL + AUTH_TOKEN_ENDPOINT,
            json={"username": USERNAME, "password": PASSWORD},
            timeout=TIMEOUT,
        )
        assert auth_resp.status_code == 200, f"Auth token request failed: {auth_resp.text}"
        auth_data = auth_resp.json()
        access_token = auth_data.get("access")
        assert access_token is not None, "No access token received"

        # Use the access token to get notifications
        headers = {"Authorization": f"Bearer {access_token}"}
        notif_resp = requests.get(BASE_URL + NOTIFICATIONS_ENDPOINT, headers=headers, timeout=TIMEOUT)
        assert notif_resp.status_code == 200, f"Failed to get notifications: {notif_resp.text}"
        notifications = notif_resp.json()
        assert isinstance(notifications, list), "Notifications response should be a list"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"


test_get_user_notifications()
