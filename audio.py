import discord
from discord.ext import commands


#--------------------PLAY COMMAND---------------------------
BOT = commands.Bot(command_prefix="!")
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

# ----------------------------- Acquire Command----------
    
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
        starttime = int(args[2])
        endtime = int(args[3])
    except:
        starttime = None
        endtime = None
    if await checksongname(filename, context) == True:
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
    await downloadmp3(link, filename, filelocation)
    
    # reupdates the songnames so !play shows the updated list
    
    BEAUTIFULSONGS[filename] = filelocation
    # writes the songlist to the csv after updating
    writedictcsv(BEAUTIFULSONGS, "songlist2")
    # says message in channel to say it's done
    makesongnames()
    await context.message.channel.send("Successfully downloaded " + filename + "\n It is ready to play")
@acquire.error
async def acquire_error(context, error):
    if isinstance(error, commands.MissingAnyRole):
        await context.message.channel.send("Error, you do not have permission")

#------------------------Force Remove Command----------------------
@BOT.command(
    name='forceremove',
    description='Quaid only command to force remove',
    aliases=['forceremovesong'],
    pass_context=True,
)
@commands.has_role('Quaid')
async def forceremove(context, *args):
    
    # takes context and the name of a song
    
    #calls check if user is quaid to make sure you can
    if await checkquaid(context) == True:
        pass
    else:
        return
    
    
    # takes the filename from the args
    filename = args[0]
    #creates the location of the mp3 file from the name
    filelocation = '/pythbot/Buttery_Biscuit_Bot/Music/' + filename + '.mp3'

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
    makesongnames()
    await context.message.channel.send("Protected song " + filename + "has been deleted")
@forceremove.error
async def forceremove_error(context, error):
    if isinstance(error, commands.MissingRole):
        await context.message.channel.send("Error, you do not have permissions")
 

#---------------------Remove Song Command--------------

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
    elif filename in protectedsonglist and await checkquaid(context) == True:
        await context.message.channel.send(filename + " is protected, use !forceremove.")
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
    makesongnames()
    await context.message.channel.send(filename + "has been deleted")
@removesong.error
async def removesong_error(context, error):
    if isinstance(error, commands.MissingAnyRole):
        await context.message.channel.send("Error, you do not have permission")

#----------------Protect Command----------

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
async def functest_error(context, error):
        if isinstance(error, commands.MissingRole):
            await context.message.channel.send("Error, you do not have permission")
            
            
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
            print("in with statement")
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
        await context.message.channel.send('I cannot join that channel, idiot')
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