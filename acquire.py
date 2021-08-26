from discord.ext import commands
import biscuitfunctions as bf

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


class acquire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='acquire',
        aliases = ['yoink'],
        pass_context = True,
        description = 'Acquire songs from youtube for playback with bot'
        )
    async def acquire(self, context, *args):
        await context.send("Sowwy, I can't acquire things cuz daddy is upgrading me")


def setup(bot):
    bot.add_cog(acquire(bot))