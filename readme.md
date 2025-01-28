# Université Lorraine support
Ceci est un petit support pour l'université de lorraine.
## Mobile
Support pour recuperer l'emploie du temp de l'université lorraine grace a l'api de l'université lorraine
## MDW
Support pout recuperer les notes de l'université lorraine avec du scrapping

Pour ce support il est important d'avoir firefox d'installer sur votre machine present de base `/usr/bin/firefox` 
ainsi que geckodriver dans le path de votre machine `src/ressources/geckodriver`

## Bot discord
J'ai fait un bot discord pour que quand il y'a une nouvelle note sur MDW il envoie un message sur discord.
Le bot est fait avec discord.py. 
Le script qui verifie les notes est dans send_notification.py et doit etre lancé tout un certain temps pour verifier les notes ( avec cron par exemple )

### Commande du bot
- `!here` : permet de s'inscrire pour recevoir les notifications
- `!remove` : permet de se desinscrire pour ne plus recevoir les notifications
- `!aide` : affiche les commandes

## Sync avec google calendar
C'est un script qui permet de synchroniser l'emploie du temps de l'université lorraine avec google calendar. Il peut etre lancé avec cron par exemple pour mettre a jour l'emploie du temps sur google calendar.

**Attention  le script supprime tout les evenements de l'emploie du temps sur google calendar et les remet a jour donc il est important d'utiliser un calendrier a part pour ne pas perdre les evenements deja present sur google calendar.**

Il est important de suivre les instructions de ce lien pour pouvoir utiliser l'api google calendar
[quickstart google calendar python
](https://developers.google.com/calendar/api/quickstart/python)

## Config
Le fichier `src/ressources/config.json` doit ressembler à ça
```json
{
  "LOGIN": "username", // votre login de l'université lorraine
  "PASSWORD": "password",   // votre mot de passe de l'université
  "CALENDAR_ID": "id_google_calendar",  // id du calendrier google calendar ( Un calendrier a part pour ne pas perdre les evenements deja present )
  "NB_JOUR": 30, // nombre de jour a recuperer
  "TOKEN_DISCORD": "token du bot discord", // token du bot discord
  "channel_id" : "id du channel discord" // id du channel discord
}
```

donc le dossier ressources contient : 
- `geckodriver` : le driver pour firefox pour le scrapping
- `config.json` : le fichier de configuration 
- `oauth.json` : le fichier de credentials pour google calendar
- `token.json` : le fichier de token pour google calendar generated par le quickstart
- `notes.db` : la base de donnée sqlite pour les notes generé automatiquement par MDW