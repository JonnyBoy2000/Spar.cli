from discord.ext import commands
from discord import Channel
from Cogs.Utils.Discord import getTextRoles
from Cogs.Utils.Configs import getServerJson, saveServerJson
from Cogs.Utils.GuiConfig import addEmojiList, updateFromEmoji, updateFromMessage
from Cogs.Utils.Permissions import permissionChecker


class Config:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def enable(self, ctx, toChange: str):
        '''Enables a certain messagetype from the bot's server configuration
        Usage :: enable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await self.sparcli.say('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), True)

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def disable(self, ctx, toChange: str):
        '''Disables a certain messagetype from the bot's server configuration
        Usage :: disable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await self.sparcli.say('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), False)

    async def toggleSetting(self, ctx, whatToSet, toSetTo):
        '''Sets a server config messagetype to true or false depending on the
        command that called it'''

        # Make line length shorter
        serverID = ctx.message.server.id

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Toggles'][whatToSet] = toSetTo
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await self.sparcli.say('The messagetype `{}` has been set to `{}`'.format(whatToSet, toSetTo))

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def set(self, ctx, toChange: str, channel: Channel):
        '''Sets a messagetype's output to a certain channel
        Usage :: set <MessageType> <ChannelPing>
        MessageTypes :: joins, leaves, bans, etc'''

        # If the user can use it, the serverconfig will be changed
        settableChannels = getServerJson('Default')['Channels']
        if toChange.title() not in settableChannels:
            await self.sparcli.say('That isn\'t a messagetype you can set. Try something from `{}`'.format(
                ', '.join(settableChannels.keys())))
            return

        serverID = ctx.message.server.id
        toChange = toChange.title()

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Channels'][whatToSet] = channel.id
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await self.sparcli.say('The messagetype `{0}` output has been set to {1.mention}, with ID `{1.id}`'.format(whatToSet, channel))

    @commands.command(pass_context=True, name='prefix', aliases=['setprefix', 'prefixset'])
    @permissionChecker(check='administrator')
    async def prefixCommand(self, ctx, prefix: str):
        '''Changes the command prefix for the server
        Usage :: prefix <New Preifx>'''

        # Set up some variables to keep line length short
        serverID = ctx.message.server.id

        # Load and save the command prefix
        serverSettings = getServerJson(serverID)
        serverSettings['CommandPrefix'] = prefix
        saveServerJson(serverID, serverSettings)

        # Print out to the user
        await self.sparcli.say('The command prefix for this server has been set to `{}`'.format(prefix))

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def setup(self, ctx):
        '''Gives you a reaction-based configuration dialogue
        Usage :: setup'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel
        serverID = ctx.message.server.id
        
        # Load current configuration
        serverSettings = getServerJson(serverID)
        defaultSettings = getServerJson('Default')

        # Make a lambda so I can easily check the author
        messageAuthor = lambda x: x.author.id == author.id

        # Tell the user to get off of mobile
        startup = await self.sparcli.say('This command works with reactions. Thus, if you are on mobile, it will not work. If you wish to proceed, send a message saying `yes`. Otherwise, the command will abort.')
        response = await self.sparcli.wait_for_message(author=author, channel=channel)
        if response.content.lower() == 'yes':
            await self.sparcli.delete_message(startup)
            await self.sparcli.delete_message(response)
        else:
            await self.sparcli.say('This command is aborting.')
            return

        # Work on each type of toggle enable
        toggleTypes = serverSettings['Toggles'].keys()
        channelTypes = defaultSettings['Channels'].keys()

        for i in toggleTypes:
            serverSettings = await updateFromEmoji(self.sparcli, ctx, serverSettings, i, serverSettings['Toggles'][i])

            # See if you need to set it up with a channel
            if i in channelTypes and serverSettings['Toggles'][i] == True:
                serverSettings = await updateFromMessage(self.sparcli, ctx, serverSettings, i)

        # Tell the user that we're done
        await self.sparcli.say('Alright, everything is updated!')

        # Save it all to file
        saveServerJson(serverID, serverSettings)


def setup(bot):
    bot.add_cog(Config(bot))
