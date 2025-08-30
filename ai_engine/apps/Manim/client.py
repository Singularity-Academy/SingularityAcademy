
import requests
def post_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
post_request("http://localhost:8888/generate", {"text": input("[TEST] Enter keyword >")})
    