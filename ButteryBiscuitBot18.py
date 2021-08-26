"""
Buttery Biscuit Bot!

Chat reply basics: https://pythonprogramming.net/discordpy-basic-bot-tutorial-introduction/
More in depth guide: https://realpython.com/how-to-make-a-discord-bot-python/
Every audio guide I found had various non-working function calls, so I had to build that mostly
just by reading the api. Let me know if you have questions, but the code block should be pretty
easy to copy for new mp3's.

API: https://discordpy.readthedocs.io/en/latest/api.html
Bot API: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
^Note that the bot is a subclass of client, so can do anything that the client can (just switch
client.whatever to bot.whatever)

In general, any api functions that are a 'coroutine' will need an 'await' or they'll probably
get skipped on execution as the next block of code will just go ahead and run.

See README.txt for necessary libraries etc...

To run - navigate to bot's directory in cmd, then enter:
python ButteryBiscuitBot.py
Or for the server:
python3.8 ButteryBiscuitBot.py
"""


from __future__ import unicode_literals
import os
import asyncio # Needed for coroutine / await functionality, which discord.py is built around.
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import psutil
import logging
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import csv
import youtube_dl
import pathlib
import random
import ffmpeg
from pydub import AudioSegment


#--------------------INITIALIZATION PRINT COMMANDS-------------

biscuitchannel = 742482393587515555
print("biscuit channel: ", biscuitchannel)

botlog = 739510798099152916
print("bot log: ", botlog)

# prints current working filepath
print("filepath: ", pathlib.Path(__file__).parent.absolute())


# prints current song list read from songlist2.csv
with open('/pythbot/Buttery_Biscuit_Bot/songlist2.csv',mode='r') as infile:
    BEAUTIFULSONGS = dict(csv.reader(infile))
# print("BEAUTIFULSONGS: ", BEAUTIFULSONGS)

# reads in the protected csv list
with open('/pythbot/Buttery_Biscuit_Bot/protected.csv',mode='r') as infile:
    protectedsonglist = dict(csv.reader(infile))
# print("protected songs: ", protectedsonglist)


# a method to tell if bot was started from !restart command
with open('/pythbot/Buttery_Biscuit_Bot/restart.csv',mode='r') as infile:
    fromrestart = dict(csv.reader(infile))

print(fromrestart)

# function to write a dictionary to CSV
def writedictcsv(dictionary, filename):
    filepath = "/pythbot/Buttery_Biscuit_Bot/" + filename + ".csv"
    w = csv.writer(open(filepath, "w"))
    for key, val in dictionary.items():
        w.writerow([key, val])
        # print(key, val)
        
newstart = {'restart' : 'false'}

writedictcsv(newstart, 'restart')


beautifulsongs2 = {}
def makenewsongdict():
    for x in BEAUTIFULSONGS:
        tempdict = {}
        tempdict.clear()
        tempdict.update([
            ('topname', x),
            ('filepath', BEAUTIFULSONGS[x]),
            ('aliases', None),
            ('protected', True),
            ('duration', 'UNK'),
            ('author', 'UNK'),
            ('addtime', 'UNK'),
            ('lastplay', 'UNK'),
            ('playcount', 0)]
            )
        beautifulsongs2.update({x: tempdict})
    #print(beautifulsongs2)


# defines global string songnames to store all songnames

songlisttemp = list(BEAUTIFULSONGS.keys())
songlist = sorted(songlisttemp)
#print("songlist :", songlist)
# print("type: ", type(songlist))

songstringlist = []

