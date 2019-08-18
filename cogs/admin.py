import discord
import os
from discord.ext import commands
import time
from contextlib import redirect_stdout
import sys
import io
import json
import speedtest
import asyncio
import textwrap
import traceback
import time

async def isDonald(ctx):
    return ctx.author.id == 289890066514575360

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None


    @commands.command(name="say", brief="Repeats text sent by user.", usage="say <content>", aliases=['echo'], hidden=True)
    @commands.check(isDonald)
    async def say(self, ctx, *, content:str):

        """Repeats content sent by the Author. Checks for one of the admin permissions"""

        await ctx.send(content)



    def cleanup_code(self, content):
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])


    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.check(isDonald)
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        # This eval is taken fon R.Danny discord bot. https://github.com/Rapptz/RoboDanny

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    bot.add_cog(Admin(bot))
