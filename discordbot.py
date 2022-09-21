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

skinwalkers = []

def most_frequent(List):
	counter = 0
	num = List[0]

	for i in List:
		curr_frequency = List.count(i)
		if (curr_frequency > counter):
			counter = curr_frequency
			num = i

	return num

def texts(file):
	with open(file) as f:
		lines = f.readlines()
		lines = [s.strip('\n') for s in lines]
		return choice(lines)



def countOccurrences(str, word):
	# split the string by spaces in a
	a = str.split(" ")

	# search for pattern in a
	count = 0
	for i in range(0, len(a)):

		# if match found increase count
		if (word == a[i]):
			count = count + 1

	return count

def compress_video(video_full_path, output_file_name, target_size):
	# Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
	min_audio_bitrate = 32000
	max_audio_bitrate = 256000

	probe = ffmpeg.probe(video_full_path)
	# Video duration, in s.
	duration = float(probe['format']['duration'])
	# Audio bitrate, in bps.
	audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
	# Target total bitrate, in bps.
	target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

	# Target audio bitrate, in bps
	if 10 * audio_bitrate > target_total_bitrate:
		audio_bitrate = target_total_bitrate / 10
		if audio_bitrate < min_audio_bitrate < target_total_bitrate:
			audio_bitrate = min_audio_bitrate
		elif audio_bitrate > max_audio_bitrate:
			audio_bitrate = max_audio_bitrate
	# Target video bitrate, in bps.
	video_bitrate = target_total_bitrate - audio_bitrate

	i = ffmpeg.input(video_full_path)
	ffmpeg.output(i, os.devnull,
				  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
				  ).overwrite_output().run()
	ffmpeg.output(i, output_file_name,
				  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
				  ).overwrite_output().run()

async def findgame(id):
	global opengames
	for index, game in enumerate(opengames):
		if id in game[0]:
			return index
	return None



client = discord.Client()
client = commands.Bot(command_prefix='./', intents=intents)
DiscordComponents(client)

@client.event
async def on_ready():
	global niceto
	file = open("assets/textFiles/niceto.who")
	niceto = file.readlines()
	niceto = [int(s.strip('\n')) for s in niceto]
	file.close()
	print(niceto)

@client.event
async def on_reaction_add(reaction, user):
	global opengames
	index = await findgame(int(reaction.message.id))
	if index == None:
		return
	pdb.set_trace()
	if user.id == opengames[index][1]:
		if str(reaction.emoji) in "⬆️⬅️➡️⬇️":
			await reaction.remove(user)

	print(reaction.emoji)

@client.event
async def on_reaction_remove(reaction, user):
	if reaction.message.id in opengames:
		if str(reaction.emoji) == "⬆️":
			pass

	print(reaction.emoji)

@client.event
async def on_message(message):
	if message.author.id == 986803208796119070 and message.reference != None and not message.is_system:
		tf = [True,False,True,False,True]
		if random.choice(tf):
			await message.reply(texts("assets/textFiles/disses.4u"))
	if ("./delete" in message.content.lower()):
		time.sleep(1)
		await message.delete()
		message.content = message.content[8:].strip(" ")
	if "meow" in message.content.lower() and not str(message.author) == "mi haels bot#6905":
		await message.channel.send("meow")
	if str(message.content) == "./shutdown":
		if str(message.author) == "mi hael#1007":
			msg = await message.channel.send(":neutral_face::gun:")
			await asyncio.sleep(2)
			await msg.edit(content=":skull::gun:")
			await asyncio.sleep(2)
			quit()
		else:
			await message.channel.send("you don't have control over me " + str(message.author) + "!")
	
	if "s my fortune" in message.content.lower() or message.content == "./fortune":
		if (random.randint(0, 100) < 50):
			await message.channel.send(texts("assets/textFiles/misfortunes.txt"))
		else:
			await message.channel.send(texts("assets/textFiles/fortunes.txt"))
	if "tiktok.com" in message.content.lower():
		print("tiktok found!")
		await message.add_reaction("✅")
		os.system("yt-dlp -v -o video.mp4 " + message.content)
		compress_video("video.mp4","compvideo.mp4", 7500)
		file = discord.File("compvideo.mp4")
		await message.reply(file=file)
		os.remove("video.mp4")
		os.remove("compvideo.mp4")
	if "youtube.com/shorts" in message.content.lower():
		await message.add_reaction("✅")
	if client.user.mentioned_in(message):
		try:
			message = await message.channel.fetch_message(message.reference.message_id)
			await on_message(message)
			return
		except:
			if message.author == client.user:
				return
			await message.reply(content="DONT PING ME FOR NO REASON!!!!!!")
	await client.process_commands(message)

