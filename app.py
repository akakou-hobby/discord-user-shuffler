import discord
import dotenv

import os

from game import Game

dotenv.load_dotenv('.env')

token = os.getenv('TOKEN')
channel_id = os.getenv('CHANNEL')
channel_id = int(channel_id)

client = discord.Client()
game = Game()

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    await game.setup(channel)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await game.next(message)

client.run(token)