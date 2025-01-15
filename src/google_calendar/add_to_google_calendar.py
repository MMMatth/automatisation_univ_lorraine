import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json


SCOPES = ["https://www.googleapis.com/auth/calendar"]

# classe qui permet d'intéragir avec l'api de google calendar
class google_calendar:
    def __init__(self, credentials_path, scopes, token = "./token.json"):
        self.service = self.get_service(credentials_path, token, scopes)

    # fonction qui permet de recuperer le service de google calendar
    def get_service(self, credentials_path, token_path, scopes):
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("Refreshed token")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    # fonction qui permet d'ajouter un evenement à un calendrier
    def add_event(self, calendar_id, event):
        try:
            event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            # print(f'Event created: {event["htmlLink"]}')
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    # fonction qui permet de supprimer tous les evenements d'un calendrier
    def clear_all_events(self, calendar_id):
        page_token = None
        while True:
            events = self.service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
            
            for event in events['items']:
                if ( self.service.events().delete(calendarId=calendar_id,  eventId=event['id']).execute() == None):
                    print("Erreur sur le delete de l'event" + event['id'])
                else:
                #    print("Event deleted: " + event['id'])
                    pass
    
    def clear_all_events_afer_today_midnight(self, calendar_id):
        page_token = None
        # heure de aujourd'hui à minuit
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        while True:
            events = self.service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
            
            for event in events['items']:
                if 'dateTime' in event['start']:
                    start = event['start']['dateTime']
                    start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                    # on eneleve le timezone
                    start = start.replace(tzinfo=None)
                    # on recuper que la date
                    
                elif 'date' in event['start']:
                    start = event['start']['date']
                    start = datetime.datetime.strptime(start, '%Y-%m-%d')
                    

                now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                
                if start >= now:
                    if ( self.service.events().delete(calendarId=calendar_id,  eventId=event['id']).execute() == None):
                        print("Erreur sur le delete de l'event" + event['id'])
                    else:
                        pass
                        # print("Event deleted: " + event['id'])
            
            page_token = events.get('nextPageToken')
            
            if not page_token:
                break