from discord.ext import commands
import discord
import asyncio
import biscuitfunctions as bf
from datetime import datetime
import csv
import youtube_dl
import pytz
from mutagen.mp3 import MP3
import json
import os.path
import random
from pydub import AudioSegment
from collections import OrderedDict

root = "/gitbot/ButteryBiscuitBot/"

reservednames = ['random', 'all', 'admin', 'delete', 'tesseract', 'delta1713', 'jon', 'jonathan', 'Jon', 'Jonathan', 'Jono', 'jono', 'Tesseract', 'song', 'Songs']

isyoinking = False

def makealiases(songdict):
    aliasdict = {}
    for x in songdict:
        if songdict[x]['aliases']:
            for y in songdict[x]['aliases']:
                aliasdict[y] = songdict[x]['topname']
    return aliasdict


songdict = bf.readdictjson('mastersonglist')

aliasdict = makealiases(songdict)

def findtopname(name):
    if name in songdict:
        return name
    elif name in aliasdict:
        return aliasdict[name]
    else:
        return None

editperms = ['quaid', 'quaidling', 'tesseract']

async def songeditF(context, song, kwargdict):
    global songdict
    global aliasdict
    changed = []
    notchanged = []
    print(songdict[song])
    print(bf.getprivs(context))
    if bf.getprivs(context) == 'tesseract':
        usereditable = ['protected', 'duration', 'volume', 'category', 'description', 'filename', 'filepath', 'topname', 'addtime', 'lastplay', 'playcount', 'server', 'source']
    else:
        usereditable = ['protected', 'duration', 'volume', 'category', 'description']
    print(usereditable)
    if kwargdict == None:
        await context.send(f"Yo, {bf.authname(context)} I don't know that stuff, check your spelling")
    if bf.getprivs(context) in editperms:
        for x in kwargdict:
            print("x: ", x)
            if x in usereditable and x != 'volume':
                print("1")
                songdict[song][x] = kwargdict[x]
                changed.append({x : kwargdict[x]})
            elif x == 'alias':
                if kwargdict['alias'] in (aliasdict or songdict):
                    notchanged.append({x : f"{kwargdict[x]}, already exists"})
                else:
                    songdict[song]['aliases'].append(kwargdict[x])
                    aliasdict = makealiases(songdict)
                    changed.append(f"{kwargdict[x]} added to {song} aliases")
            elif x == 'delalias':
                songdict[song]['aliases'].remove(kwargdict[x])
                aliasdict.pop(kwargdict[x])
                changed.append(f"{kwargdict[x]} removed from {song} aliases")
                aliasdict = makealiases(songdict)
            elif x == 'volume':
                if float(kwargdict[x]) > 5:
                    await context.send(f"Yo, {bf.authname(context)}, I am not making the volume higher than 5.")
                    songdict[song][x] = '5'
                    changed.append({x : '5'})
                else:
                    songdict[song][x] = kwargdict[x]
                    changed.append({x : kwargdict[x]})
            else:
                notchanged.append({x : kwargdict[x]})
        print("after changes: ", songdict[song])
    else:
        await context.send(f"Sorry {bf.authname(context)}, you can't edit songs")
        return
    changedstr = ", ".join(map(str, changed))
    notchangedstr = ", ".join(map(str, notchanged))
    if changed:
        await context.send(f"""{bf.authname(context)} I changed the following in {song}:
{changedstr}""")
    if notchanged:
        await context.send(f"""{bf.authname(context)} I could not change the following in {song}:
{notchangedstr}""")
    if changed == False and notchanged == False:
        await context.send(f"Yo, {bf.authname(context)} I didn't change anything, check your spellings")
    bf.writedictjson(songdict, "mastersonglist")

async def songcount(song):
    song['playcount'] = int(song['playcount']) + 1
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    time = now.strftime("%m/%d/%Y, %-I:%M:%S %p")
    song['lastplay'] = time


# -------------------------------- Play Cog ---------------------------------
async def playsong(voice_connection, song):
    voice_connection.play(discord.FFmpegPCMAudio(f'{song["filepath"]}', options=f'-filter:a "volume={song["volume"]}"'),
    after = lambda e: print(f'Done playing {song["topname"]}, errors: ', e))
    await songcount(song)
    while voice_connection.is_playing():
        await asyncio.sleep(1)
    voice_connection.stop()
    await voice_connection.disconnect()

    
