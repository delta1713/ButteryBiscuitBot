#------------------------------Picture Zone!-----------------------------
# Separate module for picture posting

import os
import asyncio # Needed for coroutine / await functionality, which discord.py is built around.
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

