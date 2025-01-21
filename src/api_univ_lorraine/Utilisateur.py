import re
import requests
import os
import sys
import aiohttp
from api_univ_lorraine import MOBILE_URL, AUTHENTICATION_MOBILE_PATH


CAS_LOGIN_URL = 'https://auth.univ-lorraine.fr/login'
CAS_SERVICE_VALIDATE_URL = 'https://auth.univ-lorraine.fr/serviceValidate'

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

    async def get_ticket(self, service):
        url = f"{CAS_LOGIN_URL}?service={service}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                execution_regex = re.search(r'name="execution" value="(\S+)"', data)
                if execution_regex is None:
                    raise ValueError("Le paramètre execution n'a pas pu être récupéré.")
                execution = execution_regex.group(1)

                login_data = {
                    "username": self.username,
                    "password": self.password,
                    "execution": execution,
                    "_eventId": "submit"
                }
                async with session.post(url, data=login_data) as login_request:
                    return str(login_request.url).split('ticket=')[1]

    def get_auth_token(self):
        response = self.login()
        return response['authToken']

async def main():
    user = Utilisateur("username", "password")
    ticket = await user.get_ticket("https://mobile-back.univ-lorraine.fr/schedule")
    print(ticket)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())