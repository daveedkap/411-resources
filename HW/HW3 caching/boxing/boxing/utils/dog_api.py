import requests

DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

def get_random_dog_image() -> str:
    """Fetch a random dog image from the Dog CEO API."""
    response = requests.get(DOG_API_URL)
    response.raise_for_status()
    data = response.json()
    return data["message"]
