import discord
import asyncpg
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

async def isOwner(ctx):
	return ctx.author.id == 289890066514575360 or ctx.author == ctx.guild.owner

class Counter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def get_channel_count(self, guild_id):
		guild = self.bot.get_guild(guild_id)
		text = 0
		voice = 0
		for channel in guild.channels:
			if isinstance(channel, discord.TextChannel):
				text += 1
			if isinstance(channel, discord.VoiceChannel):
				voice += 1
		return text, voice


	@commands.command("start")
	@commands.check(isOwner)
	async def _start(self, ctx):
		guild = ctx.guild
		text, voice = await self.get_channel_count(guild.id)
		category = discord.utils.get(guild.channels, name="📈 Counters:")
		if category == None:
			category = await guild.create_category('📈 Counters:', reason="Created by Counter bot for stat counters.")
			perms = {
				guild.default_role: discord.PermissionOverwrite(connect=False),
			}
			await category.edit(position=0)
			category = guild.get_channel(category.id)
			await category.create_voice_channel(f'Member Counter: [{guild.member_count}]', overwrites=perms)
			await asyncio.sleep(0.1)
			await category.create_voice_channel(f'Role Counter: [{len(guild.roles)}]', overwrites=perms)
			await asyncio.sleep(0.1)
			await category.create_voice_channel(f'Voice Channels: [{voice}]', overwrites=perms)
			await asyncio.sleep(0.1)
			await category.create_voice_channel(f'Text Channels: [{text}]', overwrites=perms)
			await ctx.send('Done!')
		else:
			return ctx.send('You already have the counters.')

	@commands.command("stop")
	@commands.check(isOwner)
	async def _stop(self, ctx):
		guild = ctx.guild
		category = discord.utils.get(guild.channels, name="📈 Counters:")
		if category != None:
			for channel in category.channels:
				await channel.delete()
			await category.delete()
			await ctx.send('I\'ve stopped the counters and deleted the channels. If you want to start it back up again. Please do `c!start`')
		else:
			await ctx.send('You have not started the counters. Please do `c!start` if you wish to see your guilds statistics')
	@commands.command()
	@commands.check(isOwner)
	@commands.cooldown(1,5,BucketType.guild) 
	async def update(self, ctx):
		guild = ctx.guild
		text, voice = await self.get_channel_count(guild.id)
		category = discord.utils.get(guild.channels, name="📈 Counters:")
		if category == None:
			return await ctx.send('Please do `c!start` to start up the counters')
		else:
			for c in category.channels:
				if "role counter" in c.name.lower():
					await c.edit(name=f"Role Counter: [{len(guild.roles)}]")
				elif "member counter" in c.name.lower():
					await c.edit(name=f"Member Counter: [{guild.member_count}]")
				elif "voice channels" in c.name.lower():
					await c.edit(name=f"Voice Channels: [{voice}]")
				elif "text channels" in c.name.lower():
					await c.edit(name=f"Text Channels: [{text}]")
			await ctx.send('Done! I\'ve updated all the stats.', delete_after=20)


def setup(bot):
	bot.add_cog(Counter(bot))
