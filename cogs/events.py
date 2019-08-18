import discord
import asyncpg
import asyncio
import traceback
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#self.db = self.bot.db


	async def get_channel_count(self, guild_id):

		# Get the guild instance

		guild = self.bot.get_guild(guild_id)

		# Create empty variables for counting the text and voice channels
		text = 0
		voice = 0

		# Iterate through each channel in the guild.
		for channel in guild.channels:

			# Here we check for channel types. We want text- and voice channels. Since categories count as channels. We need to check each channel.

			# Check if the channel type is TextChannel
			if isinstance(channel, discord.TextChannel):

				# Add 1 to the text counter
				text += 1

			# Check if the channel type is VoiceChannel
			if isinstance(channel, discord.VoiceChannel):

				# Add 1 to the voice counter
				voice += 1

		# Return the values for the channel counts.
		return text, voice


	######## MEMBER COUNT vvvvvv

	@commands.Cog.listener()
	async def on_member_join(self, member):

		# Simple try/except
		try:

			# Assign the guild instance to a variable for ease of use.
			guild = member.guild

			# Try to get the category where the counters are.
			category = discord.utils.get(guild.channels, name="📈 Counters:")

			# If category returns a channel object.
			if category != None:

				# Iterate through channels inside the channel category
				for channel in category.channels:

					# Compare the channel name to our known "Member Counter:" channel name.
					if "member counter" in channel.name.lower():

						# If found, edit channel name to the updated member count.
						await channel.edit(name=f"Member Counter: [{guild.member_count}]")
						return
						
		except Exception as e:
			raise e

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		# Simple try/except
		try:

			# Assign the guild instance to a variable for ease of use.
			guild = member.guild

			# Try to get the category where the counters are.
			category = discord.utils.get(guild.channels, name="📈 Counters:")

			# If category returns a channel object.
			if category != None:

				# Iterate through channels inside the channel category
				for channel in category.channels:

					# Compare the channel name to our known "Member Counter:" channel name.
					if "member counter" in channel.name.lower():

						# If found, edit channel name to the updated member count.
						await channel.edit(name=f"Member Counter: [{guild.member_count}]")
						return
						
		except Exception as e:
			raise e
	######## MEMBER COUNT ^^^^^^

	######## CHANNEL COUNT vvvvvv
	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		if any("voice channels", "text channels", "member counter", "role counter") in channel.name.lower():
			return
		try:
			guild = channel.guild
			text, voice = await self.get_channel_count(guild.id)
			category = discord.utils.get(guild.channels, name="📈 Counters:")
			if category != None:
				for c in category.channels:
					if "voice channels" in channel.name.lower():
						await c.edit(name=f"Voice Channels: [{voice}]")
						return
					elif "text channels" in channel.name.lower():
						await c.edit(name=f"Text Channels: [{text}]")
						return

		except Exception as e:
			raise e

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		if any("voice channels", "text channels", "member counter", "role counter") in channel.name.lower():
			return
		try:
			guild = channel.guild
			text, voice = await self.get_channel_count(guild.id)
			category = discord.utils.get(guild.channels, name="📈 Counters:")
			if category != None:
				for c in category.channels:
					if "voice channels" in channel.name.lower():
						await c.edit(name=f"Voice Channels: [{voice}]")
						return
					elif "text channels" in channel.name.lower():
						await c.edit(name=f"Text Channels: [{text}]")
						return
		except Exception as e:
			raise e
	######## CHANNEL COUNT ^^^^^^

	####### ROLE COUNT vvvvvvv
	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		try:
			guild = role.guild
			text, voice = await self.get_channel_count(guild.id)
			category = discord.utils.get(guild.channels, name="📈 Counters:")
			if category != None:
				for c in category.channels:
					if "role counter" in c.name.lower():
						await c.edit(name=f"Role Counter: [{len(guild.roles)}]")
						return
		except Exception as e:
			raise e

	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		try:
			guild = role.guild
			text, voice = await self.get_channel_count(guild.id)
			category = discord.utils.get(guild.channels, name="📈 Counters:")
			if category != None:
				for c in category.channels:
					if "role counter" in c.name.lower():
						await c.edit(name=f"Role Counter: [{len(guild.roles)}]")
						return
		except Exception as e:
			raise e
	####### ROLE COUNT ^^^^^^^


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		"""The event triggered when an error is raised while invoking a command.
		ctx   : Context
		error : Exception"""

		# This prevents any commands with local handlers being handled here in on_command_error.
		if hasattr(ctx.command, 'on_error'):
			return
		
		ignored = (commands.CommandNotFound)
		
		# Allows us to check for original exceptions raised and sent to CommandInvokeError.
		# If nothing is found. We keep the exception passed to on_command_error.
		error = getattr(error, 'original', error)
		
		# Anything in ignored will return and prevent anything happening.
		if isinstance(error, ignored):
			return

		elif isinstance(error, commands.DisabledCommand):
			return await ctx.send(f'{ctx.command} has been disabled.')

		elif isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
			except:
				pass

		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.message.delete()
			cmd = ctx.command
			embed=discord.Embed(title=f'Missing required argument(s): `{error.param.name}`')
			params = cmd.signature.replace('<', '[').replace('>', ']')
			
			embed.description = f'Correct syntax: `{ctx.prefix}{cmd.name} {params}`'
			return await ctx.send(embed=embed, delete_after=20)

		# All other Errors not returned come here... And we can just print the default TraceBack.
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
	bot.add_cog(Events(bot))