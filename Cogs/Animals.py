from aiohttp import get 
from random import choice, randint
from discord.ext import commands 


class Animals:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.subredditCache = {}

    @commands.command(pass_context=True, aliases=['🐱'])
    async def cat(self, ctx):
        '''
        Gives a random picture of a cat.
        '''

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.channel)

        while True:
            try:
                # async with get('http://thecatapi.com/api/images/get?format=src') as r:
                #     page = r.url
                # break

                async with get('http://random.cat/meow') as r:
                    data = await r.json()
                page = data['file']
                break
            except Exception:
                pass

        # Give the url of the loaded page
        # await self.sparcli.say(page)
        em = makeEmbed(image=page, colour=randint(0, 0xFFFFFF))
        await self.sparcli.say(embed=em)

def setup(bot):
    bot.add_cog(Animals(bot))
