import discord
from discord.ext import commands
import json
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_base import data_base_manager

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

db_manager = data_base_manager.DatabaseManager('ressources/data.db')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


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

@bot.command(name='aide')
async def help(ctx):
    await ctx.send("Commandes disponibles:\n"
                   "!here: ajoute le channel courant à la liste\n"
                   "!remove: enlève le channel courant de la liste\n")

@bot.command(name='here')
async def set_channel(ctx):
    channel_id = ctx.channel.id
    channel_name = ctx.channel.name
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    if db_manager.save_channel(channel_id, channel_name, server_name, server_id):
        await ctx.send(f"Channel {ctx.channel} ajouté à la liste")
    else:
        await ctx.send("Channel déjà présent dans la liste")

@bot.command(name='remove')
async def remove_channel(ctx):
    channel_id = ctx.channel.id
    if db_manager.remove_channel(channel_id):
        await ctx.send(f"Channel {ctx.channel} enlevé de la liste")
    else:
        await ctx.send("Channel pas trouvé dans la liste")

bot.run(config.get("TOKEN_DISCORD"))