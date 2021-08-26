from discord.ext import commands

vnumber = '0.3.5'

pnotes = """MOST RECENT PATCH NOTES:

Currently undergoing a major shift in back end framework.
(Note, due to this some functionality may temporarily be broken)

Added a roll dice function (NdN format).
Added a guessing game, guess the right number (out of 1000) and win a prize!."""

biscuits = """Here's my recipe for Buttermilk Biscuits

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


class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='version',
        aliases=['Version','v'],
        description='Return most recent bot version number',
        pass_context=True)
    async def version(self, context):
        await context.send(vnumber)

    @commands.command(
        name='patchnotes',
        aliases=['pnotes'],
        description='Most recent patch notes',
        pass_context=True)
    async def patchnotes(self, context):
        await context.send(pnotes)
        
    @commands.command(
        name='recipe',
        aliases=['biscuits'],
        description='How to make the MOST buttery biscuits',
        pass_context=True)
    async def recipe(self, context):
        await context.send(biscuits)
        
    @commands.command(
        name='deprecated',
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
    async def deprecated(self, context):
        await context.send("That command is deprecated, use !play <songname> instead, no pointy brackets.")
def setup(bot):
    bot.add_cog(general(bot))