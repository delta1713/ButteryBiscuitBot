# Biscuit Bot Main File
# This should be mostly empty

# Contains commands:
# Restart
# Load Extensions
# Unload extensions
# Reload extensions


# ----------------- Imports -----------------------


import os
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import psutil
import logging
import pathlib
import biscuitfunctions as bf

# ----------------- Initialization -----------------------
print("""-------------------------------------------------
-------------------------------------------------
STARTING BISCUIT BOT
-------------------------------------------------
-------------------------------------------------""")
print("current time is: ", datetime.now())
print("discord api version: ", discord.__version__)



newstart = {'restart' : 'false'}


# ----------------- Initialize Bot -----------------------
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print("Token loaded from dotenv")
bot = commands.Bot(command_prefix="!")

biscuitchannel = 742482393587515555
print("biscuit channel: ", biscuitchannel)

botlog = 739510798099152916
print("bot log: ", botlog)

bc = bot.get_channel(biscuitchannel)
bl = bot.get_channel(botlog)

# ----------------- Make check for privledges ----------------- 
async def tesspriv(context):
    return bf.getprivs(context) == 'tesseract'
    
async def quaidpriv(context):
    return bf.getprivs(context) in ['quaid', 'tesseract']
# ----------------- Restart Bot Command -----------------------
@bot.command(
    name='restart',
    description='restart bot, role limited',
    pass_context=True,
)
@commands.check(quaidpriv)
async def restart_program(context):
    bc = bot.get_channel(botlog)
    await bc.send("Restarted by " +  str(context.message.author))
    newstart['restart'] = 'true'
    bf.writedictcsv(newstart, 'restart')
    for x in bot.voice_clients:
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

# ----------------- Extension Commands -----------------------

@bot.command(
    name='loadext',
    pass_context=True)
@commands.check(tesspriv)
async def loadext(context, *args):
    for ext in args:
        try:
            bot.load_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} loaded".format(ext))
    
    
@bot.command(
    name='unloadext',
    pass_context=True)
@commands.check(tesspriv)
async def unloadext(context, *args):
    for ext in args:
        try:
            bot.unload_extension(ext)
        except (AttributeError, ImportError) as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.message.channel.send("{} unloaded".format(ext))
        
        
@bot.command(
    name='reloadext',
    pass_context=True)
@commands.check(tesspriv)
async def reloadext(context, *args):
    for ext in args:
        try:
            bot.reload_extension(ext)
            await context.message.channel.send("{} reloaded".format(ext))
            print(f"----------------- \nReloaded {ext}\n ----------------- ")
        except Exception as e:
            await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            print("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        
        

# ----------------- Start the bot -----------------------

startup_extensions = ["rng", "tesseract", "pictures", "admin", "general", "listeners", 'songs', 'tts']

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
