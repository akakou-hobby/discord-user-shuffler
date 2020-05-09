import discord
import dotenv

import os

dotenv.load_dotenv('.env')
token = os.getenv('TOKEN')

print(token)
