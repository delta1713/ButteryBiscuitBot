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
        
# resets the from restart csv which then only gets changed when the 
newstart = {'restart' : 'false'}
# print(newstart)

writedictcsv(newstart, 'restart')



# defines global string songnames to store all songnames
songstring = ""
songlisttemp = list(BEAUTIFULSONGS.keys())
songlist = sorted(songlisttemp)
print("songlist :", songlist)
# print("type: ", type(songlist))

songstring = ', '.join(songlist)

        
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



# This is the top version number, only thing that needs to be updated for !version to be up to
# date. Please edit this anytime an update is made!
VNUMBER = '0.0.2.10 alpha'

# same as VNUMBER this is where the text for patch notes goes, please update this (also don't
# let it get too long maybe only the most recent build?)

PNOTES = """Version: """ + VNUMBER + """\n
 A separate bot channel now exists for command storage to prevent clutter.\n
 Now including !removesong and !protect song to prevent removal.
 Both of these are role limited.\n
 Also introducing much better error handling with improved feedback\n

 Also also you can cancel songs with !disconnect, for when Biscuit Bot is a bit too...
 biscuity. """
 
 
OldPNOTES = VNUMBER + """\n added version and patch notes commands 
 \n !version will now print the current version number (note this needs to be changed manually in the code) 
 \n !patchnotes will now print the current patch notes (also need to be changed manually) 
 \n Added proper error handling for if user calls bot but is not in a voicechannel 
 \n Working on implementing timestamping for logging purposes
 \n Added Duel of the fates (!duel) and Battle of the Heroes (!heroes) to playable songs. 
 \n Working on adding a restart command do make my (Jon's) life easier."""
 

@BOT.event
async def on_ready():
    """Print a message to console to verify that bot is activated / connected to discord."""
    print(f'{BOT.user} has connected to Discord!')
    if fromrestart['restart'] == 'true':
        bc = BOT.get_channel(botlog)
        print("bc :", bc)
        await bc.send("Restarted Successfully! Yay, I'm back!")
    else:
        pass


@BOT.event
async def on_message(message):
    """
    For a set of given messages, the bot responds with pre-defined responses in the
    "callResponseDict"

    Parameters
    ----------
    first : string
        The message any given user has typed into any text channel this bot can access

    Returns
    -------
    string
        The appropriate response for a given "call" from a message

    Raises
    ------
    Does Not Error
    """
    # TODO mdman2014 2/23/2020 - check that the author is either a quaid or a duckling

    # Prevent the bot from replying to itself ad-infinitum, in case we ever create a recursive
    # reply.
    if message.author == BOT.user:
        return

    standardized_message = message.content.lower()

    for key in CALLRESPONSEDICT:
        if key in standardized_message:
            response = CALLRESPONSEDICT[key]
            await message.channel.send(response)

    # This is necessary to allow bot commands to come through (such as music), since we have
    # overwritten the default on_message event handling
    # https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working
    await BOT.process_commands(message)

CALLRESPONSEDICT = {
    'hell': 'Yeah Dog!',
    'uwu': 'Hewwwwoo~~',
    'bb': 'BOBBBBBYYYYYYY',
    'bee': 'BEE-THEMED STRIPPERS!!',
    'kiddy': 'hey there ya dingus'
}

# def create_command(command_object):
#    name = command_object.name
#    aliases = command_object.aliases
#    description = command_object.description
#    pass_context = command_object.passcontext
#    return @Bot.command(name, aliases, description, pass_context)

@BOT.command(
    name='version',
    aliases=['Version'],
    description='',
    pass_context=True,
)

async def version(ctx):
    """
    Allows the user to tell what version is currently running

    Parameters
    ----------
    first : Context
        The context of the text channel in which the command was raised

    Returns
    -------
    string
        The version of the bot and timestamp of the call

    Raises
    ------
    Does Not Error
    """
    await ctx.message.channel.send(VNUMBER)
    current_timestamp = datetime.now()
    current_timestamp_string = current_timestamp.strftime("%d/%m/%Y %H:%M:%S")
    print(current_timestamp_string)
    print("Author: ", ctx.message.author,
    "\n Context: ", ctx.message)

@BOT.command(
    name='patchnotes',
    aliases=['Patchnotes', 'PatchNotes'],
    description='what does this do',
    pass_context=True,
)

