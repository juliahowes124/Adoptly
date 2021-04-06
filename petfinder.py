import requests

from project_secrets import PETFINDER_API_KEY, PETFINDER_SECRET_KEY
from random import sample

def get_auth_token():
    resp = requests.post("https://api.petfinder.com/v2/oauth2/token",
                         data={"grant_type": "client_credentials",
                               "client_id": PETFINDER_API_KEY,
                               "client_secret": PETFINDER_SECRET_KEY})

    return resp.json()["access_token"]


def get_petfinder_pets():
    token = get_auth_token()
    resp = requests.get("https://api.petfinder.com/v2/animals?limit=100",
                        headers={"Authorization": f"Bearer {token}"})

    pets = sample(resp.json()["animals"], 5)
    pets_to_return = []
    for pet in pets:
        if pet["photos"]:
            photo_url = pet["photos"][0]["full"]
        else:
            photo_url = "https://winaero.com/blog/wp-content/uploads/2015/05/windows-10-user-account-login-icon.png"
        pets_to_return.append({
            "name": pet["name"],
            "age": pet["age"],
            "photo_url": photo_url
        })
    return pets_to_return
    
