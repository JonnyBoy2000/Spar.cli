from discord.ext import commands


class Misc:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command()
    async def invite(self):
        '''Gives the bot's invite link
        Usage :: invite'''

        await self.sparcli.say('https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=sparcli&permissions=0')

    @commands.command()
    async def git(self):
        '''Gives the link to the bot's GitHub page/code
        Usage :: git'''

        await self.sparcli.say('https://github.com/4Kaylum/Spar.cli/')

    @commands.command()
    async def echo(self, *, content: str):
        '''Makes the bot print back what the user said
        Usage :: echo <Content>'''
        
        await self.sparcli.say(content)


def setup(bot):
    bot.add_cog(Misc(bot))