async def patchnotes(ctx):
    """
    Allows the user to retrieve the updated patch notes

    Parameters
    ----------
    first : Context
        The context of the text channel in which the command was raised

    Returns
    -------
    string
        The patchnotes for the most recent release

    Raises
    ------
    Does Not Error
    """
    await ctx.message.channel.send(PNOTES)
    

BISCUITS = """Here's my recipe for Buttermilk Biscuits

-13 1/2 ounces all purpose flour
-2 Tbsp sugar
-4 tsp baking powder
-1/2 tsp baking soda
-1/2 tsp kosher salt
-2 sticks frozen butter
-1 1/4 cups buttermilk

1. Start by combining 13 ½ ounces all purpose flour, 2 tablespoons of sugar, 4 teaspoons of baking powder, ½ teaspoon of baking soda and ½ teaspoon of kosher salt in a bowl. Whisk with a fork until homogeneous.
2. By using the slightly larger holes on a cheese grater, grate 2 sticks of frozen butter.
3. Add butter to the flour mixture, and mix around until all the pieces are coated.
4. Add 1 ¼ cups buttermilk to the mixture and give it a good stir.
5. Remove the mixture from the bowl and continue to try to coax together into a sort of rectangle. Using a generously floured rolling pin, roll it out to a 16 by 9 inch rectangle and fold in thirds like a letter.  Watch the episode above if you need help!
6. Repeat this process five times.
7. Place the dough on a parchment-lined baking sheet, cover in plastic wrap, and refrigerate for 30 minutes to firm up.
8. Roll the dough out to a roughly 9x9 square-ish shape, and trim off the edges using a very sharp knife that was dusted in flour. 
9. Cut cleanly into 9 square biscuits.
10. Place back on the parchment-lined baking sheet and brush with butter.
11. Bake the biscuits at 400°F for 20-25 minutes.
12. Cool on a wire rack for about 10 minutes before consumption. """


@BOT.command(
    name='recipe',
    description='prints jacob\'s recipe',
    pass_context=True
)
async def recipe(context):
    await context.message.channel.send(BISCUITS)

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

@BOT.command(pass_context = True,
    aliases=['disconnect', 'Disconnect', 'fuckoffbiscuitbot'])
async def leavevoice(context):
    await context.message.delete()
    #print("message deleted")
    bc = BOT.get_channel(biscuitchannel)
    bl = BOT.get_channel(botlog)
    #print(bc)
    await bc.send("Disconnected by " + str(context.message.author))
    await bl.send("Disconnected by " + str(context.message.author))
    for x in BOT.voice_clients:
        return await x.disconnect()
        
    return await context.message.channel.send("I am not connected to any voice channel on this server!")
    
    
#-------------------------------Tesseract Specific commands-----------------

@BOT.command(pass_context = True)
@commands.is_owner()
async def trongsemble(ctx):
    await ctx.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/trongsemble.png'))
@trongsemble.error
async def functest_error(context, error):
    if isinstance(error, commands.CommandError):
        await context.message.channel.send("Only delta1713 can call for the Trongles to Trongsemble.")
        
        
@BOT.command(
    name='functest',
    pass_context=True)
@commands.is_owner()
async def functest(context, *args):
    fileinput = args[0]
    fileoutput = args[1]
    starttime = int(args[2] * 1000)
    endtime = int(args[3] * 1000)
    await pydubtrim(fileinput, fileoutput, starttime, endtime)
    
@BOT.command(
    name='functest2',
    pass_context=True)
@commands.is_owner()
async def functest2(context, *args):
    filepath = args[0]
    await play_mp3(filepath, VALIDTEXTCHANNELS, context)

#@functest.error
#async def functest_error(context, error):
#    if isinstance(error, commands.CommandError):
#        print("you are not tesseract")
#    if isinstance(error, commands.KeyError):
#        await context.message.channel.send("Error, could not find function")
    
    

#------------------------------Picture Zone!-----------------------------

@BOT.command(
    name='chrispenis',
    aliases=['ChrisPenis', 'Chrispenis'],
    description='Cool wafers to desired...',
    pass_context=True,
)
async def chrispenis(channel):
    """
    ChrisPenis
    """
    await channel.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/chrispenis.jpg'))
    # this sends the file directly to discord, there is a way to do so with filelike objects
    # (dunno what those are) but I couldn't get it to work

