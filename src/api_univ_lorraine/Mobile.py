import requests
from api_univ_lorraine.setup import MOBILE_URL, TIMETABLE_MOBILE_PATH

# classe qui permet d'intéragir avec l'api de multi
class Mobile:
    def __init__(self, token):
        self.token = token

    def get_edt (self, user_id, start_date, end_date):
        url = MOBILE_URL + TIMETABLE_MOBILE_PATH
        request = {
            "asUser": user_id,
            "authToken": self.token,
            "endDate": end_date,
            "startDate": start_date,
        }
        response = requests.post(url, json=request)
        return response.json()