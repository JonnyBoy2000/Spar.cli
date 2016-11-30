from discord.ext import commands
from datetime import datetime
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getMentions, makeEmbed


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

    @commands.command(pass_context=True)
    async def info(self, ctx):
        '''Gives info on the mentioned user
        Usage :: info <Mention>'''

        # Get the user who was pinged
        pingedUsers = getMentions(ctx.message, 1)
        if type(pingedUsers) == str:
            await self.sparcli.say(pingedUsers)
            return
        userOne = pingedUsers[0]

        # Generate a dictionary of their information
        userInfo = {'Username': userOne.name,
                    'Discriminator': userOne.discriminator,
                    'Display Name': userOne.display_name if userOne.display_name != None else userOne.name,
                    'ID': userOne.id,
                    'Bot': userOne.bot,
                    'Created': str(userOne.joined_at)[:-10],
                    'Age': str(datetime.now() - userOne.joined_at).split(",")[0],
                    'Roles': ', '.join([g.name for g in userOne.roles][1:])
                    }
        userIcon = userOne.avatar_url if userOne.avatar_url != None else userOne.default_avatar_url

        # Create an embed out of it
        embedMessage = makeEmbed(name='{}'.format(userOne), icon=userIcon, values=userInfo)

        # Send it out to the user
        await self.sparcli.say('', embed=embedMessage)


def setup(bot):
    bot.add_cog(Misc(bot))
