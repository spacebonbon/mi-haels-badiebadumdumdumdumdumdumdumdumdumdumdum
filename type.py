started = 0
playing = False
queue = []
skipsong = False
opengames = []
gamedata = []
niceto = []

import ffmpeg
import math
import asyncio
import pdb
from pyexpat.errors import messages
import commands.mafia as mfia
import commands.catgame as kittygame
import yt_dlp as youtube_dl
import os
import time
import nextcord as discord
from nextcord.ext import commands
import random
from random import choice
from nextcord.ext.commands import has_permissions, MissingPermissions
from mutagen.mp3 import MP3
import requests
from typing import Text
import aiohttp
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

file = open("token.env")

token = file.read()

skinwalker = [120803980983409834209834298098,219083210980321809123809809]

client = discord.Client()

client = commands.Bot(command_prefix='./', intents=intents)

DiscordComponents(client)

@client.event
async def on_ready():
	formatted_list = ""
	text_channel_list = []
	for guild in client.guilds:
		formatted_list += f"{guild.name} -- {guild.id}\n"
		for channel in guild.text_channels:
			try:
				async with channel.typing():
					pass
			except:
				print("damn")
			print(channel.name)
client.run(token)