def makesongstring():
    songlisttemp = list(songdict.keys())
    songlist = sorted(songlisttemp)
    songstringlist = []
    tempsongstring = ""
    for x in songlist:
        if len(tempsongstring) + len(x) < 1950:
            tempsongstring += f"{x}, "
        else:
            tempsongstring = tempsongstring[:-2]
            songstringlist.append(tempsongstring)
            tempsongstring = ""
            tempsongstring += f"{x}, "
    tempsongstring = tempsongstring[:-2]
    songstringlist.append(tempsongstring)
    return songstringlist

class playsongs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='play',
        aliases = ['p', 'Play', "P"],
        pass_context=True,
        description = 'Play a song from the song list in your current voice channel',
        help = "Useage: !play <songname>*\nIf no songname passed returns songlist.\nBot will join the authors voice channel and play the requested song.")
    async def play(self, context, *args):
        if len(args) == 0 or args[0] == 'all':
            mastersongstringlist = makesongstring()
            i = 1
            for x in mastersongstringlist:
                stringnumbers = len(mastersongstringlist)
                songmessage = f"Here's a list of songs I can play ({i}/{stringnumbers}): \n{x}"
                await context.send(songmessage)
                i += 1
            return
        if context.guild.voice_client != None:
            return await context.send(f"Hey, {bf.authname(context)}, I am already playing something dumbass!")
        else:
            pass
        global songdict
        botlogdict = {"quaid" : self.bot.get_channel(742482393587515555), "biscuitlog" : self.bot.get_channel(739510798099152916)}
        if context.author.voice != None:
            pass
        else:
            await context.send("Error, you're not in a voice channel, dumbass.")
            return
        song = findtopname(args[0])
        if args[0] == 'random':
            songlist = list(songdict.keys())
            end = len(songlist)
            rnum = random.randint(0, end-1)
            song = songdict[songlist[rnum]]
            await context.message.delete()
            voice_connection = await context.author.voice.channel.connect()
            await botlogdict["quaid"].send(f"Playing {song['topname']} randomly on behalf of {bf.authname(context)}")
            await botlogdict["biscuitlog"].send(f"Playing {song['topname']} randomly on behalf of {bf.authname(context)}")
            await playsong(voice_connection, song)
        elif song != None:
            await botlogdict["quaid"].send(f"Playing {song} on behalf of {bf.authname(context)}")
            await botlogdict["biscuitlog"].send(f"Playing {song} on behalf of {bf.authname(context)}")
            await context.message.delete()
            voice_connection = await context.author.voice.channel.connect()
            await playsong(voice_connection, songdict[song])
        else:
            await context.send("Play what? Uhh... Why don't you try again. (Try !play for a list of songs)")

    @commands.command(name = "leavevoice",
    pass_context = True,
    aliases=['disconnect', 'Disconnect', 'fuckoffbiscuitbot', 'd', 'fu', 'D'],
    description = 'Make the bot leave voice')
    async def leavevoice(self, context):
        botlogdict = {"quaid" : self.bot.get_channel(742482393587515555), "biscuitlog" : self.bot.get_channel(739510798099152916)}
        await botlogdict["quaid"].send("Disconnected by " + str(context.message.author))
        await botlogdict["biscuitlog"].send("Disconnected by " + str(context.message.author))
        await context.message.delete()
        if context.guild.voice_client != None:
            await context.guild.voice_client.disconnect()
        else:
            return await context.send(f"Hey, {context.author}, I am not connected to any voice channel on this server!")
            
# -------------------------------- Acquire Cog ---------------------------------
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

async def checksongurl(context, url, filelocation):
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
            if duration <= 900:
                return duration
            else:
                await context.send("This vid is way too long dude, it's " + str(duration) + " seconds.  Find something shorter!")
                return 999
    except:
        await context.send("Can't download that, check your url.")
        return 999

async def checksongname(context, name):
    if name in reservednames:
        await context.send(f"Sorry {bf.authname(context)}, {name} is reserved.")
        return False
    elif name in songdict or name in aliasdict:
        await context.send(f"Sorry {bf.authname(context)}, {name} is taken.")
        return False
    else:
        return True

async def builddictentry(context, topname, filelocation, duration, source):
    global songdict
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    time = now.strftime("%m/%d/%Y, %-I:%M:%S %p")
    entry = {}
    entry["topname"] = topname
    entry["filepath"] = filelocation
    entry["aliases"] = []
    entry['category'] = 'songs'
    entry['protected'] = 'false'
    entry['duration'] = duration
    entry["author"] = bf.authname(context)
    entry["addtime"] = time
    entry["lastplay"] = None
    entry["playcount"] = 0
    entry["volume"] = "1"
    entry["source"] = source
    entry['server'] = str(context.guild)
    entry['description'] = 'No description yet, add one with !songedit <name> "description=<description here>" (note the double quotes around both keyword and argument)'
    print("entry is: ", entry)
    songdict[topname] = entry
    return entry

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
    print(f"finished download of {filename}")

