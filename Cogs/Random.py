from discord.ext import commands
from random import randint as rnum


class Random:

    def __init__(self, sparcli):
        self.sparcli = sparcli


    @commands.command()
    async def coinflip(self):
        '''Gives a random result of heads or tails
        Usage :: coinflip'''

        # Get the result
        coinResultTable = {0:'Heads',1:'Tails'}
        result = coinResultTable[rnum(0, 1)]

        # Be a cheeky feck ;3
        if rnum(0, 100) == 73:
            result = 'The coin landed on its side .-.'

        # Print out to user
        await self.sparcli.say(result)


def setup(bot):
    bot.add_cog(Random(bot))