def makesongstring():
    songlisttemp = list(BEAUTIFULSONGS.keys())
    songlist = sorted(songlisttemp)
    songstringlist = []
    tempsongstring = ""
    for x in songlist:
        #print("tempsongstring ", len(tempsongstring))
        #print("len x", len(x))
        if len(tempsongstring) + len(x) < 1950:
            tempsongstring += f"{x}, "
            #print("tss: ", tempsongstring)
        else:
            #print("tss: ", tempsongstring)
            tempsongstring = tempsongstring[:-2]
            songstringlist.append(tempsongstring)
            #print("songstringlist: ", songstringlist)
            tempsongstring = ""
            tempsongstring += f"{x}, "
    tempsongstring = tempsongstring[:-2]
    songstringlist.append(tempsongstring)
    return songstringlist
    #print("songstringlist: ", songstringlist)


mastersongstringlist = makesongstring()
#print(mastersongstringlist)


#songstring = ', '.join(songlist)


adminfuncdict = {"makesongstring" : makesongstring,
    "makenewsongdict" : makenewsongdict
}
        
# makes songlist at the beginning
# makesonglist()

# print("songnames =", songnames)


#print version of discord api
print("discord api version: ", discord.__version__)




#-----------------Admin Function Dictinary--------------

#async def printtextchannelid(context):
#    print(context.message)
    

# functiondict = {
#    'printtextchannelid':'await printtextchannelid(context)'
#}


#----------------------------------Initialize Bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT = commands.Bot(command_prefix="!")

bc = BOT.get_channel(biscuitchannel)
bl = BOT.get_channel(botlog)

#-------------------------------Restart Bot command--------------------------
@BOT.command(
    name='restart',
    description='restart bot, role limited',
    pass_context=True,
)
@commands.has_role('Quaid')
async def restart_program(context):
    bc = BOT.get_channel(botlog)
    await bc.send("Restarted by " +  str(context.message.author))
    newstart['restart'] = 'true'
    writedictcsv(newstart, 'restart')
    for x in BOT.voice_clients:
        await x.disconnect()
        
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)
#@restart_program.error
#async def restart_error(context, error):
#    if isinstance(error, commands.MissingRole):
#        await context.message.channel.send("Error, you do not have permission to restart me.")

#-------------------------------Stop Bot command--------------------------

# Moved to cog/extension

#-------------------------------Tesseract Specific commands-----------------


@BOT.command(
    name='funcdict',
    pass_context=True)
@commands.is_owner()
async def funcdict(context, *args):
    adminfuncdict[args[0]]()
    print("executing: ", args[0])

# --------------- VOLUME COMMANDS -------------------------------
#@BOT.command(
#    name='playvol',
#    pass_context=True)
#async def playvol(context, *args):
#    filename = args[0]
#    volume = args[1]
#    voice_channel = await get_current_voice_channel_instance(context)
#    voice_channel_connection = await voice_channel.connect()
#    voice_channel_connection.play(discord.FFmpegPCMAudio(BEAUTIFULSONGS[filename], options=f'-filter:a "volume={volume}"'),
#                                      after=lambda e: print('done', e))

#------------------------------Picture Zone!-----------------------------

# Moved to cog/extension pictures

#------------------------------Mp3 command zone!-----------------------------

#--------------------TESTING !PLAY COMMAND---------------------------

