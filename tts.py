import discord
from discord.ext import commands
import biscuitfunctions as bf
import pyttsx3
import asyncio

engine = pyttsx3.init('espeak', debug=True)
voices = engine.getProperty('voices')
engine.setProperty('voice', 'en-scottish')
print(engine.getProperty('volume'))
engine.setProperty('rate', 100)

class _TTS:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self,text_):
        print("db1")
        self.engine.say(text_)
        print("db2")
        engine.save_to_file(text_, 'tts4.mp3')
        print("db3")
        self.engine.runAndWait()
        print("db4")
        print("done")

class textToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='tts',
        pass_context = True)
    async def tts(self, context, *args):
        if len(args) == 0:
            await context.send(f"Hey, {bf.authname(context)}, I can't say nothing! Gimme some words.")
        else:
            space = " "
            argstring = ""
            argstring = space.join(args)
        tts = _TTS()
        tts.start(argstring)
        guild = context.guild
        if guild.voice_client != None:
            await guild.voice_client.disconnect()
            return
        else:
            pass
        print("ttscheck5")
        vc = await context.author.voice.channel.connect()
        print("ttscheck6")
        vc.play(discord.FFmpegPCMAudio('tts4.mp3', options=f'-filter:a "volume=3"'),
        after = lambda e: print(f'Done remote playing tts string: {argstring}, errors: ', e))
        print("ttscheck8")
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        print("ttscheck9")
        await vc.disconnect()
        print("ttscheck10")
        await context.message.delete()
        del(tts)
        print("ttscheck11")
        
    @commands.command(
        name='tts2',
        pass_context=True)
    async def tts2(self, context, *args):
        if len(args) == 0:
            await context.send(f"Hey, {bf.authname(context)}, I can't say nothing! Gimme some words.")
        else:
            space = " "
            argstring = ""
            argstring = space.join(args)
        await context.send(f"{argstring}", tts=True, delete_after=15)

def setup(bot):
    bot.add_cog(textToSpeech(bot))
