# Université Lorraine Automatisation

Ce repo contient différentes automatisations pour l'Université de Lorraine, utilisant des supports pour l'Université de Lorraine, dont le Mobile inspiré de [ce repo](https://github.com/maelgangloff/univ-lorraine-api).

## Mobile

Support pour récupérer l'emploi du temps de l'Université de Lorraine grâce à l'API de l'Université de Lorraine. Il est possible d'ajouter d'autres fonctionnalités dans le futur. Si vous avez besoin d'autres choses, regardez le repo mentionné ci-dessus.

## MDW

Support pour récupérer les notes de l'Université de Lorraine avec du scrapping.

### Prérequis
Il est important d'avoir Firefox installé sur votre machine, à l'emplacement par défaut `/usr/bin/firefox`, ou de modifier le chemin dans le fichier Python. De plus, vous devez avoir `geckodriver` dans le chemin de votre machine, dans `src/ressources/geckodriver`, ou changer le chemin.

## Bot Discord

J'ai créé un bot Discord pour qu'à chaque fois qu'il y a une nouvelle note sur MDW, il envoie un message sur Discord.  
Le bot est développé avec `discord.py`.  
Le script qui vérifie les notes est dans `send_notification.py` et doit être lancé périodiquement pour vérifier les notes (par exemple, avec cron).  
Pour faire fonctionner le bot, vous avez besoin d'un serveur pour le mettre en ligne.

### Commandes du bot
- `!here` : Inscrit le channel courant pour recevoir les notifications.
- `!remove` : Désinscrit le channel courant pour ne plus recevoir les notifications.
- `!aide` : Affiche les commandes disponibles.

## Synchronisation avec Google Calendar

C'est un script qui permet de synchroniser l'emploi du temps de l'Université de Lorraine avec Google Calendar. Il peut être lancé périodiquement avec cron, par exemple, pour mettre à jour l'emploi du temps sur Google Calendar.

**Attention :** Le script supprime tous les événements de l'emploi du temps sur Google Calendar et les remet à jour. Il est donc important d'utiliser un calendrier séparé pour ne pas perdre les événements déjà présents sur Google Calendar.

Il est important de suivre les instructions de ce lien pour pouvoir utiliser l'API Google Calendar :  
[Quickstart Google Calendar Python](https://developers.google.com/calendar/api/quickstart/python)

## Configuration

### config.json
J'utilise un fichier de configuration qui est dans le `.gitignore` pour des raisons évidentes. Voici à quoi il doit ressembler.  
Le fichier `src/ressources/config.json` doit avoir le format suivant :

```json
{
  "LOGIN": "username",  // Votre login de l'Université de Lorraine
  "PASSWORD": "password",  // Votre mot de passe de l'Université
  "CALENDAR_ID": "id_google_calendar",  // ID de votre Google Calendar (un calendrier séparé pour ne pas perdre les événements déjà présents)
  "NB_JOUR": 30,  // Nombre de jours à récupérer
  "TOKEN_DISCORD": "token_du_bot_discord",  // Token du bot Discord
  "CHANNEL_ID": "id_du_channel_discord"  // ID du channel Discord
}
```
### Dossier Ressources

Le dossier ressources contient plusieurs éléments que vous devez télécharger :
- `geckodriver` : Le driver pour Firefox pour le scrapping.
- `config.json` : Le fichier de configuration.
- `oauth.json` : Le fichier de credentials pour Google Calendar.
- `token.json` : Le fichier de token pour Google Calendar généré par le Quickstart.
- `notes.db` : La base de données SQLite pour les notes, générée automatiquement par MDW.