class acquisition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='acquire',
        aliases = ['yoink'],
        pass_context = True,
        description = 'Acquire songs from youtube for playback with bot',
        help="Useage: !acquire <songname> <youtube url*> <starttime*> <stoptime*>\nArguments with * are optional\nIf no youtube url provided there must be an attached mp3 file (drag and drop the file into discord and put the command and arguments in the comments)\nStart time and stop time must be integers and in seconds (4:20 becomes 260).\n\nAdds songs to the bot's repertoire either via a youtube link (with optional timestamps) or via direct mp3 upload."
        )
    async def acquire(self, context, *args):
        global isyoinking
        if isyoinking == False:
            pass
        else:
            await context.send("Yo, I am yoinking currently. Chill yo yoink and try again.")
            return
        isyoinking = True
        print("length args: ", len(args))
        if len(args) == 0:
            await context.send("Yo, I need something to acquire dumbass")
            isyoinking = False
            return
        elif len(args) == 1 and len(context.message.attachments) != 0:
            attach = True
            fromurl = False
            trim = False
        elif len(context.message.attachments) == 0 and len(args) == 2:
            fromurl = True
            attach = False
            trim = False
        elif len(args) == 4:
            trim = True
            attach = False
            fromurl = True
            startsec = int(args[2])
            endsec = int(args[3])
        else:
            await context.send(f"Uhh, what was that {bf.authname(context)}?")
            isyoinking = False
            return
        async with context.channel.typing():
            if attach == True:
                filename = args[0]
                if not await checksongname(context, filename):
                    return
                filelocation = root + '/Music/' + filename + '.mp3'
                await context.message.attachments[0].save(filelocation)
                songmp3 = MP3(filelocation)
                duration = songmp3.info.length
                await builddictentry(context, filename, filelocation, duration, "mp3")
                bf.writedictjson(songdict, "mastersonglist")
                await context.send(f"Acquired {filename} for {bf.authname(context)}")
                isyoinking = False
                return
            elif fromurl == True and trim == False:
                filename = args[0]
                filelocation = root + '/Music/' + filename + '.mp3'
                url = args[1]
                if not await checksongname(context, filename):
                    isyoinking = False
                    return
                duration = await checksongurl(context, url, filelocation)
                if duration == 999:
                    isyoinking = False
                    return
                await downloadmp3(url, filename, filelocation)
                await builddictentry(context, filename, filelocation, duration, url)
                bf.writedictjson(songdict, "mastersonglist")
                await context.send(f"Acquired {filename} for {bf.authname(context)}")
                isyoinking = False
                return
            elif fromurl == True and trim == True:
                filename = args[0]
                filelocation = root + '/Music/' + filename + '.mp3'
                url = args[1]
                if not await checksongname(context, filename):
                    isyoinking = False
                    return
                duration = await checksongurl(context, url, filelocation)
                if duration == 999:
                    isyoinking = False
                    return
                tempfile = root + '/Music/temp.mp3'
                if os.path.isfile(tempfile):
                    try:
                        os.remove(tempfile)
                    except OSError:
                        pass
                await downloadmp3(url, filename, tempfile)
                await pydubtrim(tempfile, filelocation, startsec, endsec)
                await builddictentry(context, filename, filelocation, endsec-startsec, url)
                bf.writedictjson(songdict, "mastersonglist")
                await context.send(f"Acquired {filename} for {bf.authname(context)}")
                isyoinking = False
                return

async def pydubtrim(fileinput, fileoutput, starttime, endtime):
    startms = int(starttime)*1000
    endms = int(endtime)*1000 + 500
    clip = AudioSegment.from_file(fileinput)
    extract = clip[startms:endms].fade_out(1000)
    extract.export(fileoutput, format="mp3")

# -------------------------------- Songs Cog ---------------------------------
dellist = ['delete', 'del', 'remove', 'd']

