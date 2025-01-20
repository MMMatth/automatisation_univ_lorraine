import requests
from api_univ_lorraine.Utilisateur import Utilisateur


MDW_URL = "https://mdw.univ-lorraine.fr/"
NOTE_PATH = "/UIDL/?v-uiId=0"



# classe qui permet d'intéragir avec l'api de multi
class Mdw:
    def __init__(self, token, refresh_token):
        self.token = token
        self.refresh_token = refresh_token

    def get_notes(self):
        headers = {
            'Cookie': 'UL-AUTHTRACE=TRACE-2358-OTuOSjXpPrAFSfXnIFEB-lK7uHwdORQamQCAS-LEIA; JSESSIONID=CFC307C1791C814D1B1BAF8540CCE4D8; ULMDWID=back-lb4-mdw',
            'Content-Type': 'application/json',
        }
        body = {
            "csrfToken": "6411b589-5b81-4bb5-9065-4a891e413e27",
            # "rpc": [["126", "com.vaadin.shared.ui.button.ButtonServerRpc", "click", [{"altKey": False, "button": "LEFT", "clientX": 679, "clientY": 397, "ctrlKey": False, "metaKey": False, "relativeX": 67, "relativeY": 25, "shiftKey": False, "type": 1}]]],
            # "syncId": 1,
            # "clientId": 1
        }
        response = requests.get(f'{MDW_URL}{NOTE_PATH}', headers=headers, json=body)
        return response.text



def main():
    user = Utilisateur("username", "password")
    token = user.get_auth_token()
    mdw = Mdw(token, None)
    print(mdw.get_notes())

if __name__ == '__main__':
    main()