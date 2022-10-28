import discord
from discord.ext import commands

class Gui(discord.ui.view):
	def __init__(self):
		super().__init__()
		self.value = None
		self.v = 0

	@discord.ui.button(Label="atk", style=discord.ButtonStyle.red)
	async def atk(self, button: discord.ui.Button, interaction: discord.Interaction):
			self.v = not self.v
			print(self.v)
			await interaction.respinse.edit_message(self.v)








"""
@bot.command(
	name='fight',
	description='Lets you 1v1 somebody say ./fight for help on how to use this command',
)
async def fight(ctx, member: discord.User = None):
	if member == None:
		await ctx.send(corrupt("help message"))
		return
	if str(member) == "@everyone":
		await ctx.send(corrupt("Trust me pal your not that guy"))
		return
	message = await ctx.send(corrupt("fighting "+member.mention), components = [
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
	await message.edit(content = corrupt(f"{action}\n{ctx.author.mention}stats:\nhp: {provoker[0]}\natk: {provoker[1]}\ndef: {provoker[2]}\n---------------------------\n{member.mention} stats:\nhp: {victim[0]}\natk: {victim[1]}\ndef: {victim[2]}\n---------------------------\n{turnName}'s turn"))
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
"""