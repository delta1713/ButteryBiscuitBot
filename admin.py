from discord.ext import commands
import biscuitfunctions as bf
async def fixprivs(context):
    return bf.getprivs(context) in ['quaid', 'quaidling', 'tesseract']
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='getid',
        pass_context = True)
    async def getid(self, context):
        authid = context.author.id
        await context.author.send(f"Your id is {authid}")
        await context.message.delete()
        
        
    @commands.command(
        name='fix',
        pass_context = True,
        help="Takes no arguments.\nShould fix most issues with the bot.\nRun once and check problem, if it persists run it again.\nRunning more than twice does not help.")
    @commands.check(fixprivs)
    async def fix(self, context):
        await context.send("I'm trying to fix myself!", delete_after=60)
        connections = ""
        print(self.bot.voice_clients)
        if self.bot.voice_clients:
            for x in self.bot.voice_clients:
                await x.disconnect(force=True)
                connections = connection + f"{x.channel}, "
            await context.send(f"I disconnected from the following channels: {connections[:-2]}", delete_after=60)
            await context.send("If that doesn't work, try running !fix again")
            return
        else:
            await context.send("I am not connected to any voice channels, reloading all extensions", delete_after=60)
        extensions = list(self.bot.extensions.keys())
        print(extensions)
        for ext in extensions:
            try:
                self.bot.reload_extension(ext)
                await context.message.channel.send("```{} reloaded```".format(ext), delete_after=60)
                print(f"----------------- \nReloaded {ext}\n ----------------- ")
            except Exception as e:
                await context.message.channel.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)), delete_after=60)
                print("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        await context.send("I have tried all my troubleshooting, if I'm still not working talk to my dad.", delete_after=60)
            
def setup(bot):
    bot.add_cog(admin(bot))
