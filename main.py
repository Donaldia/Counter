#MIT License

#Copyright (c) 2019 Donaldia

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
