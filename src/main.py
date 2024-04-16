from api_univ_lorraine import Utilisateur, Multi
from google_calendar.add_to_google_calendar import google_calendar, SCOPES
from datetime import datetime, timedelta
import json

# fonction qui permet d'extraire les informations des cours
def extract_course_info(edt, groups):
    # on parcourt les plannings
    course_info = {}
    for planning in edt['plannings']:
        for event in planning['events']:
            # on recupere les informations du cours
            course_name = event['course']['label']
            
            schedule = (event['startDateTime'], event['endDateTime'])
            
            room = event['rooms'][0]['label'] if event['rooms'] else None
            
            teacher = event['teachers'][0]['name'] if event['teachers'] else None
            
            event_groups = [group['label'] for group in event['groups']]
            
            if any(group in event_groups for group in groups):
                course_info[course_name] = {'schedule': schedule, 'room': room, 'teacher': teacher, 'groups': event_groups}
    
    return course_info

def main():
    data = json.loads(open('./ressources/param.json').read())
    
    univ_lorraine_id = data['univ_lorraine_id']
    univ_lorraine_password = data['univ_lorraine_password']
    google_calendar_id = data['google_calendar_id']
    univ_lorraine_groups = data['univ_lorraine_groups']
    nb_jours_a_recuperer = data["nombre_jour_a_recuperer_apres_auj"]
    
    # on recupere les tokens
    tokens=(Multi.Multi.login(Utilisateur.Utilisateur(univ_lorraine_id, univ_lorraine_password)))
    if tokens is None:
        return False
    # on cree une instance de Multi
    multi = Multi.Multi(tokens[0], tokens[1])
    
    # on recupere l'emploi du temps
    google_calendar_instance = google_calendar('./ressources/credentials.json',  SCOPES, "./ressources/token.json")
        
    # on supprime tous les evenements de l'agenda
    google_calendar_instance.clear_all_events_afer_today_midnight(google_calendar_id)
    
    # on ajoute les evenements à l'agenda tous les 4 jours
    for i in range(0, nb_jours_a_recuperer, 4):
        # on recupere l'emploi du temps pour les 4 prochains jours
        edt = multi.get_timetable(univ_lorraine_id, datetime.now() + timedelta(days=i), datetime.now() + timedelta(days=i+3))
        # on extrait les informations des cours
        new_data = extract_course_info(edt,univ_lorraine_groups)
        
        if new_data is None:
            return False
        
        # on ajoute les evenements à l'agenda
        for course, details in new_data.items():
            if details['room'] is None:
                details['room'] = 'Aucune salle'
            event={
                'summary': course + ' - ' + details['room'],
                'start': {
                    'dateTime': details['schedule'][0],
                    'timeZone': 'Europe/Paris',
                },
                'end': {
                    'dateTime': details['schedule'][1],
                    'timeZone': 'Europe/Paris',
                },
                'location': details['room'],
                'description': details['teacher']
            }
            
            # if google_calendar_instance.add_event(google_calendar_id, event) is None:
            #     return None
            google_calendar_instance.add_event(google_calendar_id, event)
        return True
            
if __name__ == '__main__':
    if not main():
        print("Erreur lors de l'ajout des evenements à l'agenda")
    else:
        print("success")
        