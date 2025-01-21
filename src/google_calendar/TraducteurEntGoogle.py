# Function to generate a unique color for each course label

color_nb = 0

def get_color_for_label(label, color_map):
    global color_nb
    label = ' '.join(label.split(' ')[2:])  # Convert the list to a string
    if label not in color_map:
        color_map[label] = color_nb
        color_nb = (color_nb + 1) % 11
    return color_map[label]

def from_ent_to_google(respond_ent):
    # Dictionary to store the color for each course label
    color_map = {}
    course_info = []

    # Iterate over the plannings
    for planning in respond_ent['plannings']:
        for event in planning['events']:
            course_label = event['course']['label']
            color = get_color_for_label(course_label, color_map)
            course_info.append({
                'summary': course_label,
                'location': ', '.join(room['label'] for room in event['rooms']),
                'description': ', '.join(teacher['displayname'] for teacher in event['teachers']),
                'start': {
                    'dateTime': event['startDateTime'],
                    'timeZone': 'Europe/Paris',
                },
                'end': {
                    'dateTime': event['endDateTime'],
                    'timeZone': 'Europe/Paris',
                },
                'colorId': color,
            })
    return course_info