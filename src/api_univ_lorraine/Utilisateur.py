import requests
from api_univ_lorraine.setup import MOBILE_URL, AUTHENTICATION_MOBILE_PATH

# classe utilisateur qui permet de recuperer l'authentification
class Utilisateur:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        url = MOBILE_URL + AUTHENTICATION_MOBILE_PATH
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_auth_token(self):
        response = self.login()
        return response['authToken']