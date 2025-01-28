import datetime
import json
import requests
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_univ_lorraine.Mdw import Mdw
from api_univ_lorraine.Utilisateur import Utilisateur
from data_base import data_base_manager

"""
Ce fichier sert a faire le lien entre l'api de l'université de lorraine et discord.
"""


# Set up logging
logging.basicConfig(level=logging.INFO)

# Path to the configuration file
CONFIG_FILE = 'ressources/config.json'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def send_discord_message(channel_id, token, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("Message sent successfully")
    else:
        logging.error(f"Failed to send message: {response.status_code} - {response.text}")

def main():
    config = load_config()
    db_manager = data_base_manager.DatabaseManager('ressources/data.db')
    channels_id = db_manager.get_all_channels(True)
    token = config.get('TOKEN_DISCORD')

    user = Utilisateur(config.get('LOGIN'), config.get('PASSWORD'))
    mdw = Mdw(user)
    mdw.login()
    nouvelle_notes = mdw.update_db()

    for channel_id in channels_id:
        if nouvelle_notes:
            message = " nouvelle(s) note(s):\n" + "\n".join([f"{matiere}" for matiere, note in nouvelle_notes])
            logging.info(f"{datetime.datetime.now()} {message}")
            send_discord_message(channel_id, token, message)
        else:
            logging.info(f"{datetime.datetime.now()} Pas de nouvelles notes")

if __name__ == "__main__":
    main()