@BOT.command(
    name='play',
    aliases=['Play', 'p', 'song', 'Song', 'PLAY'],
    description='Play a song from known song list',
    pass_context=True,
)
async def play(context, *args):
    print("check1", datetime.now())
    # In order to try to troubleshoot why it breaks sometime I'm adding a ton of prints with timestamps
    # I hope it's in the play command.
    bc = BOT.get_channel(biscuitchannel)
    bl = BOT.get_channel(botlog)
    print("check2", datetime.now())
    if len(args) == 0:
        print("check3", datetime.now())
        #print("we are here")
        #songlistmessage = "Here's a list of songs I can play: \n" + songstring
        # print("type of songlistmessage:", type(songlistmessage))
        i = 1
        for x in mastersongstringlist:
            stringnumbers = len(mastersongstringlist)
            #print(stringnumbers)
            songmessage = f"Here's a list of songs I can play ({i}/{stringnumbers}): \n {x}"
            #print(songmessage)
            await context.message.channel.send(songmessage)
            i += 1
        #await context.message.channel.send(songlistmessage)
        print("check4", datetime.now())
        return
    else:
        print("check5", datetime.now())
        pass
    if args[0] == 'random':
        print("check6", datetime.now())
        #print("args is random")
        randomsong = True
    else:
        print("check7", datetime.now())
        randomsong = False
    if len(args) == 1 and randomsong == False:
        print("check8", datetime.now())
        filename = args[0]
        try:
            songpath = BEAUTIFULSONGS[filename]
            print("check9", datetime.now())
        except KeyError:
            print("check10", datetime.now())
            errmessage = filename + " is not a song, try !play for a list of songs"
            await context.message.channel.send(errmessage)
            return
        await context.message.delete()
        print("check11", datetime.now())
        #print("message deleted")
        #print(bc)
        await bc.send("Now playing " + args[0] + " on behalf of " + str(context.message.author))
        await bl.send("Now playing " + args[0] + " on behalf of " + str(context.message.author))
        await play_mp3(BEAUTIFULSONGS[filename], VALIDTEXTCHANNELS, context)
        print("check12", datetime.now())
    elif randomsong == True:
        end = len(songlist)
        #print(end)
        rnum = random.randint(0,end-1)
        #print(rnum)
        songname = songlist[rnum]
        #print(songname)
        await context.message.delete()
        await play_mp3(BEAUTIFULSONGS[songname], VALIDTEXTCHANNELS, context)
        await bc.send("Randomly playing " + songname + " on behalf of " + str(context.message.author))
        await bl.send("Randomly playing " + songname + " on behalf of " + str(context.message.author))
    else:
        await context.message.channel.send("Play what? Uhh... Why don't you try again.(Try !play for a list of songs)")
#@play.error
#async def play_error(context, error):
#    if isinstance(error, commands.CommandInvokeError):
#        await context.message.channel.send("Chill out dude, I'm playing something already")

#--------------------------------------



#--------------------------ADD VIA YOUTUBE----------
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


async def checkurl(url, filelocation, context):
    ydl_opts = {
    'format': '[filesize<7.5M]bestaudio/best',
    'extractaudio':True,
    'audioformat':'mp3',
    'outtmpl':filelocation,
    'noplaylist':True,
    'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality':'192',
    }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # print("in with statement")
            infodict = ydl.extract_info(url, download=False)
            # print(infodict)
            duration = infodict["duration"]
            # print("duration:", fragments)
            if duration <= 600:
                return True
            else:
                await context.message.channel.send("This vid is way too long dude, it's " + str(duration) + " seconds.  Find something shorter!")
                return False
    except:
        await context.message.channel.send("Can't download that, check your url.")
        return False
        
async def checksongname(name, context):
    # checks if a song name exists
    # returns false if no, true if yes
    if name == 'random':
        await context.message.channel.send("Yo, random isn't okay, it's how I play random songs for people.")
        return True
    try:
        BEAUTIFULSONGS[name]
        await context.message.channel.send("That song already exists, choose a different name")
        return True
    except:
        return False

@BOT.command(
    name='acquire',
    aliases=['add', 'download', 'yoink'],
    description = 'Download a song from youtube and add it to the known song list',
    pass_context = True)
