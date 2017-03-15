from discord.ext import commands
from Cogs.Utils.Configs import getServerJson, saveServerJson
from Cogs.Utils.Discord import getPermissions
from Cogs.Utils.Permissions import permissionChecker


'''
Todo: Rewrite this entire class
On completion: I can remove the getPermissions function
'''


class Tags:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True, aliases=['t'])
    async def tag(self, ctx, *, subcom: str=None):
        '''Defines server-specific tags for repeating
        Usage :: tag add
              :: tag del'''

        await self.runTag(ctx, subcom, False)

    @commands.command(pass_context=True, aliases=['et'], hidden=True)
    @permissionChecker(check='is_owner')
    async def etag(self, ctx, *, subcom: str=None):
        '''Defines server-specific tags for evaluating Python expressions
        Usage :: etag add
              :: etag del'''

        await self.runTag(ctx, subcom, True)

    async def runTag(self, ctx, subcom, runWithExec):
        # See if you're trying to call a subcommand or error
        if subcom == None:
            # Return if sayig nothing
            return

        # Work through the functions if trying to call one
        elif subcom.split(' ', 1)[0] in ['add', 'delete', 'del', 'globaladd', 'globaldelete', 'globaldel', 'list']:

            # Create a dictionary of functions to call for different commands
            functionDict = {'add': self.tagAdd,
                            'delete': self.tagDelete,
                            'del': self.tagDelete,
                            'globaladd': self.tagGlobalAdd,
                            'globaldel': self.tagGlobalDelete,
                            'globaldelete': self.tagGlobalDelete,
                            'list': self.tagInfo
                            }

            # Get the tag name
            try:
                content = subcom.split(' ', 1)[1]
            except IndexError:
                content = None

            # Call the function that actually does stuff.
            await functionDict[subcom.split(' ', 1)[0]](ctx, content, ctx.message.guild.id, runWithExec)
            return

        # This is run to actually print a tag
        server = ctx.message.guild

        # Get both the global and local tags
        globalTags = getServerJson(
            'Globals')[{False: 'Tags', True: 'Etags'}[runWithExec]]
        localTags = getServerJson(
            server.id)[{False: 'Tags', True: 'Etags'}[runWithExec]]

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
            pass

        # Executes output if it's an etag
        if tagOutput != None and runWithExec == True:
            try:
                tagOutput = eval(tagOutput)
            except Exception as e:
                tagOutput = repr(e)

        # Output to user
        if tagOutput != None:
            await ctx.send(tagOutput)
        else:
            await ctx.send('That tag does not exist.')

    async def tagInfo(self, ctx, tagName, completelyUnused, runWithExec):
        # Tagname isn't used, but it's kinda necessary because of how I'm calling it
        # Get the local and global tags
        server = ctx.message.guild
        globalTags = getServerJson(
            'Globals')[{False: 'Tags', True: 'Etags'}[runWithExec]]
        localTags = getServerJson(
            server.id)[{False: 'Tags', True: 'Etags'}[runWithExec]]

        # Plonk them into a new list
        locald = []
        for i in localTags:
            if i in globalTags:
                pass
            else:
                locald.append('{} :: {}'.format(i, localTags[i]))
        globald = []
        for i in globalTags:
            globald.append('{} :: {}'.format(i, globalTags[i]))

        # Format them into a string
        formatLocal = 'Local Tags :: \n```\n{}```'.format('\n'.join(locald))
        formatGlobal = 'Global Tags :: \n```\n{}```'.format('\n'.join(globald))
        formatted = '{}\n{}'.format(formatLocal, formatGlobal)

        # PM it to the user
        await ctx.send('You have been private messaged a list of all of the commands.')
        await ctx.author.send(formatted)

    async def tagGlobalAdd(self, ctx, tagName, unusedServerID, runWithExec):
        permThing = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permThing) == str:
            await self.sparcli.say(permThing)
            return
        await self.tagAdd(ctx, tagName, 'Globals', runWithExec)

    async def tagGlobalDelete(self, ctx, tagName, unusedServerID, runWithExec):
        permThing = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permThing) == str:
            await ctx.send(permThing)
            return
        await self.tagDelete(ctx, tagName, 'Globals', runWithExec)

    async def tagDelete(self, ctx, tagName, serverID=None, runWithExec=False):
        # Deal with idiots - trying to make tag without name
        if tagName == None:
            await ctx.send('What is the tag name you want to delete?')
            check = lambda mes: mes.author == ctx.message.author
            nameMessage = await self.sparcli.wait_for('message', check=check)
            tagName = nameMessage.content

        # Get the serverID
        serverID = ctx.message.guild.id if serverID == None else serverID

        # Save it into the server configs
        settings = getServerJson(serverID)
        try:
            del settings[{False: 'Tags', True: 'Etags'}[runWithExec]][tagName]
        except KeyError:
            await ctx.send('This tag does not exist.')
            return

        saveServerJson(serverID, settings)

        # Respond to the user
        await ctx.send('This tag has been deleted.')

    async def tagAdd(self, ctx, tagName, serverID=None, runWithExec=False):

        settings = getServerJson(serverID)
        zz = settings[{False: 'Tags', True: 'Etags'}[runWithExec]]
        if len(zz) > 30:
            await ctx.send('There are already 30 tags on this server. You can\'t add any more.')
            return

        # Deal with idiots - trying to make tag without name
        if tagName == None:
            await ctx.send('What is the tag name you want to add?')
            check = lambda mes: mes.author == ctx.message.author
            nameMessage = await self.sparcli.wait_for('message', check=check)
            tagName = nameMessage.content

            # If someone tries to tag a command
            if tagName[0] in [',', '👌']:
                return

        # Tell them thhat you're making tag and being nice
        await ctx.send('Creating tag with name `{}`. What is the indended content?'.format(tagName))
        check = lambda mes: mes.author == ctx.message.author
        contentMessage = await self.sparcli.wait_for('message', check=check)
        content = contentMessage.content if contentMessage.content != '' else contentMessage.attachments[0]['url']

        # Get the serverID
        serverID = ctx.message.guild.id if serverID == None else serverID

        # Save it into the server configs
        settings = getServerJson(serverID)
        settings[{False: 'Tags', True: 'Etags'}[runWithExec]][tagName] = content
        saveServerJson(serverID, settings)

        # Respond to the user
        await ctx.send('This tag has been created.')


def setup(bot):
    bot.add_cog(Tags(bot))
