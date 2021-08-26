import discord
from discord.ext import commands
import biscuitfunctions as bf
import pyttsx3
import asyncio



voicelist = []
for voice in voices:
    voicelist.append(voice.name)
print(voicelist)

class textToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
            
    @commands.command(
        name='tts',
        pass_context = True)
    async def getid(self, context, *args):
        if len(args) == 0:
            await context.send(f"Hey, {bf.authname(context)}, I can't say nothing! Gimme some words.")
        else:
            space = " "
            argstring = ""
            argstring = space.join(args)
        print(argstring)
        engine = pyttsx3.init('espeak')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', 'en-scottish')
        print(engine.getProperty('volume'))
        engine.setProperty('rate', 100)
        print("ttscheck1")
        engine.save_to_file(argstring, 'tts2.mp3')
        print("ttscheck2")
        engine.runAndWait()
        print("ttscheck3")
        guild = context.guild
        print("ttscheck4")
        if guild.voice_client != None:
            await guild.voice_client.disconnect()
            return
        else:
            pass
        print("ttscheck5")
        vc = await context.author.voice.channel.connect()
        print("ttscheck6")
        vc.play(discord.FFmpegPCMAudio('tts2.mp3', options=f'-filter:a "volume=3"'),
        after = lambda e: print(f'Done remote playing tts string: {argstring}, errors: ', e))
        print("ttscheck8")
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        print("ttscheck9")
        await vc.disconnect()
        print("ttscheck10")
        await context.message.delete()
        print("ttscheck11")

def setup(bot):
    bot.add_cog(textToSpeech(bot))