@client.command()
async def mafia(ctx):
	await mfia.mafia(ctx,client)

@client.command()
async def catgame(ctx):
	global opengames
	global gamedata
	game = await kittygame.start()
	skin = await kittygame.discordskin(game[0])
	msg = await ctx.channel.send(skin)
	reactions = ["⬆️","⬅️","➡️","⬇️"]
	for emoji in reactions:
		await msg.add_reaction(emoji)
	opengames.append([ctx.message.id, ctx.author.id])
	gamedata.append(game)
	pdb.set_trace()

@client.command()
async def owner(ctx):
	await ctx.message.delete()
	await ctx.channel.send(ctx.guild.owner.id)

@client.command(hidden=True)
async def nice(ctx, member: discord.User = None):
	global niceto
	if (ctx.author.id == 530508910713372682 and member != None):
		file = open('assets/textFiles/niceto.who', 'r+')
		lines = file.read()
		file.write(str(member.id)+"\n")
		file.close()
		await on_ready()
	elif int(ctx.author.id not in niceto):
			file = open('assets/textFiles/niceto.who', 'r+')
			lines = file.read()
			file.write(str(ctx.author.id)+"\n")
			file.close()
			await on_ready()

@client.command(hidden=True)
async def listnice(ctx):
	for id in niceto:
		person = (client.get_user(id))
		print(person)

@client.command(hidden=True)
async def unnice(ctx, member: discord.User = None):
	global niceto
	if (ctx.author.id == 878796669871853618 or ctx.author.id == 530508910713372682 and member != None):
		for index, person in enumerate(niceto):
			if int(person) == member.id:
				niceto.pop(index)
				break
	else:
		for index, person in enumerate(niceto):
			if int(person) == ctx.author.id:
				niceto.pop(index)
				break
	file = open('assets/textFiles/niceto.who', 'w')
	strng = ""
	for line in niceto:
		strng += str(line)+"\n"
	file.write(strng)
	file.close()
	await on_ready()

@client.command()
async def debug(ctx):
	if (ctx.author.id == 530508910713372682):
		await ctx.channel.send(niceto)

@client.command()
async def cat(ctx):
	response = requests.get('https://aws.random.cat/meow')
	data = response.json()
	embed = discord.Embed(
		title = 'Cat',
		colour = discord.Colour.purple()
		)
	embed.set_image(url=data['file'])
	embed.set_footer(text="")
	await ctx.send(embed=embed)

@client.command()
async def nick(ctx, *, content):
	if str(ctx.message.author) == "mi hael#1007":
		await ctx.message.channel.send("Did you mean LegendaryDumbass?")
		await ctx.message.author.edit(nick="LegendaryDumbass")
	else:
		await ctx.message.author.edit(nick=content)

@client.command()
async def wear(ctx, id=None):
	skinwalkers.append([ctx.author.id, id])
	print(skinwalkers)

