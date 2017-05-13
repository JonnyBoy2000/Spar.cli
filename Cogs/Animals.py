from aiohttp import get 
from random import choice, randint
from discord.ext import commands 
from Cogs.Utils.Messages import makeEmbed


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

    @commands.command(pass_context=True)
    async def doggo(self, ctx):
        '''
        Gives a random picture of a doggo
        '''

        await self.randomSubredditImages(ctx, 'Dog', 'puppy')

    @commands.command(pass_context=True)
    async def fox(self, ctx):
        '''
        Gives a random picture of a fox
        '''

        await self.randomSubredditImages(ctx, 'Fox', 'foxes')

    async def randomSubredditImages(self, ctx, animal, subreddit):
        await self.sparcli.send_typing(ctx.message.channel)

        if self.subredditCache.get('{}_Timeout'.format(animal), 10) == 10:
            self.subredditCache['{}_Timeout'.format(animal)] = -1
            async with get('https://www.reddit.com/r/{}/.json'.format(subreddit)) as r:
                data = await r.json()
            o = []
            for i in data['data']['children']:
                if i['data'].get('post_hint', None) == 'image':
                    o.append(i['data']['url'])
            self.subredditCache['{}'.format(animal)] = o 

        randomDog = choice(self.subredditCache['{}'.format(animal)])
        self.subredditCache['{}_Timeout'.format(animal)] += 1
        em = makeEmbed(image=randomDog, colour=randint(0, 0xFFFFFF))
        await self.sparcli.say(embed=em)


def setup(bot):
    bot.add_cog(Animals(bot))
