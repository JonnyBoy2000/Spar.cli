from discord.ext import commands
from discord import Embed
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

        # https://discordapi.com/permissions.html
        clientID = '252880131540910080'
        permissionsID = '469888119'
        baseLink = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'
        inviteLink = baseLink.format(clientID, permissionsID)
        em = makeEmbed(user=self.sparcli.user, values={'Invite me!':'[Click here!]({})'.format(inviteLink)})
        await self.sparcli.say('', embed=em)

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
        Usage :: info <UserPing>'''

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
        embedMessage = makeEmbed(name='{}'.format(
            userOne), icon=userIcon, values=userInfo)

        # Send it out to the user
        await self.sparcli.say(userIcon, embed=embedMessage)

    @commands.command(pass_context=True, aliases=['clear'])
    async def clean(self, ctx, amount: int=50, user: str=None):
        '''Checks a given amount of messages, and removes ones from a certain user
        Defaults to 50, with the user being the bot
        Usage :: clean
              :: clean <Number>
              :: clean <Number> <UserMention>'''

        # Check if the user has mentioned anyone
        messagePings = getMentions(ctx.message, 1)
        if type(messagePings) == str:
            user = self.sparcli.user
        else:
            user = messagePings[0]

        # Set up the check
        cleanCheck = lambda m: m.author.id == user.id

        # Purge accurately
        deleted = await self.sparcli.purge_from(ctx.message.channel, limit=amount, check=cleanCheck)
        await self.sparcli.say('Cleaned `{}` messages from the channel.'.format(len(deleted)))


def setup(bot):
    bot.add_cog(Misc(bot))