@client.command()
async def play(ctx, url: str):
	global playing, queue
	await ctx.message.delete()
	queue.append(url)
	if not playing:
		global skipsong
		while len(queue) > 0:
			song_there = os.path.isfile("song.mp3")
			try:
				if song_there:
					os.remove("song.mp3")
			except PermissionError:
				await ctx.send("Wait for the current playing music to end or use the 'stop' command")
				return
			await ctx.channel.send("loading song please wait")
			ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
				}],
			}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([queue[0]])
			for file in os.listdir("./"):
				if file.endswith(".mp3"):
					os.rename(file, "song.mp3")
			audio = MP3("song.mp3")
			duration = (audio.info.length)
			await ctx.channel.send("done")
			voice_channel = ctx.author.voice.channel
			try:
				vc= await voice_channel.connect()
			except:
				voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
				await voice.disconnect()
				vc= await voice_channel.connect()
			queue.pop(0)
			playing = True
			vc.play(discord.FFmpegPCMAudio("song.mp3"))
			start = time.time()
			while (time.time() - start) < duration and not skipsong:
				pass
			if skipsong:
				skipsong = False
			playing = False
			await vc.disconnect()
	else:
		await ctx.channel.send("added to queue please wait")




@client.command()
async def unmafia(ctx):
	for channel in ctx.guild.channels:
		if str(channel.name) == "mafia":
			await channel.delete()
@client.command()
async def forceplay(ctx):
	voice_channel = ctx.author.voice.channel
	try:
		vc= await voice_channel.connect()
	except:
		voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
		await voice.disconnect()
	vc.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def skip(ctx):
	global skipsong
	skipsong= True

@client.command()
async def rickroll(ctx):
	voice_channel = ctx.author.voice.channel
	try:
		vc= await voice_channel.connect()
	except:
		voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
		await voice.disconnect()
	vc.play(discord.FFmpegPCMAudio("astley/rickroll.mp3"))
	

