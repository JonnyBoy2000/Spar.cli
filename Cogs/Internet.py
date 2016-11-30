from discord.ext import commands 
from requests import get


class Internet:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command()
    async def pun(self):
        '''Grabs a random pun form around the internet
        Usage :: pun'''

        pass

    @commands.command()
    async def cat(self):
        '''Gives a random picture of a cat
        Usage :: cat'''

        # Loop to keep track of rate limiting
        while True:
            # Try to load the page
            try:
                page = get('http://thecatapi.com/api/images/get?format=src')
                break
            except:
                pass

        # Give the url of the loaded page
        returnUrl = page.url
        await self.sparcli.say(returnUrl)

    @commands.command()
    async def pun(self):
        '''Gives a random pun from the depths of the internet
        Usage :: pun'''

        # Read from page
        page = get('http://www.punoftheday.com/cgi-bin/randompun.pl')

        # Scrape the raw HTML
        rawPun = page.text.split('dropshadow1')[1][6:].split('<')[0]
        
        # Boop it out
        await self.sparcli.say(rawPun)


def setup(bot):
    bot.add_cog(Internet(bot))
