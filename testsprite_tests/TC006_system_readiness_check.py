import requests

BASE_URL = "http://localhost:8000"


def test_system_readiness_check():
    url = f"{BASE_URL}/ready/"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    # Validate that the response is JSON and contains a readiness status indicating the system is ready
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Check for a typical readiness indicator: presence of key "ready" with truthy value or status "ok"
    # Since PRD does not specify exact response schema, check common patterns
    assert (
        ("ready" in data and data["ready"] is True)
        or ("status" in data and data["status"].lower() in ["ok", "ready", "healthy"])
    ), f"System readiness check failed. Response JSON: {data}"


test_system_readiness_check()