class songs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='songinfo',
        aliases = ['si', 'info'],
        pass_context = True,
        description = 'Return information about a song',
        help = "Useage: !songinfo <songname> ...\n\nReturns information about song names/aliases passed as arguments."
        )
    async def songinfo(self, context, *args):
        for x in args:
            name = findtopname(x)
            if name != None:
                dembed = discord.Embed(name=f'{name}', description = f'Songinfo about {x}')
                song = songdict[name]
                for key in song:
                    if key not in ['filepath', 'duration']:
                        dembed.add_field(name=f'{key}', value=f'{str(song[key])[:1023]}')
                    elif key == 'duration':
                        if isinstance(song['duration'], str):
                            dembed.add_field(name=f"{key}", value=f"{song['duration']}")
                        else:
                            dembed.add_field(name=f"{key}", value=f"{round(song['duration'], 1)}")
                    elif key == 'filepath':
                        dembed.add_field(name=f'filename', value=f'{song["filepath"][35:]}')
                await context.send(embed=dembed)
            else:
                await context.send(f"You want info about what?! (I can't find {x}, use !play for a list of all songnames)")
                return
            
            
    @commands.command(
        name='songsearch',
        aliases = ['search', 'find', 'lookup'],
        pass_context = True,
        brief = 'Searches name, aliases, and descriptions for given argument.',
        help = 'Useage !songsearch <string> ...\nArguments must be a string, can pass multiple strings and will do a different search for each argument\n\nReturns all song names that contain passed strings.')
    async def songsearch(self, context, *args):
        resultsdict = {}
        for x in args:
            results = []
            for songentry in songdict:
                song = songdict[songentry]
                if x in song['topname']:
                    results.append(song['topname'])
                elif any(x in s for s in song['aliases']):
                    results.append(song['topname'])
                elif x in song['description']:
                    results.append(song['topname'])
            resultsdict[x] = results
        await context.send(f"Here are the results I found for your search:\n{resultsdict}", delete_after=60)
        await context.message.delete()

    @commands.command(
        name='songedit',
        aliases = ['edit', 'e', 'se'],
        pass_context = True,
        description = 'Edit some of a songs information')
    async def songedit(self, context, *args):
        global songdict
        global aliasdict
        arglist = list(args)
        insong1 = arglist.pop(0)
        insong = findtopname(insong1)
        if findtopname(insong) != None:
            pass
        else:
            await context.send(f"Yo, {bf.authname(context)}, I can't edit {insong}, I don't know it!")
            return
        if (arglist[0] in dellist):
            if songdict[insong]['protected'] == 'false':
                pop = songdict.pop(args[0], None)
                if pop != None:
                    for x in pop['aliases']:
                        aliasdict.pop(x, None)
                    try:
                        os.remove(pop['filepath'])
                    except OSError:
                        print(f"--------------------\nERROR COULD NOT DELETE {pop['topname']} FILE\n--------------------")
                        await context.send("Maybe this was deleted? I errored trying to delete the mp3 file, ask dad")
                    bf.writedictjson(songdict, "mastersonglist")
                    await context.send(f"I have removed {insong} from my momery, {bf.authname(context)}")
                    return
            else:
                await context.send(f"{insong} is protected {bf.authname(context)}, you gotta talk to my dad to remove it.")
                return
            return
        kwargs = await bf.makekwargs(arglist)
        if insong in songdict and kwargs != None:
            await songeditF(context, insong, kwargs)
        elif insong in aliasdict:
            song = aliasdict[song]
            await songeditF(context, song, kwargs)
        elif kwargs == None:
            await context.send("Error, use format !songedit <songname> <field>=<value> (no pointy brackets)")
        else:
            await context.send("Yo, I can't find that song, check yo shit dawg.")
            
    @commands.command(
        name="songstats",
        aliases = ["stats"],
        pass_context=True,
        description = "Returns playcount statistics for all songs",
        brief = "Playcount statistics for songs")
    async def songstats(self, context, *args):
        if len(args) == 0:
            osongdict = OrderedDict(sorted(songdict.items(), key=lambda x: int(x[1]['playcount']), reverse=True))
            namestring = ""
            countstring = ""
            dembed = discord.Embed(name='Most played songs', description = 'Here are the top 25 songs by playcount')
            totlen = len(osongdict)
            for x in range(1,25):
                key = list(osongdict)[x-1]
                namestring = namestring + f"{key} \n"
                countstring = countstring + f"{osongdict[key]['playcount']} \n"
            dembed.add_field(name=f"Song", value=namestring[:-2], inline = True)
            dembed.add_field(name=f"Playcount", value=countstring[:-2], inline = True)
            await context.send(embed=dembed)

    @commands.command(
        name="legacyadd",
        aliases = ['legadd', 'legsong', 'oldshit', 'oldyoink'],
        pass_context = True,
        description = "Checks for legacy songs and adds it if it existed before",
        )
    async def legacyadd(self, context, *args):
        global songdict
        if not args:
            await context.send("Yo, you gotta give me something to go on here, looking through this ancient history is hard", delete_after=60)
        filename = args[0]
        filelocation = root + '/Music/' + filename + '.mp3'
        filelocation2 = root + '/Music/aoe2/' + filename + '.mp3'
        if filename in songdict or filename in aliasdict:
            await context.send(f"Yo, I already know that one, just do !play {filename}", delete_after=60)
            await context.message.delete()
            return
        elif filename in reservednames:
            await context.send(f"The name {filename} is reserved!", delete_after=60)
        if os.path.isfile(filelocation):
            duration = "a mystery"
            source = "ancient ruins"
            await builddictentry(context, filename, filelocation, duration, source)
            bf.writedictjson(songdict, "mastersonglist")
            await context.send(f"Yo, I found {filename}, it's pretty dusty but I added it", delete_after=60)
        elif os.path.isfile(filelocation2):
            duration = "a mystery"
            source = "ancient ruins"
            await builddictentry(context, filename, filelocation2, duration, source)
            await context.send(f"Yo, I found {filename}, it's pretty dusty but I added it", delete_after=60)
            songdict[filename]['category'] = 'aoe2'
            bf.writedictjson(songdict, "mastersonglist")
        else:
            await context.send(f"Damn, couldn't find it. You need a better archaeologist", delete_after=60)
        await context.message.delete()

    @commands.command(
        name="legacylist",
        pass_context = True,
        description = "Shows the list of legacy songs")
    async def legacylist(self, context):
        part1 = """2hours, 500, 5crown, 9000, DND, Dettlaff, EENURNET, Fall, Geralt, aaroncorey, ae, africa, africaremix, ahshit, airplane, allhail, amygdala, artorias, ashenone, axelf, babymonkey, barbarie, batmandance, bearlullaby, becareful, because, beverly, birthday, biscuit, blockparty, bobby, bondulance, boneless2, bonesaw, breath, bridge, bridgeisout, brother, byeah, cannibal, cantina, captain, car, cavitating, cena, chickenshit, christian, cockpit, coming, comingdown, crabgod, crabgod2, crabrave, csb, csbaaron, csbbad, csbbecause, csbbees, csbbobby, csbdave, csbjared, csbjealous, csbjoe, csbjono, csbkitty, csbmike, csbnope, csbokay, csboooh, csbsusha, csbyes, damage, darkness, davecorey, ddduel, dejavu, discord, dkrap, dogeater, dogs, dontwant, doot, dubhall, duel, elk, else, fire, fish, friendz, fuck, getinhere, goat, goodcorey, goodnews, goods, gravy, greatjob, h, hamilton, hams, hava, hellcorey, hello, hellyaa, helpme, heman, heroes, hesitate, hesitation, heycorey, homeowner, hwat, igotbitches, imhelping, imperialmarch, incandescent, inception, insideout, interessante, intoodeep, isp, jacksparrow, jaredcorey, jealouscorey, job, joecorey, jonocorey, jpeg, kid, kittycorey, koolaid, kosm, luke, mada, majestic, mando, mange, mikecorey, move, mozambique, mozambiquehere, mylilies, nani, no, nocorey, numb, octo, okaycorey, onlygame, oooh, ooohcorey, oughtaknow, oughttaknow, pacadub, pam, pamdub, pizza, planet, polka, popstars, psy, purple, queen, repcom, robcorey, ru4real, runaway, runts, sail, sandman, sandstorm, sax, scary, scotty, scream, sea, sheeit, shhh, shia, shortbiscuit, shreds, shrek, sif, silverscrapes, skrillex, slimshady, snout, snouts, something, songlist, sorry, spaghetti, spatulacity, spittingbars, spooky, start, ster, supplies, surprise, sushacorey, table, tazdingo, tempname, testificate, theyretricky, throwitontheground, tobecontinued, toblerone, trombone, turndown, turtles, verygood, washington, washingtonlong"""
        part2 = """ wasted, welcome, wise, wololo, xp, yes, yescorey, yooooo"""
        await context.send(f"""Here's my archive of ancient history:\n{part1}""")
        await context.send(f"""Oh, found a bit more:\n{part2}""")
        beautifulOrderedDictionary = OrderedDict(sorted(songdict.items(), key=lambda x: x[1]['playcount'], reverse=True))



def setup(bot):
    bot.add_cog(playsongs(bot))
    bot.add_cog(acquisition(bot))
    bot.add_cog(songs(bot))