# Université Lorraine support
## Mobile
Support pour recuperer l'emploie du temp de l'université lorraine grace a l'api de l'université lorraine
## MDW
Support pout recuperer les notes de l'université lorraine avec du scrapping

Pour ce support il est important d'avoir firefox d'installer sur votre machine present de base `/usr/bin/firefox` 
ainsi que geckodriver dans le path de votre machine `src/ressources/geckodriver`

## Sync avec google calendar
Il est important de suivre les instructions de ce lien pour pouvoir utiliser l'api google calendar
[quickstart google calendar python
](https://developers.google.com/calendar/api/quickstart/python)
## Config
Le fichier `src/ressources/config.json` doit ressembler à ça
```json
{
  "LOGIN": "username", 
  "PASSWORD": "password",  
  "CALENDAR_ID": "id_google_calendar", 
  "NB_JOUR": 30, 
  "TOKEN_DISCORD": "token du bot discord",
  "channel_id" : "id du channel discord"
}
```

donc le dossier ressources contient : 
- `geckodriver` : le driver pour firefox
- `config.json` : le fichier de configuration
- `oauth.json` : le fichier de credentials pour google calendar
- `token.json` : le fichier de token pour google calendar generated par le quickstart
- `notes.db` : la base de donnée sqlite pour les notes generé automatiquement par MDW