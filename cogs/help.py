import discord
from discord.ext import commands



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", brief="Shows all available commands")
    async def help(self, ctx):

        # Assign every cog and command into variables for ease of use.
        cogs = self.bot.cogs
        cmds = self.bot.commands


        # Create the embed object
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar_url)


        # Iterate through each cog name in cogs
        for cog in cogs:

            # Get the cog to access the commands.
            cog = self.bot.get_cog(cog)

            # Make an empty list var for later usage
            field_value = []

            # Iterate through all commands in the cog.
            for command in cog.get_commands():

                # Add the command name to the earlier made list var
                field_value.append(f'`{command.name}`')

            # Check if "commands list" is empty. If it is, it means no commands were in the cog and we dont need to add that cog to the help command.

            if field_value == []:
                pass
            else:
                # Add an embed field with cog's name as the "title" and command names as value
                embed.add_field(name=cog.qualified_name, value=", ".join(field_value), inline=False)

        embed.title = f'Help ({len(field_value)})' # We put len(field_value), because it will then show the amount of commands that are not hidden from normal people.
        
        # Send the help embed in the channel that the message was used.
        await ctx.send(embed=embed)


def setup(bot):

    # Remove the default help command.
    bot.remove_command("help")

    # Add the class to the bot
    bot.add_cog(Help(bot))
