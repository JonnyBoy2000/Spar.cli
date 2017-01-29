from discord.ext import commands
from discord import Member
from requests import get
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, checkPerm
from Utils.Permissions import permissionChecker, botPermission


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True)
    @permissionChecker(check='ban_members', compare=True)
    @botPermission(check='ban_members', compare=True)
    async def ban(self, ctx, user:Member=None, *, reason: str='Unspecified'):
        '''Bans a user from the server.
        Usage :: ban <Mention> <Reason...>'''

        await self.sparcli.ban(user)
        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{0}** `({0.id})` has been banned for reason `{1}`.'.format(user, reason))

    @commands.command(pass_context=True)
    @permissionChecker(check='kick_members', compare=True)
    @botPermission(check='kick_members', compare=True)
    async def kick(self, ctx, user: Member, *, reason: str=None):
        '''Kicks a user from the server.
        Usage :: kick <Mention> <Reason...>'''

        await self.sparcli.kick(user)
        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{0}** `({0.id})` has been kicked for reason `{1}`.'.format(user, reason))

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_messages')
    @botPermission(check='manage_messages')
    async def purge(self, ctx, amount: int):
        '''Deletes a number of messages from a channel
        Usage :: purge <Number>'''

        # Make sure the calling member isn't an idiot
        if amount >= 500:
            await self.sparcli.say('That number is too large. Please tone it down a notch.')
            return

        # Use the API's purge feature
        amount += 1
        deleted = await self.sparcli.purge_from(ctx.message.channel, limit=amount)
        deletedAmount = len(deleted)
        await self.sparcli.say('Removed `{}` messages.'.format(deletedAmount))

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_nicknames', compare=True)
    @botPermission(check='manage_nicknames', compare=True)
    async def rename(self, ctx, user:Member, *, name:str=None):
        '''Changes the nickname of a member
        Usage :: rename <UserMention> <Name>'''

        await self.sparcli.change_nickname(user, name)
        await self.sparcli.say('Name updated successfully.')

    @commands.command(pass_context=True, aliases=['servericon'])
    @permissionChecker(check='manage_server')
    @botPermission(check='manage_server')
    async def serverimage(self, ctx, *, icon:str=None):
        '''Changes the icon of the server
        Usage :: serverimage <ImageURL>
              :: serverimage <ImageUpload>'''

        # Sees if there's an image as an icon
        if icon != None:
            pass
        # Gets it from the attachments
        else:
            try:
                icon = ctx.message.attachments[0]['url']
            except (KeyError, IndexError):
                return

        # Sets it as the server image
        server = ctx.message.server
        await self.sparcli.edit_server(server, icon=get(icon).content)
        await self.sparcli.say('Server icon has been updated.')



def setup(bot):
    bot.add_cog(Admin(bot))
