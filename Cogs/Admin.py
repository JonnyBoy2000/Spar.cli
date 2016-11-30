from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: str, *, reason: str=None):
        '''Bans a user from the server.
        Usage :: ban <Mention> <Reason...>'''

        # Get the tagged users from the message
        taggedUser = ctx.message.mentions

        # If nobody was tagged
        if ctx.message.mentions == []:
            await self.sparcli.say('You need to tag a user to ban.')
            return

        # If more than one person is tagged
        elif len(ctx.message.mentions) > 1:
            await self.sparcli.say('You can only tag one user to ban.')
            return

        permReturn = getPermissions(
            ctx.message.channel, 'ban', ctx.message.author, taggedUser[0])

        if permReturn == 'not allowed':
            await self.sparcli.say('You do not have permission to ban members.')
            return
        elif permReturn == 'too low':
            await self.sparcli.say('Your role is not high enough to ban that user.')
            return

        # Try and ban the user
        try:
            await self.sparcli.ban(taggedUser[0])
        except:
            await self.sparcli.say('I was unable to ban that user.')
            return

        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{}** has been banned.'.format(taggedUser[0]))

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: str, *, reason: str=None):
        '''Kicks a user from the server.
        Usage :: kick <Mention> <Reason...>'''

        # Get the tagged users from the message
        taggedUser = ctx.message.mentions

        # If nobody was tagged
        if ctx.message.mentions == []:
            await self.sparcli.say('You need to tag a user to kick.')
            return

        # If more than one person is tagged
        elif len(ctx.message.mentions) > 1:
            await self.sparcli.say('You can only tag one user to kick.')
            return

        permReturn = getPermissions(
            ctx.message.channel, 'kick', ctx.message.author, taggedUser[0])

        if permReturn == 'not allowed':
            await self.sparcli.say('You do not have permission to kick members.')
            return
        elif permReturn == 'too low':
            await self.sparcli.say('Your role is not high enough to kick that user.')
            return

        # Try and kick the user
        try:
            await self.sparcli.kick(taggedUser[0])
        except:
            await self.sparcli.say('I was unable to kick that user.')
            return

        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{}** has been kicked.'.format(taggedUser[0]))


def setup(bot):
    bot.add_cog(Admin(bot))
