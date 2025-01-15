
# Fonction qui prend en paramère le json de l'emploi du temps et renoie une liste d'évènements à ajouter à l'agenda
def from_ent_to_google(respond_ent) :
    # on parcourt les plannings
    course_info = []
    for planning in respond_ent['plannings']:
        for event in planning['events']:
            course_info.append({
                'summary': event['course']['label'],
                'location' : ', '.join(room['label'] for room in event['rooms']),
                'description': ', '.join(teacher['displayname'] for teacher in event['teachers']),
                'start': {
                    'dateTime': event['startDateTime'],
                    'timeZone': 'Europe/Paris',
                },
                'end': {
                    'dateTime': event['endDateTime'],
                    'timeZone': 'Europe/Paris',
                },
            })
    return course_info