@commands.has_any_role('Quaid', 'Quaidling')
async def acquire(context, *args):
    argnum = len(args)
    attachnum = len(context.message.attachments)
    attach = False
    youtube = False
    needtrim = False
    if argnum == 0:
        await context.message.channel.send("You gotta gimme something to acquire dumbie")
        return
    elif argnum == 1:
        attach = True
        print("attach is ", attach)
    elif argnum == 2:
        youtube = True
        link = args[1]
        print("youtube is ", youtube)
    else:
        await context.message.channel.send("Could not parse your arguments")
    filename = args[0]
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'


    if attach == True and await checksongname(filename, context) == False:
        attachment = context.message.attachments[0]
        await attachment.save(filelocation)
        # reupdates the songnames so !play shows the updated list
        BEAUTIFULSONGS[filename] = filelocation
        # writes the songlist to the csv after updating
        writedictcsv(BEAUTIFULSONGS, "songlist2")
        # says message in channel to say it's done
        mastersonglist = makesongstring()
        await context.message.channel.send("Successfully downloaded " + filename + "\n It is ready to play")
        return
    else:
        pass

    if await checksongname(filename, context) == True:
        return
    elif filename == 'random':
        await context.message.channel.send("Yo, random is taken, choose something else")
        return
    else:
        pass
    if await checkurl(link, filelocation, context) == True:
        pass
    else:
        return
    # debugging print statements
    # print("type :", type(filename))
    # print("type :", type(link))
    # print(starttime, type(starttime))
    # print(endtime, type(endtime))
    # print("filelocation: ", filelocation)
    
    # actually download the song
    if needtrim == False:
        await downloadmp3(link, filename, filelocation)
    else:
        tempname = 'tempname'
        temploc = '/pythbot/Buttery_Biscuit_Bot/Music/temp.mp3'
        await downloadmp3(link, tempname, temploc)
        await pydubtrim(temploc, filelocation, starttime, endtime)
        #os.remove(temploc)
        print("purged temploc")
        
    # reupdates the songnames so !play shows the updated list
    
    BEAUTIFULSONGS[filename] = filelocation
    # writes the songlist to the csv after updating
    writedictcsv(BEAUTIFULSONGS, "songlist2")
    # says message in channel to say it's done
    songlist = list(BEAUTIFULSONGS.keys())
    songstring = ', '.join(songlist)
    if needtrim == False:
        await context.message.channel.send("Successfully downloaded " + filename + "\n It is ready to play")
    else:
        await context.message.channel.send("Successfully downloaded and trimmed " + filename + "\n It is ready to play")
#@acquire.error
#async def acquire_error(context, error):
#    if isinstance(error, commands.MissingAnyRole):
#        await context.message.channel.send("Error, you cannot acquire things.")
#    else:
#        print(error)






#-------------Download MP3 from YT func------------

async def downloadmp3(link, filename, filelocation):
    ydl_opts = {
    'format': '[filesize<7.5M]bestaudio/best',
    'extractaudio':True,
    'audioformat':'mp3',
    'outtmpl':filelocation,
    'noplaylist':True,
    'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality':'192',
    }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        downloadresult = ydl.download([link])
        BEAUTIFULSONGS[filename] = filelocation
    print("finished download")


#-----------------Trim MP3 test------------------------------
# define a function to run a bash command to use ffmpeg via cli
# honestly no fucking idea if this'll work right
"""
async def runbash(command):
    os.system(command)
"""
"""
async def trim(input, output, starttime, endtime):
    str = "ffmpeg -i " + input + " -ss " + starttime + " -to " + endtime + " -c copy " + output
    print(str)
    await runbash(str)
"""
    
"""
async def alttrim(fileinput, fileoutput, starttime, endtime):
    print(fileinput)
    print(fileoutput)
    print(starttime)
    print(endtime)
    clip = ffmpeg.input(fileinput, v=0, a=1)
    print("clip: ", clip)
    trim = clip.trim(start=starttime, end=endtime)
    output = trim.output(fileoutput)
    print(output.compile())
    output.run()
    print("trimmed")
"""
async def pydubtrim(fileinput, fileoutput, starttime, endtime):
    startms = int(starttime*1000)
    endms = int(endtime*1000)
    print("type: ", type(startms))
    print("type: ", type(endms))
    clip = AudioSegment.from_file(fileinput)
    extract = clip[startms:endms]
    extract.export(fileoutput, format="mp3")



#---------------------Protect and Remove Song Commands --------------

