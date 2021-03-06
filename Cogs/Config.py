from discord.ext import commands
from discord import Channel
from Cogs.Utils.Messages import getTextRoles
from Cogs.Utils.Configs import getServerJson, saveServerJson
from Cogs.Utils.GuiConfig import addEmojiList, updateFromEmoji, updateFromMessage
from Cogs.Utils.Permissions import permissionChecker


class Config:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True, name='prefix', aliases=['setprefix', 'prefixset'])
    @permissionChecker(check='administrator')
    async def prefixCommand(self, ctx, *, prefix: str):
        '''
        Changes the command prefix for the server.
        '''

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
        '''
        Gives you a reaction-based configuration dialogue.
        '''

        # Set up some variables to keep line length short
        author = ctx.message.author
        channel = ctx.message.channel
        serverID = ctx.message.server.id
        
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
        await self.sparcli.say('Alright, everything is updated!')

        # Save it all to file
        saveServerJson(serverID, serverSettings)


def setup(bot):
    bot.add_cog(Config(bot))
