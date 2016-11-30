from discord.ext import commands


class Misc:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command()
    async def invite():
        '''invite
        Gives the bot's invite link'''
        await self.sparcli.say('https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=sparcli&permissions=0')

    @commands.command()
    async def git():
        '''git
        Gives the link to the bot's GitHub page/code'''
        await self.sparcli.say('https://github.com/4Kaylum/Spar.cli/')

    @commands.command()
    async def echo(*, content: str):
        '''echo <Content>
        Makes the bot print back what the user said'''
        await self.sparcli.say(content)

def setup(bot):
    bot.add_cog(Misc(bot))
