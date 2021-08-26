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

# import version

#Initialize Bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT = commands.Bot(command_prefix="!")

# This is the top version number, only thing that needs to be updated for !version to be up to
# date. Please edit this anytime an update is made!
VNUMBER = '0.0.1.13 alpha'

# same as VNUMBER this is where the text for patch notes goes, please update this (also don't
# let it get too long maybe only the most recent build?)
PNOTES = VNUMBER + """\n added version and patch notes commands 
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

#-------------------------------Stop Bot command--------------------------

@BOT.command(pass_context = True,
    aliases=['disconnect', 'Disconnect', 'fuckoffbiscuitbot'])
async def leavevoice(ctx):
    for x in BOT.voice_clients:
        return await x.disconnect()
    return await ctx.message.channel.send("I am not connected to any voice channel on this server!")
    
    
#-------------------------------Tesseract Specific commands-----------------

@BOT.command(pass_context = True)
async def trongsemble(ctx):
    auth = ctx.message.author.id
    # print("Auth :", auth)
    # print("authtype:", type(auth))
    if auth == 97172418258280448:
        await ctx.send(file=discord.File('/pythbot/Buttery_Biscuit_Bot/pictures/trongsemble.png'))
    else:
        await ctx.message.channel.send("Nah dog, you gotta be delta1713 to trongsemble")

    

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

#This whole section is just aoe2 Taunts
@BOT.command(
    name='yes',
    aliases=['Yes'],
    description='',
    pass_context=True,
)
async def aoe2_yes(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['yes'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='no',
    aliases=['No'],
    description='',
    pass_context=True,
)
async def aoe2_no(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['no'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='allhail',
    aliases=['AllHail'],
    description='',
    pass_context=True,
)
async def aoe2_all_hail(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['allhail'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='oooh',
    aliases=['Oooh'],
    description='',
    pass_context=True,
)
async def aoe2_oooh(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['oooh'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='isp',
    aliases=['ISP'],
    description='',
    pass_context=True,
)
async def aoe2_blame_your_isp(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['isp'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='start',
    aliases=['Start'],
    description='',
    pass_context=True,
)
async def aoe2_start_the_game(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['start'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='2hours',
    aliases=[''],
    description='',
    pass_context=True,
)
async def aoe2_you_play2hours_to_die_like_that(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['2hours'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='wololo',
    aliases=['Wololo'],
    description='',
    pass_context=True,
)
async def aoe2_wololo(context):
    """
    AOE2 taunt
    """
    await play_mp3(BEAUTIFULSONGS['wololo'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='washington',
    aliases=['Washington'],
    description='He\'s Coming!',
    pass_context=True,
)
async def washington(context):
    """
    plays Washington mp3
    """
    await play_mp3(BEAUTIFULSONGS['washington'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='biscuit',
    aliases=['Biscuit'],
    description='All your base...',
    pass_context=True,
)
async def biscuit(context):
    """
    plays ButteryBiscuitBase mp3
    """
    await play_mp3(BEAUTIFULSONGS['biscuit'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='shortbiscuit',
    aliases=['ShortBiscuit'],
    description='All your biscuit...',
    pass_context=True,
)
async def shortbiscuit(context):
    """
    plays the opening riff from ButteryBiscuitBase mp3
    """
    await play_mp3(BEAUTIFULSONGS['shortbiscuit'], VALIDTEXTCHANNELS, context)

@BOT.command(
    name='snout',
    aliases=['Snout', 'Sing', 'singforme', 'sing', 'SingForMe'],
    description='phantom of the opera snout',
    pass_context=True,
)
async def snout(context):
    """
    plays the wierd snout phantom of the opera thing
    """
    await play_mp3(BEAUTIFULSONGS['snout'], VALIDTEXTCHANNELS, context)
    
    

@BOT.command(
    name='duel',
    aliases=['Duel', 'DueloftheFates', 'maul', 'bestbossfightmusic'],
    description='duel of the fates',
    pass_context=True,
)
async def duel(context):
    """
    plays duel of the fates
    """
    await play_mp3(BEAUTIFULSONGS['duel'], VALIDTEXTCHANNELS, context)
    
    
@BOT.command(
    name='heroes',
    aliases=['Heroes', 'battleoftheheroes', 'highgroundfight'],
    description='battle of the heroes',
    pass_context=True,
)
async def duel(context):
    """
    plays battle of the heroes
    """
    await play_mp3(BEAUTIFULSONGS['heroes'], VALIDTEXTCHANNELS, context)
#--------------------TESTING !PLAY COMMAND---------------------------

@BOT.command(
    name='play',
    aliases=['Play', 'p', 'song', 'Song', 'PLAY'],
    description='Play a song from known song list',
    pass_context=True,
)
async def play(context, *args):
    #print("Context.message: ", context.message)
    #print("args: ", args)
    if len(args) == 1:
        try:
            await play_mp3(BEAUTIFULSONGS[args[0]], VALIDTEXTCHANNELS, context)
        except KeyError:
            errmessage = args[0] + " is not a song, try !play for a list of songs"
            await context.message.channel.send(errmessage)
    elif len(args) == 0:
        songlistmessage = "Here's a list of songs I can play: \n" + songnames
        # print("type of songlistmessage:", type(songlistmessage))
        await context.message.channel.send(songlistmessage)
    else:
        await context.message.channel.send("Play what? Uhh... Why don't you try again.(Try !play for a list of songs)")
 
#-----------------------------------------------


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
        await context.message.channel.send('User is not in a voice channel.')

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

BEAUTIFULSONGS = {
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
    'heroes': '/pythbot/Buttery_Biscuit_Bot/Music/heroes.mp3'
}

songnames = ""
for x in BEAUTIFULSONGS:
    songnames = songnames + x + "\n"
#print("songnames: ", songnames)
#print("type of songnames:", type(songnames))

VALIDTEXTCHANNELS = [
    'Bobby Lobby',
    'General'
]

#-----------------------------Actually run the bot----------------------------
print(discord.__version__)
BOT.run(TOKEN)


#TODO:
    # Add uwu-translator function
    # Mess w/ Bobby somehow
    # Rename washington to 'he's coming'? Has punctuation and a space so probably horrible,
    #but I want it to be invokable that way >.>
    # Add songs or other commands, build out additional functionality
