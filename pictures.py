from discord.ext import commands
import discord
import random

root = "/gitbot/ButteryBiscuitBot/pictures/"

class pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='chrispenis',
        aliases=['ChrisPenis', 'Chrispenis'],
        description='Cool wafers to desired...',
        pass_context=True,
    )
    async def chrispenis(self, context):
        """
        ChrisPenis
        """
        await context.send(file=discord.File(root + 'chrispenis.jpg'))
        # this sends the file directly to discord, there is a way to do so with filelike objects
        # (dunno what those are) but I couldn't get it to work
    
    @commands.command(
        name='biscuitface',
        aliases=['biscuitfaces', 'BiscuitFace', 'BiscuitFaces'],
        description='They are buttery...',
        pass_context=True,
    )
    async def biscuitface(self, context):
        """
        biscuitfaces
        """
        await context.send(file=discord.File('biscuitface.jpg'))
    
    @commands.command(
        name='pepperoni',
        aliases=['Pepperoni', 'heyyotony', 'freshpepperoni', 'cleverthoughts', 'CleverThoughts'],
        description='Hey yo tony, whered you get that fresh pepperoni',
        pass_context=True,
    )
    async def pepperoni(self, context):
        """
        pepperoni
        """
        await context.send(file=discord.File(root + 'pepperoni.png'))
    
    
    @commands.command(
        name='stream',
        aliases=[],
        description='stream it for him',
        pass_context=True,
    )
    async def stream(self, context):
        """
        stream
        """
        await context.send(file=discord.File(root + 'stream.png'))
    
    
    @commands.command(
        name='trongle',
        aliases=['Trongle', 'trongleman', 'Trongleman'],
        description='TRONGLE MAN!',
        pass_context=True,
    )
    async def trongle(self, context):
        """
        trongle man
        """
        await context.send(file=discord.File(root + 'trongle.jpg'))
        
    
    @commands.command(
        name='metatrongle',
        aliases=['MetaTrongle', 'sushtrongle'],
        description='it\'s trongle man, but meta',
        pass_context=True,
    )
    async def metatrongle(self, context):
        """
        meta trongle
        """
        await context.send(file=discord.File(root + 'metatrongle.png'))
        
    
    @commands.command(
        name='hyd',
        aliases=['hellyeadog', 'hellyeahdog', 'hellyeahdawg'],
        description='helll yeaaaaaa',
        pass_context=True,
    )
    async def hyd(self, context):
        """
        hell yea dawg
        """
        hydlist = [root + 'hyd.jpg', root + 'hyd2.jpg', root + 'hyd3.jpg', root + 'hyd4.jpg', root + 'hyd5.jpg', root + 'hyd6.jpg', root + 'hyd7.jpg', root + 'hyd8.jpg']
        rnum = random.randint(0,len(hydlist)-1)
        await context.send(file=discord.File(hydlist[rnum]))
        
    @commands.command(
        name='hyduck',
        aliases=[],
        description='hell yeaaaaa duck',
        pass_context=True)
    async def hyduck(self, context):
        await context.send(file=discord.File(root + 'hyduck1.jpg'))

def setup(bot):
    bot.add_cog(pictures(bot))