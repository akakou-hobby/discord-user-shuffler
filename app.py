import discord
import dotenv

import os

dotenv.load_dotenv('.env')

token = os.getenv('TOKEN')
channel_id = os.getenv('CHANNEL')
channel_id = int(channel_id)

client = discord.Client()

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    await channel.send('Botが起動しました')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        pass

client.run(token)