@BOT.command(
    name='removesong',
    description='Removed a song from playlist as long as it is not protected',
    aliases = ['remove', 'Remove', 'Removesong', 'yeet', 'Yeet'],
    pass_context=True)
@commands.has_any_role('Quaid', 'Quaidling')
async def removesong(context, *args):
    # takes context and the name of a song
    # takes the filename from the args
    filename = args[0]
    #creates the location of the mp3 file from the name
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'

    # checks if song is in protected songlist
    if filename in protectedsonglist:
        await context.message.channel.send("Cannot delete " + filename + " because it is protected.")
        return
    else:
        pass
    
    # Checks if file exists then removes it, otherwise responds with error in discord
    if os.path.exists(filelocation):
        os.remove(filelocation)
    else:
        await context.message.channel.send("Error, song file does not exist, purging from song list")
        pass
        
    # tries to delete it from the BEAUTIFULSONGS dictionary
    # if it cannot then responds with error in discord
    if filename in BEAUTIFULSONGS:
        del BEAUTIFULSONGS[filename]
        writedictcsv(BEAUTIFULSONGS, 'songlist2')
        print(BEAUTIFULSONGS)
    else:
        await context.message.channel.send("Error, song name does not exist.")
        return
    # remakes songnames which should no longer contain the deleted song
    songlist = list(BEAUTIFULSONGS.keys())
    mastersongstringlist = makesongstring()
    print(mastersongstringlist)
    await context.message.channel.send(filename + "has been deleted")
#@removesong.error
#async def removesong_error(context, error):
#    if isinstance(error, commands.MissingAnyRole):
#        await context.message.channel.send("Error, you cannot remove things.")
#    else:
#        print(error)


# Force remove command to remove protected songs

@BOT.command(
    name='forceremove',
    description='Quaid only command to force remove',
    aliases=['forceremovesong'],
    pass_context=True,
)
@commands.has_role('Quaid')
async def forceremove(context, *args):
    
    # takes context and the name of a song
    fileexist = False
    listexist = False
    
    # takes the filename from the args
    filename = args[0]
    #creates the location of the mp3 file from the name
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'

    # Checks if file exists then removes it, otherwise responds with error in discord
    if os.path.exists(filelocation) == True:
        print("removing file")
        os.remove(filelocation)
    else:
        await context.message.channel.send("Error, song file does not exist, purging from song list")
        
    # tries to delete it from the BEAUTIFULSONGS dictionary
    # if it cannot then responds with error in discord
    try:
        del BEAUTIFULSONGS[filename]
        writedictcsv(BEAUTIFULSONGS, 'songlist2')
    except KeyError:
        await context.message.channel.send("Error, song name does not exist.")
        return
    # remakes songnames which should no longer contain the deleted song
    
    songlist = list(BEAUTIFULSONGS.keys())
    mastersongstringlist = makesongstring()
    print(mastersongstringlist)
    await context.message.channel.send("Song " + filename + " has been deleted")
@forceremove.error
async def forceremove_error(context, error):
    if isinstance(error, commands.MissingRole):
        await context.message.channel.send("Error, you cannot remove things.")
    else:
        print(error)

#--------------------------

@BOT.command(
    name='protectsong',
    aliases = ['protect', 'Protect', 'Protectsong', 'ProtectSong'],
    description = 'Protect a song so that it cannot be removed',
    pass_context=True,
)
@commands.has_role('Quaid')
async def protectsong(context, *args):
    # checks if user has quaid
    if await checkquaid(context) == True:
        pass
    else:
        return
    # defines filename from args
    filename = args[0]
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'
    # writes filename to dictionary protected
    protectedsonglist[filename] = filelocation
    # writes new protected dictionary to csv
    writedictcsv(protectedsonglist, 'protected')
    # messages in discord to confirm
    await context.message.channel.send(filename + " is now protected")
