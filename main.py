import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="c!")


startup_extensions = ["cogs.events", "cogs.counter", "cogs.admin", "cogs.help"]


@bot.event
async def on_ready():
    print('Online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"c!help"))


if __name__ == "__main__":
    
    bot.load_extension('jishaku')
    print('Succesfully loaded jsk')
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Succesfully loaded ' + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n[{}]'.format(extension, e))
            raise e

bot.run(token)
