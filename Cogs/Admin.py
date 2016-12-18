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

        # See if the user is allowed to run the command
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

        # See if the user is allowed to run the command
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

    @commands.command(pass_context=True)
    async def purge(self, ctx, amount: int):
        '''Deletes a number of messages from a channel
        Usage :: purge <Number>'''

        # See if the user is allowed to run the command
        permReturn = getPermissions(
            ctx.message.channel, 'manage_messages', ctx.message.author)

        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        if amount > 500:
            await self.sparcli.say('That number is too large. Please tone it down a notch.')

        # Use the API's purge feature
        amount += 1
        deleted = await self.sparcli.purge_from(ctx.message.channel, limit=amount)
        deletedAmount = len(deleted)
        await self.sparcli.say('Removed `{}` messages.'.format(deletedAmount))


def setup(bot):
    bot.add_cog(Admin(bot))
