from collections import OrderedDict
from random import choice
try:
    from brickfront import Client
except ImportError:
    raise Exception('You need to install Brickfront for this class to work.')
from discord.ext import commands
from Cogs.Utils.Messages import makeEmbed
from Cogs.Utils.Configs import getTokens


class LEGO:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.brickClient = Client(getTokens()['Brickset']['Secret'])

    @commands.command()
    async def legoset(self, *, query: str):
        '''Searches for a LEGO set'''

        sets = self.brickClient.getSets(query=query, pageSize=200)
        try:
            r = choice(sets)
        except IndexError:
            await self.sparcli.say('That query returned no results.')
            return            
        o = OrderedDict()
        name = r.name 
        image = r.imageURL
        o['Year Released'] = r.year 
        o['Theme'] = r.theme 
        o['Pieces'] = r.pieces 
        o['Minifigs'] = r.minifigs 
        if r.priceUK != None and r.priceUS != None:
            z = '£{}\n${}'.format(r.priceUK, r.priceUS)
        elif r.priceUK != None:
            z = '£{}'.format(r.priceUK)
        elif r.priceUS != None:
            z = '${}'.format(r.priceUS)
        else:
            z = 'None available.'
        o['Price'] = z
        e = makeEmbed(author=name, image=image, fields=o)
        await self.sparcli.say('', embed=e)


def setup(bot):
    bot.add_cog(LEGO(bot))