@protectsong.error
async def protectsong_error(context, error):
    if isinstance(error, commands.MissingRole):
        await context.message.channel.send("Error, you cannot protect things.")
    else:
        print(error)


#-----------------------Play mp3 files----------------------------------
async def play_mp3(mp3_file_path, channel_names, context):
    """
    Plays an mp3 that passed as an arg

    Parameters
    ----------
    first : mp3_file_path
        The filepath of the mp3 to be played
    second : channel_names
        The channels where music can be played
    third : context
        The context of the bot

    Returns
    -------
    void

    Raises
    ------
    Does Not Error
    """
    # Only play music if user is in a voice channel
    # checks if file exists, if not messages in discord and returns, else continues
    if os.path.exists(mp3_file_path) == False:
        await context.message.channel.send("Error, I can't find a file called that")
        return
    else:
        pass
    print("playing: ", mp3_file_path, " at ", datetime.now())
    print("check13", datetime.now())
    if await is_user_in_channel(context, channel_names):
        # Connect to voice chat and play .mp3
        voice_channel = await get_current_voice_channel_instance(context)
        print("check14", datetime.now())
        voice_channel_connection = await voice_channel.connect()
        print("check15", datetime.now())
        voice_channel_connection.play(discord.FFmpegPCMAudio(mp3_file_path),
                                      after=lambda e: print('done', e))
        print("check16", datetime.now())
        # Wait for music to finish
        while voice_channel_connection.is_playing():
            await asyncio.sleep(1)
        print("check17", datetime.now())
        # Disconnect after music stops
        voice_channel_connection.stop()
        print("check18", datetime.now())
        await voice_channel_connection.disconnect()
        print("check19", datetime.now())
    else:
        #await context.message.channel.send('User is not in a voice channel.')
        return

async def is_user_in_channel(context, channel_names):
    """
    Grab the user who sent the command and the voice channel they are in, checks if the
    user is in a channel that's allowed to play music

    Parameters
    ----------
    first : context
        The context of the bot
    second : channel_names
        The channels where music can be played

    Returns
    -------
    boolean

    Raises
    ------
    Does Not Error
    """
    
    
    try:
        voice_channel = await get_current_voice_channel_instance(context)
    except AttributeError:
        #if user is not in a voice channel assign voice_channel to None so the lower if statement handles the error correctly
        voice_channel = None
        await context.message.channel.send('User is not in a voice channel.')
        return False
    if voice_channel.name in channel_names:
        return True
    else:
        await context.message.channel.send('I cannot join that channel idiot')
        return False



async def get_current_voice_channel_instance(context):
    """
    Grab the user who sent the command and the voice channel they are in

    Parameters
    ----------
    first : context
        The context of the bot

    Returns
    -------
    the voice_channel of the user

    Raises
    ------
    Does Not Error
    """
    user = context.message.author
    voice_channel = user.voice.channel
    return voice_channel

VALIDTEXTCHANNELS = [
    'Bobby Lobby',
    'General'
]

# ----------------- EXTENSION LOAD/UNLOAD TEST ------------------------------
@BOT.command(
    name='loadext',
    pass_context=True)
@commands.is_owner()
async def loadext(context, *args):
    for ext in args:
        try:
            BOT.load_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} loaded".format(ext))
    
    
@BOT.command(
    name='unloadext',
    pass_context=True)
@commands.is_owner()
async def unloadext(context, *args):
    for ext in args:
        try:
            BOT.unload_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} unloaded".format(ext))
        
        
@BOT.command(
    name='reloadext',
    pass_context=True)
@commands.is_owner()
async def reloadext(context, *args):
    for ext in args:
        try:
            BOT.unload_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} unloaded".format(ext))
    for ext in args:
        try:
            BOT.load_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} loaded".format(ext))



#-----------------------------Actually run the bot----------------------------

startup_extensions = ["rng", "tesseract", "pictures", "admin", "general", "listeners"]

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            BOT.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    BOT.run(TOKEN)

