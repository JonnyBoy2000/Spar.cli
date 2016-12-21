from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, getMentions, getNonTaggedMentions
from Utils.Configs import getServerJson, saveServerJson
from Utils.GuiConfig import addEmojiList, updateFromEmoji, updateFromMessage


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
    async def set(self, ctx, toChange: str):
        '''Sets a messagetype's output to a certain channel
        Usage :: set <MessageType> <ChannelPing>
        MessageTypes :: joins, leaves, bans'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

        # If the user can use it, the serverconfig will be changed
        if toChange.title() not in getServerJson('Default')['Channels']:
            await self.sparcli.say('That isn\'t a messagetype you can set. Try something from `{}`'.format(
                ', '.join(getServerJson('Default')['Channels'].keys())))

        # Change the thingy
        await self.setSettings(ctx, toChange.title())

    async def setSettings(self, ctx, whatToSet):
        '''Sets a certain server config to a string'''

        # Get any tagged channels
        mentions = getMentions(ctx.message, 1, 'channel')
        if type(mentions) == str:
            await self.sparcli.say(mentions)
            return
        mentions = mentions[0]

        # Make line length shorter
        serverID = ctx.message.server.id

        # Changes the server settings
        serverSettings = getServerJson(serverID)
        serverSettings['Channels'][whatToSet] = mentions.id
        saveServerJson(serverID, serverSettings)

        # Print out to user
        await self.sparcli.say('The messagetype `{0}` output has been set to {1.mention}, with ID `{1.id}`'.format(whatToSet, mentions))

    @commands.group(pass_context=True)
    async def youare(self, ctx, addRemove: str, *, whatToChange: str):
        '''Allows you to change which roles are self-assignable
        Usage :: youare not <RoleName>
              :: youare not <RolePing>
              :: youare del <RoleName>
              :: youare now <RoleName>
              :: youare add <RolePing>'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

        # Try and see if the role was pinged
        roleToGive = getMentions(ctx.message, 1, 'role')
        if type(roleToGive) == str:

            # If wasn't pinged - see if it exists
            roleToGive = getNonTaggedMentions(
                ctx.message.server, whatToChange, 'role')
            if type(roleToGive) == str:

                # The user hates us
                await self.sparcli.say(roleToGive)
                return

        # Turn the role list into a role
        roleToGive = roleToGive[0]

        # Set up where the subcommand will redirect to
        subcommands = {'not': True,
                       'del': True,
                       'delete': True,
                       'add': False,
                       'now': False}
        calledSubcommand = subcommands[addRemove.lower()]

        # Read from the server configs
        serverSettings = getServerJson(ctx.message.server.id)
        allowableIDs = serverSettings['SelfAssignableRoles']

        # Fliter if add or remove
        if calledSubcommand:
            try:
                allowableIDs.remove(roleToGive.id)
            except ValueError:
                await self.sparcli.say('This role isn\'t self-assignable.')
                return
        else:
            if roleToGive.id not in allowableIDs:
                allowableIDs.append(roleToGive.id)
            else:
                await self.sparcli.say('This role can already be self-assigned.')
                return

        # Plonk the settings back into the file storage
        serverSettings['SelfAssignableRoles'] = allowableIDs
        saveServerJson(ctx.message.server.id, serverSettings)

        # Print out to the user
        await self.sparcli.say('The role `{0.name}` with ID `{0.id}` {1} self-assigned.'.format(
            roleToGive, {False: 'can now be', True: 'can no longer be'}[calledSubcommand]))

    @commands.command(pass_context=True, aliases=['setprefix', 'prefixset'])
    async def prefix(self, ctx, prefix: str):
        '''Changes the command prefix for the server
        Usage :: prefix <New Preifx>'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel
        serverID = ctx.message.server.id

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

        # Load and save the command prefix
        serverSettings = getServerJson(serverID)
        serverSettings['CommandPrefix'] = prefix
        saveServerJson(serverID, serverSettings)

        # Print out to the user
        await self.sparcli.say('The command prefix for this server has been set to `{}`'.format(prefix))

    @commands.command(pass_context=True)
    async def setup(self, ctx):
        '''Gives you a reaction-based configuration dialogue
        Usage :: setup'''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel
        serverID = ctx.message.server.id

        # Get the permissions of the calling user
        userPerms = getPermissions(channel, 'admin', author)
        if type(userPerms) == str:
            await self.sparcli.say(userPerms)
            return

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
