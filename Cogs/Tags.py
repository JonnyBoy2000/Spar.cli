from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Configs import getServerJson, saveServerJson
from Utils.Discord import getPermissions


class Tags:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True)
    async def tag(self, ctx, *, subcom: str=None):
        '''Defines server-specific tags for repeating on the server
        Usage :: tag add
              :: tag del'''
        # See if you're trying to call a subcommand or error
        if subcom == None:
            # Return if sayig nothing
            return

        # Work through the functions if trying to call one
        elif subcom.split(' ', 1)[0] in ['add', 'delete', 'del', 'globaladd', 'globaldelete', 'globaldel']:

            # Create a dictionary of functions to call for different commands
            functionDict = {'add': self.tagAdd,
                            'delete': self.tagDelete,
                            'del': self.tagDelete,
                            'globaladd': self.tagGlobalAdd,
                            'globaldel': self.tagGlobalDelete,
                            'globaldelete': self.tagGlobalDelete
                            }

            # Get the tag name
            try:
                content = subcom.split(' ', 1)[1]
            except IndexError:
                content = None

            # Call the function that actually does stuff.
            await functionDict[subcom.split(' ', 1)[0]](ctx, content)
            return

        # This is run to actually print a tag
        server = ctx.message.server

        # Get both the global and local tags
        globalTags = getServerJson('Globals')['Tags']
        localTags = getServerJson(server.id)['Tags']

        # See if it's a local tag
        try:
            tagOutput = localTags[subcom]
        except KeyError:
            tagOutput = None

        # See if it's a global tag -
        # by putting second it takes priority
        try:
            tagOutput = globalTags[subcom]
        except KeyError:
            tagOutput = None if tagOutput == None else tagOutput

        # Output to user
        if tagOutput != None:
            await self.sparcli.say(tagOutput)
        else:
            await self.sparcli.say('That tag does not exist.')

    async def tagGlobalAdd(self, ctx, tagName):
        permThing = getPermissions(ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permThing) == str:
            await self.sparcli.say(permThing)
            return
        await self.tagAdd(ctx, tagName, 'Globals')

    async def tagGlobalDelete(self, ctx, tagName):
        permThing = getPermissions(ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permThing) == str:
            await self.sparcli.say(permThing)
            return
        await self.tagDelete(ctx, tagName, 'Globals')

    async def tagDelete(self, ctx, tagName, serverID=None):
        # Deal with idiots - trying to make tag without name
        if tagName == None:
            await self.sparcli.say('What is the tag name you want to delete?')
            nameMessage = await self.sparcli.wait_for_message(author=ctx.message.author)
            tagName = nameMessage.content

        # Get the serverID
        serverID = ctx.message.server.id if serverID == None else serverID

        # Save it into the server configs
        settings = getServerJson(serverID)
        try:
            del settings['Tags'][tagName]
        except KeyError:
            await self.sparcli.say('This tag does not exist.')
            return

        saveServerJson(serverID, settings)

        # Respond to the user
        await self.sparcli.say('This tag has been deleted.')

    async def tagAdd(self, ctx, tagName, serverID=None):
        # Deal with idiots - trying to make tag without name
        if tagName == None:
            await self.sparcli.say('What is the tag name you want to add?')
            nameMessage = await self.sparcli.wait_for_message(author=ctx.message.author)
            tagName = nameMessage.content

        # Tell them thhat you're making tag and being nice
        await self.sparcli.say('Creating tag with name `{}`. What is the indended content?'.format(tagName))
        contentMessage = await self.sparcli.wait_for_message(author=ctx.message.author)
        content = contentMessage.content if contentMessage.content != '' else contentMessage.attachments[0]['url']

        # Get the serverID
        serverID = ctx.message.server.id if serverID == None else serverID

        # Save it into the server configs
        settings = getServerJson(serverID)
        settings['Tags'][tagName] = content
        saveServerJson(serverID, settings)

        # Respond to the user
        await self.sparcli.say('This tag has been created.')


def setup(bot):
    bot.add_cog(Tags(bot))
