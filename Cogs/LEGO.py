from discord.ext import commands 
try:
    from brickfront import Client
except ImportError:
    raise Exception('You need to install Brickfront for this class to work.')
from collections import OrderedDict
from random import choice
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Cogs.Utils.Discord import makeEmbed
from Cogs.Utils.Configs import getTokens


class LEGO:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.brickClient = Client(getTokens()['Brickset']['Secret'])

    @commands.command()
    async def legoset(self, ctx, *, query: str):
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
        e = makeEmbed(name=name, image=image, values=o)
        await ctx.send('', embed=e)


def setup(bot):
    bot.add_cog(LEGO(bot))
