from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, getMentions


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: str, *, reason: str=None):
        '''Bans a user from the server.
        Usage :: ban <Mention> <Reason...>'''

        # Get the tagged users from the message
        taggedUser = getMentions(ctx.message, 1)
        if type(taggedUser) == str:
            await self.sparcli.say(taggedUser)
            return

        permReturn = getPermissions(
            ctx.message.channel, 'ban', ctx.message.author, taggedUser[0])

        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
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
        taggedUser = getMentions(ctx.message, 1)
        if type(taggedUser) == str:
            await self.sparcli.say(taggedUser)
            return

        permReturn = getPermissions(
            ctx.message.channel, 'kick', ctx.message.author, taggedUser[0])

        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
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
