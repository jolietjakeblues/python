import requests

def test_request():
    try:
        response = requests.get('https://httpbin.org/get')
        response.raise_for_status()
        print("Request successful!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_request()
