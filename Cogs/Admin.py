from discord.ext import commands
from discord import Member
from requests import get
from Cogs.Utils.Permissions import permissionChecker, botPermission


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command()
    @permissionChecker(check='ban_members', compare=True)
    @botPermission(check='ban_members', compare=True)
    async def ban(self, ctx, user:Member=None, *, reason: str='Unspecified'):
        '''
        Bans a user from the server.
        '''

        serverData = getServerJson(ctx.guild.id)
        enabled = serverData['Toggles']['Bans']
        channel = serverData['Channels']['Bans']
        channelSend = ctx.message.guild.get_channel(int(channel))

        await ctx.guild.ban(user)
        if enabled:
            await channelSend.send('**{0}** `({0.id})` has been banned for reason `{1}`.'.format(user, reason))
        await ctx.send('👌')

    @commands.command()
    @permissionChecker(check='kick_members', compare=True)
    @botPermission(check='kick_members', compare=True)
    async def kick(self, ctx, user: Member, *, reason: str=None):
        '''
        Kicks a user from the server.
        '''

        serverData = getServerJson(ctx.guild.id)
        enabled = serverData['Toggles']['Kicks']
        channel = serverData['Channels']['Kicks']
        channelSend = ctx.message.guild.get_channel(int(channel))

        await ctx.guild.kick(user)
        if enabled:
            await channelSend.send('**{0}** `({0.id})` has been kicked for reason `{1}`.'.format(user, reason))
        await ctx.send('👌')

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_messages')
    @botPermission(check='manage_messages')
    async def purge(self, ctx, amount: int):
        '''Deletes a number of messages from a channel
        Usage :: purge <Number>'''

        # Make sure the calling member isn't an idiot
        if amount >= 500:
            await ctx.send('That number is too large. Please tone it down a notch.')
            return

        # Use the API's purge feature
        amount += 1
        deleted = await ctx.message.channel.purge(limit=amount)
        deletedAmount = len(deleted)
        await ctx.send('Removed `{}` messages.'.format(deletedAmount))

    @commands.command()
    @permissionChecker(check='manage_nicknames', compare=True)
    @botPermission(check='manage_nicknames', compare=True)
    async def rename(self, ctx, user:Member, *, name:str=None):
        '''Changes the nickname of a member
        Usage :: rename <UserMention> <Name>'''

        await user.edit(nick=name)
        await ctx.send('Name updated successfully.')

    @commands.command(aliases=['servericon'])
    @permissionChecker(check='manage_guild')
    @botPermission(check='manage_guild')
    async def serverimage(self, ctx, *, icon:str):
        '''
        Changes the icon of the server.
        '''

        # Sets it as the guild image
        guild = ctx.message.guild
        await guild.edit(icon=get(icon).content)
        await ctx.send('Server icon has been updated.')


def setup(bot):
    bot.add_cog(Admin(bot))
