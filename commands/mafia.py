
import time,asyncio,math,random
import discord

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


async def mafia(ctx, client):
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