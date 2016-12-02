from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions
from Utils.Configs import getServerJson, saveServerJson


class Config:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True)
    async def enable(self, ctx, toChange: str):
        '''Enables a certain messagetype from the bot's server configuration
        Usage :: enable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await self.sparcli.say('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), True)

    @commands.command(pass_context=True)
    async def disable(self, ctx, toChange: str):
        '''Disables a certain messagetype from the bot's server configuration
        Usage :: disable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await self.sparcli.say('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), False)

    async def toggleSetting(self, ctx, whatToSet, toSetTo):
        # Make line length shorter
        serverID = ctx.message.server.id

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Toggles'][whatToSet] = toSetTo
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await self.sparcli.say('The messagetype `{}` has been set to `{}`'.format(whatToSet, toSetTo))


def setup(bot):
    bot.add_cog(Config(bot))
