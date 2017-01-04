from discord.ext import commands
from discord import Member
from requests import get
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

    @commands.command(pass_context=True)
    @checkPerm(check='manage_nicknames')
    async def rename(self, ctx, user:Member, *, name:str=None):
        '''Changes the nickname of a member
        Usage :: rename <UserMention> <Name>'''

        try:
            await self.sparcli.change_nickname(user, name)
            await self.sparcli.say('Name updated successfully.')
        except:
            await self.sparcli.say('I was unable to change that person\'s nickname.')

    @commands.command(pass_context=True, aliases=['servericon'])
    @checkPerm(check='manage_server')
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