@BOT.command(
    name='biscuitface',
    aliases=['biscuitfaces', 'BiscuitFace', 'BiscuitFaces'],
    description='They are buttery...',
    pass_context=True,
)
async def biscuitface(channel):
    """
    biscuitfaces
    """
    await channel.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/biscuitface.jpg'))

@BOT.command(
    name='pepperoni',
    aliases=['Pepperoni', 'heyyotony', 'freshpepperoni', 'cleverthoughts', 'CleverThoughts'],
    description='Hey yo tony, whered you get that fresh pepperoni',
    pass_context=True,
)
async def pepperoni(channel):
    """
    pepperoni
    """
    await channel.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/pepperoni.png'))


@BOT.command(
    name='trongle',
    aliases=['Trongle', 'trongleman', 'Trongleman'],
    description='TRONGLE MAN!',
    pass_context=True,
)
async def trongle(channel):
    """
    trongle man
    """
    await channel.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/trongle.jpg'))
    

@BOT.command(
    name='metatrongle',
    aliases=['MetaTrongle', 'sushtrongle'],
    description='it\'s trongle man, but meta',
    pass_context=True,
)
async def metatrongle(channel):
    """
    meta trongle
    """
    await channel.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/metatrongle.png'))

#------------------------------Mp3 command zone!-----------------------------
# Command for the old deprecated commands
@BOT.command(name='deprecated',
    aliases=['biscuit',
    'washington',
    'yes',
    'no',
    'allhail',
    'oooh',
    'isp',
    '2hours',
    'start',
    'wololo',
    'snout',
    'shortbiscuit',
    'duel',
    'heroes'],
    description = 'Deprecated commands, returns a message from the bot to use newer commands',
    pass_context = True,
    )
    
async def deprecated(context):
    await context.message.channel.send("That command is deprecated, use !play <songname> instead (no pointy brackets)")


#--------------------TESTING !PLAY COMMAND---------------------------

@BOT.command(
    name='play',
    aliases=['Play', 'p', 'song', 'Song', 'PLAY'],
    description='Play a song from known song list',
    pass_context=True,
)
async def play(context, *args):
    # debugging prints lol
    # print("Context.message: ", context.message)
    # print("args: ", args)
    if len(args) == 1 and args[0] != 'random':
        filename = args[0]
        try:
            songpath = BEAUTIFULSONGS[filename]
        except KeyError:
            errmessage = filename + " is not a song, try !play for a list of songs"
            await context.message.channel.send(errmessage)
            return
        await context.message.delete()
        #print("message deleted")
        bc = BOT.get_channel(biscuitchannel)
        bl = BOT.get_channel(botlog)
        #print(bc)
        await bc.send("Now playing " + args[0] + " on behalf of " + str(context.message.author))
        await bl.send("Now playing " + args[0] + " on behalf of " + str(context.message.author))
        await play_mp3(BEAUTIFULSONGS[filename], VALIDTEXTCHANNELS, context)

#    elif args[0] == 'random':
#        end = len(BEAUTIFULSONGS)
#        print(end)
#        rnum = random.randint(0,end)
#        print(rnum)
#        await play_mp3(BEAUTIFULSONGS[rnum], VALIDTEXTCHANNELS, context)
    elif len(args) == 0:
        songlistmessage = "Here's a list of songs I can play: \n" + songstring
        # print("type of songlistmessage:", type(songlistmessage))
        await context.message.channel.send(songlistmessage)
    else:
        await context.message.channel.send("Play what? Uhh... Why don't you try again.(Try !play for a list of songs)")
@play.error
async def play_error(context, error):
    if isinstance(error, commands.CommandInvokeError):
        await context.message.channel.send("Chill out dude, I'm playing something already")

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
        await context.message.channel.send("Can't download that, check your url dude.")
        return False
        
async def checksongname(name, context):
    # checks if a song name exists
    # returns false if no, true if yes
    try:
        BEAUTIFULSONGS[name]
        await context.message.channel.send("That song already exists dude, choose a different name")
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
    # print("in function")
    filename = args[0]
    link = args[1]
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'
    try:
        starttime = str(args[2])
        endtime = str(args[3])
        needtrim = True
        print("needs trim: ", needtrim)
    except:
        starttime = None
        endtime = None
        needtrim = False
        print("no trim")
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
    aliases = ['remove', 'Remove', 'Removesong'],
    pass_context=True)
