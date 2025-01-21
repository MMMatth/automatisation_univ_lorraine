import discord
from discord.ext import commands
import json
import os
import logging

"""
Ce fichier est un bot discord qui permet d'envoyer des messages sur un channel discord.
"""

# Set up logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Path to the configuration file
CONFIG_FILE = 'ressources/config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

@bot.event
async def on_ready():
    logging.info(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_disconnect():
    logging.warning('Bot has disconnected')

@bot.event
async def on_resumed():
    logging.info('Bot has resumed')

@bot.command(name='send')
async def send_message(ctx, *, message: str):
    channel_id = config.get('channel_id')
    if channel_id is None:
        await ctx.send("Channel not set. Use the !setchannel command to set the channel.")
    else:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            await channel.send(message)
        else:
            await ctx.send("Invalid channel ID. Use the !setchannel command to set a valid channel.")

@bot.command(name='setchannel')
async def set_channel(ctx, id: int):
    config['channel_id'] = id
    save_config(config)
    await ctx.send(f"Channel set to {id}")

bot.run(config.get("TOKEN_DISCORD"))