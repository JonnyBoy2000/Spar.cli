from discord.ext import commands
from discord import Member
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, getMentions, checkPerm


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True)
    @checkPerm(check='ban_members')
    async def ban(self, ctx, user:Member=None, *, reason: str=None):
        '''Bans a user from the server.
        Usage :: ban <Mention> <Reason...>'''

        # Get the tagged users from the message
        if user == None:
            await self.sparcli.say('You need to tag a member in your message')
            return

        # See if the user is allowed to run the command on the given user
        permReturn = getPermissions(ctx=ctx, person=user, check='ban_members')
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Try and ban the user
        try:
            await self.sparcli.ban(user)
        except:
            await self.sparcli.say('I was unable to ban that user.')
            return

        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{0}** `({0.id})` has been banned.'.format(user))

    @commands.command(pass_context=True)
    @checkPerm(check='kick_members')
    async def kick(self, ctx, user: Member, *, reason: str=None):
        '''Kicks a user from the server.
        Usage :: kick <Mention> <Reason...>'''

        # See if the user is allowed to run the command
        permReturn = getPermissions(ctx=ctx, person=user, check='kick_members')
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Try and kick the user
        try:
            await self.sparcli.kick(user)
        except:
            await self.sparcli.say('I was unable to kick that user.')
            return

        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{0}** `({0.id})` has been kicked.'.format(taggedUser[0]))

    @commands.command(pass_context=True)
    @checkPerm(check='manage_messages')
    async def purge(self, ctx, amount: int):
        '''Deletes a number of messages from a channel
        Usage :: purge <Number>'''

        # Make sure the calling member isn't an idiot
        if amount > 500:
            await self.sparcli.say('That number is too large. Please tone it down a notch.')
            return

        # Use the API's purge feature
        amount += 1
        deleted = await self.sparcli.purge_from(ctx.message.channel, limit=amount)
        deletedAmount = len(deleted)
        await self.sparcli.say('Removed `{}` messages.'.format(deletedAmount))


def setup(bot):
    bot.add_cog(Admin(bot))
