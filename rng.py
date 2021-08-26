import random
from discord.ext import commands
import biscuitfunctions as bf

intoftheday = random.randint(1,1000)

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
    name = 'roll',
    pass_context=True)
    async def roll(self, context, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await context.send('Format has to be in NdN!')
            return
        if rolls > 20 or limit > 42069:
            await context.send("Yo, that's too much man.  I ain't doing more than 20 dice and no more than a d42069")
            return
        else:
            pass
        rollresult = ''
        rollsum = 0
        for r in range(rolls):
            i = random.randint(1, limit)
            rollresult += str(i) + ', '
            rollsum += i
        result = f"{context.author} rolled {rolls}d{limit} and got a {rollresult} for a total of {rollsum}"
        await context.send(result)
        
    @commands.command(
        name='guess',
        description = 'Guess a number between 1 and 1000',
        pass_context=True)
    async def guess(self, context, *args):
        global intoftheday
        try:
            userguess = int(args[0])
        except:
            await context.send("Yo, you gotta guess an integer")
        if userguess == intoftheday:
            await context.send(f"Congratulations {context.author}, you win!")
            intoftheday = random.randint(1,1000)
        else:
            await context.send(f"Dang, close. Try again if you want!")
    
    @commands.command(
        name='eightball',
        description = "Ask the bot's magic 8 ball for an answer",
        brief = "Magic 8 ball",
        pass_context=True,
        aliases = ['8ball', '8', 'magicball', 'shake'])
    async def eightball(self, context, *args):
        eightballlist = ["As I see it, yes.",
        "Ask again later",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Outlook good.",
        "Reply hazy, try again.",
        "Signs point to yes.",
        "Very doubtful.",
        "Without a doubt.",
        "Yes.",
        "Yes - definitely.",
        "You may rely on it."]
        rnum = random.randint(1,20)
        ans = eightballlist[rnum-1]
        await context.send(f"{bf.authname(context)}, 8 ball says: {ans}")
        
    @commands.command(
        name="rps",
        description="Play rock paper scissors with the biscuit bot!",
        brief="Play rock paper scissors with the bot!",
        pass_context=True,
        alias="rockpaperscissors")
    async def rps(self, context, *args):
        arg = args[0]
        print(dir(arg))
        rock = ["rock", "r", "rocks", "stone"]
        paper = ["paper", "p"]
        scissors = ["scissors", "s", "skissors", "scissor"]
        if arg in rock:
            await context.send(f"*plays paper*\nI win, you suck {bf.authname(context)}")
        elif arg in paper:
            await context.send(f"*plays scissors*\nI win, you suck {bf.authname(context)}")
        elif arg in scissors:
            await context.send(f"*plays rock*\nI win, you suck {bf.authname(context)}")
        else:
            await context.send("I don't know that move, make a legal move (rock, paper, scissor)")



def setup(bot):
    bot.add_cog(RNG(bot))