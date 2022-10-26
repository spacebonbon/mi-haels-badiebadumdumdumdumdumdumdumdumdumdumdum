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
import discord
from discord.ext import commands
import random
from random import choice
from discord.ext.commands import has_permissions, MissingPermissions
from mutagen.mp3 import MP3
import discord_components
from discord_components import DiscordComponents, Button, SelectOption, Select, Interaction
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
			formatted_list += f"	{channel.name} -- {channel.id}\n"
			text_channel_list.append(channel)
	print(formatted_list)
	print("input channel id")
	cid = int(input())
	channel = client.get_channel(cid)
	history = await channel.history(limit=1000).flatten()
	print(history == None)
	history.reverse()
	formatted_history = ""
	print("getting msgs")
	for message in history:
		pre = f"{message.author}: {message.content} \nmessage attachments:{len(message.attachments) > 0}\n\n"
		formatted_history += pre
	print(formatted_history)
	print("what do you want to say?")
	async with channel.typing():
		message = input()
		await channel.send(message)

client.run(token)
