started = 0
playing = False
queue = []
skipsong = False

niceto = []

import math
import asyncio
from pyexpat.errors import messages
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

intents = discord.Intents.all()


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

client = discord.Client()
client = commands.Bot(command_prefix='./', intents=intents)
DiscordComponents(client)

@client.event
async def on_ready():
    file = open("niceto.who")
    niceto = file.readlines()
    niceto = [int(s.strip('\n')) for s in niceto]
    file.close()
    print(niceto)

@client.event
async def on_message(message):
    if "meow" in message.content.lower() and not str(message.author) == "mi haels bot#6905":
        await message.channel.send("meow")
    if message.content == "./ai on":
        global started
        if (started == 0):
            await message.delete()
            started = 1
            while (True):
                msg = input("message =>")
                await message.channel.send(msg)
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
    await client.process_commands(message)

@client.command()
async def owner(ctx):
    
    await ctx.message.delete()
    await ctx.channel.send(ctx.guild.owner.id)

@client.command(hidden=True)
async def nice(ctx):
    if int(ctx.author.id not in niceto):
        file = open('assets/textFiles/niceto.who', 'w+')
        lines = file.read()
        file.write(lines+ctx.author.id+"\n")
        on_ready()

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
async def mafia(ctx):
    channel = await ctx.guild.create_text_channel(name="mafia")
    players = []
    starttime = time.time()
    allowed_mentions = discord.AllowedMentions(everyone=True)
    await channel.send(content="@everyone There is a game of mafia happening! if you want to participate send a message in this channel!", allowed_mentions=allowed_mentions)
    await ctx.channel.send(content=f"the game is being held at {channel.mention}")
    while True:
        try:
            message = await client.wait_for('message', timeout=1)
            if message.author not in players and message.channel == channel and str(message.author) != "mi haels bot#6905":
                players.append(message.author)
            if time.time() - starttime > 60:
                raise TimeoutError
            print(message.channel == channel)
        except:
            if time.time() - starttime > 60:
                if len(players) >= 3:
                    playrs = f""
                    for player in players:
                        playrs += f"{player.mention} "
                    await channel.send(f"{playrs} are going to participate in this game")
                    break
                else:
                    await channel.send("not enough players joined. This game will close in 10 seconds")
                    await asyncio.sleep(10)
                    await channel.delete()
                    raise TimeoutError
    alive = players.copy()
    tnum = math.floor(len(players)/3)
    traitors = []
    detective = None
    doctor = None
    unassigned = players.copy()
    print(len(alive))
    print("players")
    print(len(players))
    for i in range(tnum):
        traitor = random.randint(0,(len(unassigned)-1))
        traitors.append(unassigned[traitor])
        unassigned.pop(traitor)
    if len(players) > 4:
        dnum = random.randint(0,(len(unassigned)-1))
        doctor = unassigned[dnum]
        unassigned.pop(dnum)
    if len(players) > 8:
        detective = random.choice(unassigned)
    for traitor in traitors:
        await traitor.send("You are part of the mafia! every night you vote on who dies next")
    for innocent in unassigned:
        await innocent.send("You are an innocent.... Hey at least you don't have to worry about dying..... right? The mafia are after you!")
    if doctor != None:
        await doctor.send("You are the doctor! You get to decide who you save every night from the mafia! This can even be yourself!")
    if detective != None:
        await detective.send("You are the detective! You get to see the role of one person every night!")
    print(traitors)
    print(doctor)
    print(detective)
    await channel.send("Everybody that has participated should have received a dm telling them their roles")
    nightnum = 0
    while True:
        nightnum += 1
        await channel.send(f"Night {nightnum}: Mafia please dm the bot who you wish to kill!")
        voted = []
        votes = []
        saved = None
        print(len(players))
        print(len(alive))
        for traitor in traitors:
            opts = f"```diff\n"
            for person in alive:
                if person not in traitors:
                    opts += (f"-{person}\n")
            opts += ("```")
            await traitor.send(f"choose which person you would like to off tonight! choices:\n{opts}\nsay their whole name with tag or just a partial of their name to choose!")
        starttime = time.time()
        while True:
            try:
                message = await client.wait_for('message', timeout=1)
                if message.author not in voted and message.author in traitors:
                    for person in alive:
                        if person not in traitors and str(message.content) in str(person):
                            votes.append(person)
                            await message.channel.send(f"{str(person)} chosen!")
                            voted.append(message.author)
                            break
                        elif person in traitors:
                            await message.channel.send(f"You can off your comrades!")
                    if message.author not in voted:
                        await message.channel.send("That is not a person!")
                if time.time() - starttime > 20:
                    raise TimeoutError
                #print(message.author)
            except:
                if time.time() - starttime > 30 or len(voted) == len(alive):
                    try:
                        dying = most_frequent(votes)
                    except:
                        dying = random.choice(alive)
                        for traitor in traitors:
                            if traitor in alive:
                                await traitor.send("Nobody voted on who to kill so I chose for you. This may also be one of you for your lack of compliance!")
                    break
        if detective in alive and detective != None:
            opts = f"```diff\n"
            for person in alive:
                opts += (f"-{person}\n")
            opts += "```"
            await channel.send(f"Detective please dm the bot who you want to see their role")
            await detective.send(f"{opts}\nplease say the full or partial of the name of who you want to see their role")
            while True:
                try:
                    detected = False
                    message = await client.wait_for('message', timeout=1)
                    if message.author == detective:
                        for person in alive:
                            if str(message.content) in str(person):
                                detected = True
                                if person in traitors:
                                    await ctx.author.send(f"{str(person)} is part of the mafia!")
                                elif person == doctor:
                                    await ctx.author.send(f"{str(person)} is a doctor!")
                                elif person in alive:
                                    await ctx.author.send(f"{str(person)} is innocent.")
                                else:
                                    await ctx.author.send(f"{str(person)} is dead....")
                        if not detected:
                            await message.channel.send("That is not a person!")
                    if time.time() - starttime > 20 or detected:
                        raise TimeoutError
                    #print(message.author)
                except:
                    if time.time() - starttime > 30 or detected:
                        break
        if doctor in alive and doctor != None:
            opts = f"```diff\n"
            for person in alive:
                opts += (f"-{person}\n")
            opts += "```"
            await channel.send(f"Doctor please dm the bot who you want to save")
            await doctor.send(f"{opts}\nplease say the full or partial of the name of who you want to save")
            while True:
                try:
                    detected = False
                    message = await client.wait_for('message', timeout=1)
                    if message.author == doctor:
                        for person in alive:
                            if str(message.content) in str(person):
                                detected = True
                                if person in alive:
                                    await ctx.author.send(f"{str(person)} chosen")
                                else:
                                    await ctx.author.send(f"{str(person)} is dead....")
                        if not detected:
                            await message.channel.send("That is not a person!")
                    if time.time() - starttime > 20 or detected:
                        raise TimeoutError
                    #print(message.author)
                except:
                    if time.time() - starttime > 30 or detected:
                        break
        if dying != saved:
            for i,player in enumerate(alive):
                if dying == player:
                    alive.pop(i)
                    break
            await channel.send(f"{dying.mention} was murdered! Who do you think is in the mafia?")
        else:
            await channel.send(f"{dying.mention} was almost murdered! But the doctor saved them. Who do you think is in the mafia?")
        opts = f"```diff\n"
        print(len(alive))
        for person in alive:
            opts += (f"+{person}\n")
        opts += ("```")
        await channel.send(f"Vote on who you think is in the mafia!\n{opts}\nsay their whole name or a partial of their name in here to choose")
        voted = []
        votes = []
        starttime = time.time()
        while True:
            try:
                message = await client.wait_for('message', timeout=1)
                if message.author not in voted and message.channel == channel and message.author in alive:
                    for person in alive:
                        if str(message.content) in str(person):
                            votes.append(person)
                            await message.channel.send(f"{str(person)} chosen!")
                            voted.append(message.author)
                    if message.author not in voted:
                        await message.channel.send(f"{message.author.mention}That is not a person!")
                if time.time() - starttime > 20:
                    raise TimeoutError
                #print(message.author)
            except:
                print("timout")
                if time.time() - starttime > 20:
                    try:
                        dying = most_frequent(votes)
                    except:
                        dying = None
                    break
        if dying != None:
            for i, player in enumerate(alive):
                if dying == player:
                    alive.pop(i)
                    break
            await channel.send(f"{dying.mention} was voted out!")
            if dying in traitors:
                await channel.send(f"{dying.mention} was a traitor!")
        tleft = 0
        ileft = 0
        for player in alive:
            if player in traitors:
                tleft += 1
            else:
                ileft += 1
        if tleft == 0:
            await channel.send("INNOCENTS WIN")
            break
        if ileft == 0:
            traits = f""
            for player in players:
                if player in traitors:
                    traits += f"{player.mention} "
            await channel.send(f"the traitors win! they were {traits}!")
            break
    await channel.send("The game has ended. This channel will delete in 10 seconds")
    #while True
    await asyncio.sleep(20)
    await channel.delete()

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
async def nuke(ctx, number=None):
    await ctx.message.delete()
    if number == None:
        await ctx.send("initiating nuke.....")
        time.sleep(5)
        await ctx.send("5")
        time.sleep(1)
        await ctx.send("4")
        time.sleep(1)
        await ctx.send("3")
        time.sleep(1)
        await ctx.send("2")
        time.sleep(1)
        await ctx.send("1")
        time.sleep(1)
        await ctx.send("say goodbye")
        time.sleep(5)

        await ctx.channel.purge()
    else:
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


client.run("NzkwNzY1NjU2NTcxMzc5NzYy.X-FX6A.9JOPvXnfoYvtd1G2RkwN79yDiXU")
