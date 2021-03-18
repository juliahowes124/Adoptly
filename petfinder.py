import requests

from project_secrets import PETFINDER_API_KEY, PETFINDER_SECRET_KEY

from random import choice


def get_auth_token():
    resp = requests.post("https://api.petfinder.com/v2/oauth2/token",
                         data={"grant_type": "client_credentials",
                               "client_id": PETFINDER_API_KEY,
                               "client_secret": PETFINDER_SECRET_KEY})

    return resp.json()["access_token"]


def get_random_pet():
    token = get_auth_token()
    resp = requests.get("https://api.petfinder.com/v2/animals?limit=100",
                        headers={"Authorization": f"Bearer {token}"})

    random_pet = choice(resp.json()["animals"])
    print(random_pet)
    pet_to_return = {
        "name": random_pet["name"],
        "age": random_pet["age"],
        "photo_url": random_pet["primary_photo_cropped"]
    }
    return pet_to_return
