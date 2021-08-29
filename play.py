from discord.ext import commands
import discord
import asyncio
import biscuitfunctions as bf

# songdict = MASTER SONG DICTIONARY
# aliasdict = alias dictionary
# def reloadsongdict(): read master song dictionary in from file
# songlist = list of song names

songdict = {'hello' : {'topname' : 'hello',
'filepath' : "/pythbot/Buttery_Biscuit_Bot/Music/hello.mp3",
'aliases' : ['darksoulshello'],
'category' : 'riff',
'protected' : True,
'duration' : 'short time',
'author' : 'tesseract',
'addtime' : '12/23/2020 1:36 pm',
'lastplay' : 'last play',
'playcount' : '500',
'volume' : '1'}
}

async def playsong(voice_connection, song):
    voice_connection.play(discord.FFmpegPCMAudio(f'{song["filepath"]}', options=f'-filter:a "volume={song["volume"]}"'),
    after = lambda e: print(f'Done playing {song["topname"]}, errors: ', e))
    while voice_connection.is_playing():
        await asyncio.sleep(1)
    voice_connection.stop()
    await voice_connection.disconnect()


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='play',
        aliases = ['p'],
        pass_context=True,
        description = 'Play a song from the song list in your current voice channel')
    async def play(self, context, *args):
        global songdict
        if context.author.voice != None:
            voice_connection = await context.author.voice.channel.connect()
        else:
            await context.send("Error, you're not in a voice channel, dumbass.")
        if len(args) == 0:
            await context.send("Sorry, songlist is temporarily down")
        elif args[0] == 'random':
            end = len(songlist)
            rnum = random.randint(0, end-1)
            song = songdict[songlist[rnum]]
            await context.message.delete()
            await playsong(voice_connection, song)
        elif len(args) == 1 and args[0] != 'random':
            if args[0] in songdict:
                song = songdict[args[0]]
                await playsong(voice_connection, song)
            elif args[0] in aliasdict:
                song = songdict[aliasdict[args[0]]]
                await playsong(voice_connection, song)
            else:

                await context.send("Play what? Uhh... Why don't you try again. (Try !play for a list of songs)")

def setup(bot):
    bot.add_cog(play(bot))