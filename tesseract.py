import discord
from discord.ext import commands
import biscuitfunctions as bf
import asyncio

async def tesstest(context):
    print(dir(context))
    await context.send("This was a test. I passed")

async def is_tesseract(context):
    return context.author.id == 97172418258280448

class tesseract(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
    async def cog_check(self, context):
        return context.author.id == 97172418258280448
        """
    async def cog_command_error(self, context, error):
        if isinstance(error, commands.errors.CheckFailure):
            await context.send("You can't make me, you're not my dad! (Only tesseract can do that).")
    """
    @commands.command(
        name = 'trongsemble',
        pass_context = True)
    async def trongsemble(self, context):
        await context.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/trongsemble.png'))
        
        
    @commands.command(
        name='troubleshoot',
        pass_context=True)
    async def troubleshoot(self, context):
        print(self.bot.extensions)
#        print("context is: ", context)
#        print("context dir is:", dir(context))
#        print("context.channel is: ", context.channel)
#        print("context.channel dir is:", dir(context.channel))
#        print("context.author is: ", context.author)
#        print("context.message is: ", context.message)
#        print("context message dir is: ", dir(context.message))
#        print("context.guild is: ", context.guild)
#        print("context.guild dir is: ", dir(context.guild))
#        print("context.guild.channels is: ", context.guild.channels)
#        print("context.guild.channels dir is: ", dir(context.guild.channels))
#        
#        print("context.author.nick is: ", context.author.nick)
#        print("context.author dir:", dir(context.author))
#        print("context.author.roles is: ", context.author.roles)
#        print("context.author.roles dir is: ", dir(context.author.roles))
#        await context.author.send(str(context.author.roles))
#        print("context.author.voice is: ", context.author.voice)
#        print("context.author.voice.channel is", context.author.voice.channel)
#        print("context.author.voice.channel dir is", dir(context.author.voice.channel))
#        print("context.author.voice.channel.members is: ", context.author.voice.channel.members)
#        for x in BOT.voice_clients:
#            print("connected voice client: ", bot.voice_clients)
#            await context.message.channel.send(str(x.channel))
#        await context.author.send(f"context.guild.id is: {str(context.guild.id)}")
#        for x in self.bot.voice_clients:
#            print("voice client.channel: ", x.channel)
#            print("dir voice_client: ", dir(x))
#            await x.disconnect()
#            print(f"{x} disconnected")


    @commands.command(
        name='pins',
        pass_context=True)
    async def pins(self, context, *args):
        user = args[0]
        pinned = await context.pins()
        for x in pinned:
            if x.author.name == user:
                await context.author.send(x.author.id)
                
                
    @commands.command(
        name='channelinfo',
        pass_context=True)
    async def channelinfo(self, context):
        await context.author.send(f"dir for {context.message.channel}:")
        await context.author.send(",".join(dir(context.message.channel)))
        await context.author.send(context.message.channel.id)
        await context.message.delete()

    @commands.command(
        name='tessplay',
        aliases = ['tplay'],
        pass_context = True)
    async def tessplay(self, context, *args):
        bobbylobby = self.bot.get_channel(98542453115621376)
        songname = args[0]
        songdict = bf.readdictjson('mastersonglist')
        if songname in songdict:
            song = songdict[songname]
            pass
        else:
            await context.author.send(f"Filename error, could not find {songname} (remember, only topnames)")
            return
        quaidguild = self.bot.get_guild(98542453052706816)
        if quaidguild.voice_client != None:
            await quaidguild.voice_client.disconnect()
        else:
            pass
        await context.author.send(f"remote playing {songname} in bobby lobby")
        vc = await bobbylobby.connect()
        vc.play(discord.FFmpegPCMAudio(f'{song["filepath"]}', options=f'-filter:a "volume={song["volume"]}"'),
        after = lambda e: print(f'Done remote playing {song["topname"]}, errors: ', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        await vc.disconnect()
        
    @commands.command(
        name="post",
        pass_context=True)
    async def post(self, context, *args):
        args2 = list(args)
        location = args2.pop(0)
        locdict = {"quaid" : 98542453052706816, "biscuit" : 677741161611395078}
        location_id = locdict[location]
        say = " ".join(args2)
        channel = self.bot.get_channel(location_id)
        await channel.send(say)
        
98542453052706816
def setup(bot):
    bot.add_cog(tesseract(bot))