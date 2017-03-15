from discord.ext import commands
from discord import TextChannel
from Cogs.Utils.Discord import getTextRoles
from Cogs.Utils.Configs import getServerJson, saveServerJson
from Cogs.Utils.GuiConfig import addEmojiList, updateFromEmoji, updateFromMessage
from Cogs.Utils.Permissions import permissionChecker


class Config:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command()
    @permissionChecker(check='administrator')
    async def enable(self, ctx, toChange: str):
        '''Enables a certain messagetype from the bot's server configuration
        Usage :: enable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await ctx.send('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), True)

    @commands.command()
    @permissionChecker(check='administrator')
    async def disable(self, ctx, toChange: str):
        '''Disables a certain messagetype from the bot's server configuration
        Usage :: disable <MessageType>
        MessageTypes :: joins, leaves, bans, serverupdates, channelupdates'''

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Toggles']:
            await ctx.send('That isn\'t something you can configure. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Toggles'].keys())))

        # Change the thingy
        await self.toggleSetting(ctx, toChange.title(), False)

    async def toggleSetting(self, ctx, whatToSet, toSetTo):
        '''Sets a server config messagetype to true or false depending on the
        command that called it'''

        # Make line length shorter
        serverID = ctx.message.guild.id

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Toggles'][whatToSet] = toSetTo
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await ctx.send('The messagetype `{}` has been set to `{}`'.format(whatToSet, toSetTo))

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def set(self, ctx, toChange: str, channel: TextChannel):
        '''Sets a messagetype's output to a certain channel
        Usage :: set <MessageType> <ChannelPing>
        MessageTypes :: joins, leaves, bans, etc'''

        # If the user can use it, the serverconfig will be changed
        settableChannels = getServerJson('Default')['Channels']
        if toChange.title() not in settableChannels:
            await ctx.send('That isn\'t a messagetype you can set. Try something from `{}`'.format(
                ', '.join(settableChannels.keys())))
            return

        serverID = ctx.message.guild.id
        toChange = toChange.title()

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Channels'][whatToSet] = channel.id
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await self.sparcli.say('The messagetype `{0}` output has been set to {1.mention}, with ID `{1.id}`'.format(whatToSet, channel))

    @commands.command()
    @permissionChecker(check='administrator')
    async def youare(self, ctx, addRemove: str, *, whatToChange: str):
        '''Allows you to change which roles are self-assignable
        Usage :: youare not <RoleName>
              :: youare not <RolePing>
              :: youare del <RoleName>
              :: youare now <RoleName>
              :: youare add <RolePing>'''

        roleToGive = await getTextRoles(ctx)
        if roleToGive is 0:
            return

        # Set up where the subcommand will redirect to
        subcommands = {'not': True,
                       'del': True,
                       'delete': True,
                       'add': False,
                       'now': False}
        calledSubcommand = subcommands[addRemove.lower()]

        # Read from the server configs
        serverSettings = getServerJson(ctx.message.guild.id)
        allowableIDs = serverSettings['SelfAssignableRoles']

        # Fliter if add or remove
        if calledSubcommand:
            try:
                allowableIDs.remove(roleToGive.id)
            except ValueError:
                await ctx.send('This role isn\'t self-assignable.')
                return
        else:
            if roleToGive.id not in allowableIDs:
                allowableIDs.append(roleToGive.id)
            else:
                await ctx.send('This role can already be self-assigned.')
                return

        # Plonk the settings back into the file storage
        serverSettings['SelfAssignableRoles'] = allowableIDs
        saveServerJson(ctx.message.guild.id, serverSettings)
        canItBeAssigned = {False: 'can now be', True: 'can no longer be'}[calledSubcommand]

        # Print out to the user
        await ctx.send('The role `{0.name}` with ID `{0.id}` {1} self-assigned.'.format(
            roleToGive, canItBeAssigned))

    @commands.command(aliases=['setprefix', 'prefixset'])
    @permissionChecker(check='administrator')
    async def prefix(self, ctx, prefix: str):
        '''Changes the command prefix for the server
        Usage :: prefix <New Preifx>'''

        # Set up some variables to keep line length short
        serverID = ctx.message.guild.id

        # Load and save the command prefix
        serverSettings = getServerJson(serverID)
        serverSettings['CommandPrefix'] = prefix
        saveServerJson(serverID, serverSettings)

        # Print out to the user
        await ctx.send('The command prefix for this server has been set to `{}`'.format(prefix))

    @commands.command()
    @permissionChecker(check='administrator')
    async def setup(self, ctx):
        '''Gives you a reaction-based configuration dialogue
        Usage :: setup'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel
        serverID = ctx.message.guild.id
        
        # Load current configuration
        serverSettings = getServerJson(serverID)
        defaultSettings = getServerJson('Default')

        # Make a lambda so I can easily check the author
        messageAuthor = lambda x: x.author.id == author.id

        # Work on each type of toggle enable
        toggleTypes = serverSettings['Toggles'].keys()
        channelTypes = defaultSettings['Channels'].keys()

        for i in toggleTypes:
            serverSettings = await updateFromEmoji(self.sparcli, ctx, serverSettings, i, serverSettings['Toggles'][i])

            # See if you need to set it up with a channel
            if i in channelTypes and serverSettings['Toggles'][i] == True:
                serverSettings = await updateFromMessage(self.sparcli, ctx, serverSettings, i)

        # Tell the user that we're done
        await ctx.send('Alright, everything is updated!')

        # Save it all to file
        saveServerJson(serverID, serverSettings)


def setup(bot):
    bot.add_cog(Config(bot))