@commands.has_any_role('Quaid', 'Quaidling')
async def removesong(context, *args):
    # takes context and the name of a song
    
    #calls check permissions to make sure you can
    if await checkpermissions(context) == True:
        pass
    else:
        return
    
    
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
    try:
        del BEAUTIFULSONGS[filename]
        writedictcsv(BEAUTIFULSONGS, 'songlist2')
    except KeyError:
        await context.message.channel.send("Error, song name does not exist.")
        return
    # remakes songnames which should no longer contain the deleted song
    songlist = list(BEAUTIFULSONGS.keys())
    songstring = ', '.join(songlist)
    await context.message.channel.send(filename + "has been deleted")
@removesong.error
async def removesong_error(context, error):
    if isinstance(error, commands.MissingAnyRole):
        await context.message.channel.send("Error, you cannot remove things.")
    else:
        print(error)


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
    songstring = ', '.join(songlist)
    await context.message.channel.send("Song " + filename + "has been deleted")
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
    if await is_user_in_channel(context, channel_names):
        # Connect to voice chat and play .mp3
        voice_channel = await get_current_voice_channel_instance(context)
        voice_channel_connection = await voice_channel.connect()
        voice_channel_connection.play(discord.FFmpegPCMAudio(mp3_file_path),
                                      after=lambda e: print('done', e))

        # Wait for music to finish
        while voice_channel_connection.is_playing():
            await asyncio.sleep(1)
        # Disconnect after music stops
        voice_channel_connection.stop()
        await voice_channel_connection.disconnect()
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

BEAUTIFULSONGS2 = {
    'biscuit': '/pythbot/Buttery_Biscuit_Bot/Music/ButteryBiscuitBase.mp3',
    'washington': '/pythbot/Buttery_Biscuit_Bot/Music/Washington.mp3',
    'yes': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/yes.mp3',
    'no': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/no.mp3',
    'allhail': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/allhail.mp3',
    'oooh': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/oooh.mp3',
    'isp': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/blameyourisp.mp3',
    '2hours': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/2hours.mp3',
    'start': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/startthegame.mp3',
    'wololo': '/pythbot/Buttery_Biscuit_Bot/Music/AOE2Taunts/wololo.mp3',
    'snout': '/pythbot/Buttery_Biscuit_Bot/Music/snout.mp3',
    'shortbiscuit': '/pythbot/Buttery_Biscuit_Bot/Music/shortbiscuit.mp3',
    'duel': '/pythbot/Buttery_Biscuit_Bot/Music/duel.mp3',
    'heroes': '/pythbot/Buttery_Biscuit_Bot/Music/heroes.mp3',
    'silverscrapes': '/pythbot/Buttery_Biscuit_Bot/Music/silverscrapes.mp3',
    'sandstorm': '/pythbot/Buttery_Biscuit_Bot/Music/darudesandstorm.mp3',
    'crab': '/pythbot/Buttery_Biscuit_Bot/Music/crab.mp3',
    'mando': '/pythbot/Buttery_Biscuit_Bot/Music/mando.mp3',
    'surprise': '/pythbot/Buttery_Biscuit_Bot/Music/surprise.mp3',
    'cantina': '/pythbot/Buttery_Biscuit_Bot/Music/cantina.mp3',
    'elk': '/pythbot/Buttery_Biscuit_Bot/Music/elk.mp3',
    'hello': '/pythbot/Buttery_Biscuit_Bot/Music/hello.mp3',
    'kid': '/pythbot/Buttery_Biscuit_Bot/Music/kid.mp3',
    'sorry': '/pythbot/Buttery_Biscuit_Bot/Music/sorry.mp3',
    'artorias': '/pythbot/Buttery_Biscuit_Bot/Music/artorias.mp3',
    'verygood': '/pythbot/Buttery_Biscuit_Bot/Music/verygood.mp3',
    'kosm': '/pythbot/Buttery_Biscuit_Bot/Music/kosm.mp3',
}







        
        


VALIDTEXTCHANNELS = [
    'Bobby Lobby',
    'General'
]

#-----------------------------Actually run the bot----------------------------
BOT.run(TOKEN)


#TODO:
    # Add uwu-translator function
    # Mess w/ Bobby somehow
    # Rename washington to 'he's coming'? Has punctuation and a space so probably horrible,
    #but I want it to be invokable that way >.>
    # Add songs or other commands, build out additional functionality
