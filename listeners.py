from discord.ext import commands
import csv
import random
import discord
import asyncio
import biscuitfunctions as bf


fromrestart = bf.readcsvtodict('restart')

print(fromrestart)

introdict = {97172418258280448 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/tessboyos.mp3", 'volume' : "4", "user" : "tesseract"},
101462910349381632 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/welcome.mp3", 'volume' : "2", "user" : "gonnjeppi"},
97171583524691968 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/queen.mp3", 'volume' : "0.5", "user" : "attolias"},
97171421553233920 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/Jarrier.mp3", 'volume' : "1.5", "user" : "RedJar"},
98542595751288832 : {'path' : "/pythbot/Buttery_Biscuit_Bot/welcomebackpilot.mp3", 'volume' : "2", "user" : "formyndare"},
97171512729014272 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/aaron.mp3", 'volume' : ".75", "user" : "quaid"},
280833155148021773 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/thelarch.mp3", 'volume' : "6", "user" : "thelarch"},
100412818922168320 : {'path' : "/pythbot/Buttery_Biscuit_Bot/Music/bobbyintro.mp3", 'volume' : "1", "user" : "mdman2014"}
}
# "/pythbot/Buttery_Biscuit_Bot/Music/northstarprime.mp3" OLd tesseract intro

class listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        botlogdict = {"quaid" : self.bot.get_channel(742482393587515555), "biscuitlog" : self.bot.get_channel(739510798099152916)}
        print(f"{self.bot.user} has connected to Discord!")
        if fromrestart['restart'] == 'true':
            await botlogdict['biscuitlog'].send("Restarted successfully! Yay, I'm back!")
            newstart = {'restart' : 'false'}
            bf.writedictcsv(newstart, 'restart')
        print("GNU Sir Terry Pratchett")
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        auth1 = bf.authname(message)
        callresponsedict = {
        'hell': 'Yeah Dog!',
        'uwu': 'Hewwwwoo~~',
        'bb': 'BOBBBBBYYYYYYY',
        'bee': 'BEE-THEMED STRIPPERS!!',
        'kiddy': 'hey there ya dingus',
        'salmonelle' : 'chicken',
        'bad bot' : ['i\'ve been a bad bot daddy, i need spanking', '*pees on floor* is that better?!?'],
        'good bot': [f'*blushes* th..thank you senpai-{auth1} uwu', 'awww, stahp :blush:', f'you\'re a pretty good bot too, {auth1}'],
        'coggy bot' : 'My cogs are turning! Thanks, dad!',
        'sandwich' : "Don't start that shit again please",
        'sammich' : "Oh god, this shit again",
        'burrito' : "Not the fucking sandwich debate",
        'taco' : "Seriously Jacob, tacos are not sandwiches",
        'hotdog' : "Hotdogs are not a sandwich",
        'discworld' : "GNU Sir Terry Pratchett",
        'thelarch' : {'path' : '/pythbot/Buttery_Biscuit_Bot/pictures/lucashorrific.png'}
        }
        lowermessage = message.content.lower()
        for key in callresponsedict:
            if key in lowermessage:
                value = callresponsedict[key]
                if type(value) == list:
                    length = len(value) - 1
                    response = value[random.randint(0,length)]
                elif type(value) == dict:
                    print(value["path"])
                    await message.channel.send("Here's my favorite artwork from thelarch :", file=discord.File(value["path"]))
                    return
                else:
                    response = value
                await message.channel.send(response)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id in introdict:
            if before.channel is None and after.channel is not None:
                if after.channel.id == 98545878125547520:
                    return
                else:
                    voice_connection = await after.channel.connect()
                    voice_connection.play(discord.FFmpegPCMAudio(f'{introdict[member.id]["path"]}', options=f'-filter:a "volume={introdict[member.id]["volume"]}"'),
                                        after=lambda e: print('done', e))
                    while voice_connection.is_playing():
                        await asyncio.sleep(1)
                    voice_connection.stop()
                    await voice_connection.disconnect()
        else:
            return

def setup(bot):
    bot.add_cog(listener(bot))