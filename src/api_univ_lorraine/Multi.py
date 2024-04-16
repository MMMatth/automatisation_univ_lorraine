import requests
import json
from datetime import datetime, timedelta
from api_univ_lorraine.Utilisateur import Utilisateur
import asyncio
import json

data=json.loads(open('./ressources/multi.json').read())

MULTI_GRAPHQL_URL = data['MULTI_GRAPHQL_URL']
TIMETABLE_GRAPHQL_QUERY = data['TIMETABLE_GRAPHQL_QUERY']
CROUS_MENU_GRAPHQL_QUERY = data['CROUS_MENU_GRAPHQL_QUERY']
FACTUEL_GRAPHQL_QUERY = data['FACTUEL_GRAPHQL_QUERY']


# classe qui permet d'intéragir avec l'api de multi
class Multi:
    def __init__(self, token, refresh_token):
        self.token = token 
        self.refresh_token = refresh_token

    # fonction permet de recuperer l'emploi du temps d'un utilisateur
    def get_timetable(self, uid, from_date, to_date):
        query = {
            "operationName": "timetable",
            "query": TIMETABLE_GRAPHQL_QUERY,
            "variables": {
                "uid": uid,
                "from": int(from_date.timestamp() * 1000),
                "to": int(to_date.timestamp() * 1000)
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'x-refresh-token': self.refresh_token,
            'x-token': self.token
        }
        response = requests.post(MULTI_GRAPHQL_URL, headers=headers, data=json.dumps(query))
        return response.json()['data']['timetable']

    # fonction qui permet de recuperer le taux de remplissage d'une BU
    @staticmethod
    def get_affluence_bu(bu_token):
        response = requests.get(f'https://webapi.affluences.com/api/fillRate?token={bu_token}')
        return response.json()

    # fonction qui permet de recuperer les menus du crous
    @staticmethod
    def get_crous_menu():
        query = {
            "operationName": "crous",
            "query": CROUS_MENU_GRAPHQL_QUERY,
            "variables": {}
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(MULTI_GRAPHQL_URL, headers=headers, data=json.dumps(query))
        return response.json()['data']['restos']

    # fonction qui permet de recuperer les news factuels
    @staticmethod
    def get_factuel():
        query = {
            "operationName": "factuel",
            "query": FACTUEL_GRAPHQL_QUERY,
            "variables": {}
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(MULTI_GRAPHQL_URL, headers=headers, data=json.dumps(query))
        return response.json()['data']['news']

    # fonction qui permet de recuperer le token et le refresh token d'un utilisateur
    @staticmethod
    def login(user):
        token = asyncio.run(user.get_ticket('https://multi.univ-lorraine.fr/login'))
        query = {
            "operationName": "casAuth",
            "query": "query casAuth($token: String!) {casAuth(token: $token)}",
            "variables": {"token": token}
        }
        response = requests.post(
            MULTI_GRAPHQL_URL, json=query
        )
        
        if response.status_code == 200:
            return response.json()['data']['casAuth']
        else:
            return None
        

    
def main():
    code=(Multi.login(Utilisateur("username", "password")))
    multi=Multi(code[0],code[1])
    edt = multi.get_timetable("username", datetime.now(), datetime.now() + timedelta(days=2))
    with open("../../out/data.json", 'w') as f:
        json.dump(edt, f)
    
if __name__ == '__main__':
    main()