@client.command()
async def leave(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect()
	else:
		await ctx.send("The bot is not connected to a voice channel.")
"""
@client.command(
	name='vuvuzela',
	description='plays your favorite song on youtube!',
	pass_context=True,
	)
async def ply(context):
	# grab the user who sent the command
	user=context.message.author
	voice_channel=user.voice.voice_channel
	channel=None
	# only play music if user is in a voice channel
	if voice_channel!= None:
		# grab user's voice channel
		channel=voice_channel.name
		await client.say('User is in channel: '+ channel)
		# create StreamPlayer
		vc= await client.join_voice_channel(voice_channel)
		player = vc.create_ffmpeg_player('vuvuzela.mp3', after=lambda: print('done'))
		player.start()
		while not player.is_done():
			await asyncio.sleep(1)
		# disconnect after the player has finished
		player.stop()
		await vc.disconnect()
	else:
		await client.say('User is not in a channel.')
"""
@client.command()
async def pause(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	voice.stop()

@client.command()
async def among_us(ctx):
	await ctx.channel.send("starting game instance")
	text_channel_list = []
	for channel in ctx.guild.text_channels:
		text_channel_list.append(channel.name)
		with open(f"{str(channel.name)}.txt", 'w+') as file:
			histry = await channel.history().flatten()
			history = ""
			for message in histry:
				history += (f"{message.author}: {message.content}\n")
			file.write(history)
	print(text_channel_list)
	await ctx.channel.send("Welcome message")
	
@client.command()
async def id(ctx):
	await ctx.channel.send(ctx.author.id)

@client.command()
async def ping(ctx):
	if (int(ctx.author.id) == 878796669871853618 or ctx.author == ctx.guild.owner):
		string = ""
		await ctx.channel.send("ok")
		for member in ctx.guild.members:
			string += member.mention
		await ctx.channel.send(string)

@client.command()
async def legendary(ctx):
	if (int(ctx.author.id) == 878796669871853618 or ctx.author == ctx.guild.owner):
		await ctx.channel.send("Renaming everybody to a Legendary name (if not already)")
		members = ctx.guild.members
		print(members)
		changes = ""
		for member in members:
			name = member.nick
			if name == None:
				name = member.display_name
			print(name)
			if ("legendary" not in name.lower()):
				try:
					await member.edit(nick="Legendary"+name)
					changes += (f"{name} changed to {member.nick}\n")
				except:
					changes += (f"failed renaming {member.display_name}\n")
		await ctx.channel.send("done")
		await ctx.channel.send(changes)


@client.command()
@has_permissions(manage_messages=True)
async def nuke(ctx, number=0):
	await ctx.message.delete()
	if number == 0:
		ctx.message.reply(content="you need to specify how many")
	
	await ctx.channel.purge(limit=int(number))


@client.command(
	name='fight',
	description='Lets you 1v1 somebody say ./fight for help on how to use this command',
)
async def fight(ctx, member: discord.User = None):
	if member == None:
		await ctx.send("help message")
		return
	if str(member) == "@everyone":
		await ctx.send("Trust me pal your not that guy")
		return
	message = await ctx.send("fighting "+member.mention, components = [
		[Button(label="attack", style="3", custom_id="attack")],
		[Button(label="run", style="1", custom_id="run")]
	])
	start = time.time()
	def check_button(i: discord_components.Interaction):
		return i
	turn = 0
	provoker = [100,15,1]
	victim   = [100,15,1]
	if str(member) == "IzMlxlin#8307":
		victim = [420, 69, 40]
	if str(ctx.author) == "IzMlxlin#8307":
		provoker = [99999,99999,9999]
	turnName = ctx.author.mention
	action = f"fighting {member.mention}"
	await message.edit(content = f"{action}\n{ctx.author.mention}stats:\nhp: {provoker[0]}\natk: {provoker[1]}\ndef: {provoker[2]}\n---------------------------\n{member.mention} stats:\nhp: {victim[0]}\natk: {victim[1]}\ndef: {victim[2]}\n---------------------------\n{turnName}'s turn")
	while 1:
		interaction = await client.wait_for('button_click', check=check_button)
		start = time.time()
		if turn == 1:
			if interaction.author == member:
				turn = 0
				turnName = ctx.author.mention
				if str(interaction.custom_id) == "run":
					await interaction.message.edit(content=member.mention + " you are a wimp", components=[])
					interaction.disable_compnents()
					return
				if str(interaction.custom_id) == "attack":
					power = random.randint(0, victim[1]) - provoker[2]
					if power < 0:
						power = 0
					provoker[0] -= power
					action = f"{member.mention} attacks {ctx.author.mention} and deals {power} damage"
				await interaction.message.edit(
					content=f"{action}\n{ctx.author.mention}stats:\nhp: {provoker[0]}\natk: {provoker[1]}\ndef: {provoker[2]}\n---------------------------\n{member.mention} stats:\nhp: {victim[0]}\natk: {victim[1]}\ndef: {victim[2]}\n---------------------------\n{turnName}'s turn")
			else:
				await interaction.send("It is not your turn", delete_after=5)
			deletit = await interaction.send("loading", delete_after=0, ephemeral=False)
		else:
			if interaction.author == ctx.author:
				turn = 1
				turnName = member.mention
				if str(interaction.custom_id) == "run":
					await interaction.message.edit(content=ctx.author.mention + " you are a wimp", components=[])
					interaction.disable_compnents()
					return
				if str(interaction.custom_id) == "attack":
					power = random.randint(0, victim[1])-provoker[2]
					if power < 0:
						power = 0
					victim[0] -= power
					action = f"{ctx.author.mention} attacks {member.mention} and deals {power} damage"
				await interaction.message.edit(
					content=f"{action}\n{ctx.author.mention}stats:\nhp: {provoker[0]}\natk: {provoker[1]}\ndef: {provoker[2]}\n---------------------------\n{member.mention} stats:\nhp: {victim[0]}\natk: {victim[1]}\ndef: {victim[2]}\n---------------------------\n{turnName}'s turn")
			else:
				await interaction.send("It is not your turn", delete_after=5)
		deletit = await interaction.send("loading", delete_after=0,ephemeral=False)
		if provoker[0] <= 0:
			await ctx.channel.send(f"{ctx.author.mention} died")
			break
		if victim[0] <= 0:
			await ctx.channel.send(f"{member.mention} died")
			break
@nuke.error
async def nuke_error(ctx, error):
	await ctx.send("You cannot do that {}! You do not have message management permissions!".format(ctx.author.mention))


client.run(token)
