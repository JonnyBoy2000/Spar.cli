from discord.ext import commands
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Configs import getServerJson, saveServerJson


class Tags:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True)
    async def tag(self, ctx, *, subcom:str=None):
        # See if you're trying to call a subcommand or error
        if subcom == None:
            # Return if sayig nothing
            return

        # Work through the functions if trying to call one
        elif subcom.split(' ',1)[0] in ['add', 'delete', 'del', 'globaladd', 'globaldelete', 'globaldel']:
            
            # Create a dictionary of functions to call for different commands
            functionDict = {'add':self.tagAdd}

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
        globalTags = getServerJson('Default')['Tags']
        localTags = getServerJson(server.id)['Tags']

        # See if it's a local tag
        try:
            tagOutput = localTags[subcom]
        except KeyError:
            pass

        # See if it's a global tag - 
        # by putting second it takes priority
        try:
            tagOutput = globalTags[subcom]
        except KeyError:
            pass

        # Output to user
        await self.sparcli.say(tagOutput)


    async def tagAdd(self, ctx, tagName):
        # Deal with idiots - trying to make tag without name
        if tagName == None:
            await self.sparcli.say('What is the tag name you want to add?')
            nameMessage = await self.sparcli.wait_for_message(author=ctx.message.author)
            tagName = nameMessage.content

        # Tell them thhat you're making tag and being nice
        await self.sparcli.say('Creating tag with name `{}`. What is the indended content?'.format(name))
        contentMessage = await self.sparcli.wait_for_message(author=ctx.message.author)
        content = contentMessage.content

        # Save it into the server configs
        settings = getServerJson(ctx.message.server.id)
        settings['Tags'][tagName] = content
        saveServerJson(ctx.message.server.id, settings)

        # Respond to the user
        await self.sparcli.say('This tag has been created.')


def setup(bot):
    bot.add_cog(Tags(bot))
