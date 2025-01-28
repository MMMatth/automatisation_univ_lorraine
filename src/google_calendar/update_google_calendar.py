import json
from datetime import datetime, timedelta

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_to_google_calendar import google_calendar
from TraducteurEntGoogle import from_ent_to_google
from api_univ_lorraine.Utilisateur import Utilisateur
from api_univ_lorraine.Mobile import Mobile


with open("ressources/config.json", "r") as file:
    config = json.load(file)

NB_JOUR = config["NB_JOUR"]
CALENDAR_ID = config["CALENDAR_ID"]
LOGIN = config["LOGIN"]
PASSWORD = config["PASSWORD"]

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDENTIALS_PATH = 'ressources/oauth.json'
TOKEN_PATH = 'ressources/token.json'

def get_auth_token(username, password):
    user = Utilisateur(username, password)
    return user.get_auth_token()

def get_ent_schedule(auth_token, user_id, date_from, date_to):
    mobile = Mobile(auth_token)
    return mobile.get_edt(user_id, date_from, date_to)

def clear_calendar_events(calendar, calendar_id):
    calendar.clear_all_events_afer_today_midnight(calendar_id)

def add_events_to_calendar(calendar, calendar_id, events):
    for event in events:
        calendar.add_event(calendar_id, event)

def main():
    auth_token = get_auth_token(LOGIN, PASSWORD)

    date_from = str(datetime.now().date())
    date_to = str(datetime.now().date() + timedelta(days=NB_JOUR))
    ent = get_ent_schedule(auth_token, LOGIN, date_from, date_to)

    events = from_ent_to_google(ent)

    calendar = google_calendar(CREDENTIALS_PATH, SCOPES, TOKEN_PATH)
    clear_calendar_events(calendar, CALENDAR_ID)
    add_events_to_calendar(calendar, CALENDAR_ID, events)

if __name__ == "__main__":
    main()