import discord
import dotenv

import os

from game import DiscordShuffleGame

dotenv.load_dotenv('.env')

token = os.getenv('TOKEN')
channel_id = os.getenv('CHANNEL')
channel_id = int(channel_id)

client = discord.Client()
game = DiscordShuffleGame()

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    await game.ready(channel)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await game.next(message)

client.run(token)