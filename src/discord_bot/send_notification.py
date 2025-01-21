import datetime
import json
import requests
from api_univ_lorraine.Mdw import Mdw
from api_univ_lorraine.Utilisateur import Utilisateur

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
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

def main():
    config = load_config()
    channel_id = config.get('channel_id')
    token = config.get('TOKEN_DISCORD')

    user = Utilisateur(config.get('LOGIN'), config.get('PASSWORD'))
    mdw = Mdw(user)
    mdw.login()
    nouvelle_notes = mdw.update_db()

    if nouvelle_notes:
        message = "@everyone nouvelle(s) note(s):\n" + "\n".join([f"{matiere}" for matiere, note in nouvelle_notes])
        print(datetime.datetime.now(), message)
        send_discord_message(channel_id, token, message)
    else:
        print(datetime.datetime.now(), "Pas de nouvelles notes")

if __name__ == "__main__":
    main()