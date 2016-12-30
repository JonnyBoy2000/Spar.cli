import discord
from discord.ext import commands
from sys import argv
from Utils.Configs import *
from Utils.Updates import *
from Utils.Discord import messageToStarboard, makeEmbed
from Utils.Extentions import q as initialExtentions


def getCommandPrefix(bot, message):
    # Returns the command prefix of the server
    # Get the settings for the server
    try:
        serverSettings = getServerJson(message.server.id)
        serverPrefix = serverSettings['CommandPrefix']
    except AttributeError:
        return [';', '<@252880131540910080> ']

    # Load the server prefix as defined
    return [serverPrefix, serverPrefix + ' ', '<@252880131540910080> ']


sparcli = commands.Bot(
    command_prefix=getCommandPrefix, description='ApplePy 2.0, pretty much.', pm_help=True)



@sparcli.event 
async def on_command_error(error, ctx):
    # Check failure
    if isinstance(error, commands.errors.CheckFailure):
        await sparcli.send_message(ctx.message.channel, 'You are not permitted to use that command.')


@sparcli.event
async def on_server_join(server):
    # Runs when the bot joins a server
    # Create a config file for the server it joined
    z = getServerJson(server.id)
    z = fixJson(z)
    saveServerJson(server.id, z)

    # Say hi
    await sparcli.send_message(server, 'Hey! I\'ve just been added to this server. I\'m Spar.cli, and i\'ll try and do a good job c;')


@sparcli.event
async def on_message_edit(before, after):
    # Get the last message from the channel
    editedIDs = []
    async for message in sparcli.logs_from(after.channel, limit=3):
        editedIDs.append(message.id)

    # Check if the edited message and the last few messages are the same;
    # if they are you can process that as a command
    if after.id in editedIDs:
        await sparcli.process_commands(after)


async def starboard(reaction):
    # See if the message is already in the starboard
    whereTo = serverEnables(reaction.message.server.id, 'Starboard')[1]
    channel = [i for i in reaction.message.server.channels if i.id == whereTo][0]

    toEdit = None
    async for message in sparcli.logs_from(channel, limit=10):
        if reaction.message.id in message.content:
            toEdit = message

    # Create the embed if it does want to be sent
    starMes, starEmb = messageToStarboard(reaction.message)

    # All stars have been removed from the message - delete
    if starMes == False:
        await sparcli.delete_message(toEdit)
        return

    # Ping a message to the starboard channel
    await sendIfEnabled(sparcli, reaction.message.server, 'Starboard', overrideMessage=starMes, embed=starEmb, edit=toEdit)


@sparcli.event
async def on_reaction_add(reaction, member):
    # See if it applies for the starboard
    if reaction.emoji == '⭐':
        await starboard(reaction)


@sparcli.event
async def on_reaction_remove(reaction, member):
    # See if it applies for the starboard
    if reaction.emoji == '⭐':
        await starboard(reaction)


@sparcli.event
async def on_message(message):
    # Print out to console
    try:
        print(
            '{0.timestamp} :: {0.server.id} :: {0.author.id} :: {0.id}'.format(message))
    except AttributeError:
        print(
            '{0.timestamp} :: Private Message :: {0.author.id} :: {0.id}'.format(message))

    # Make the bot not respond to other bots
    if message.author.bot:
        return

    # Process commands
    await sparcli.process_commands(message)


@sparcli.event
async def on_member_join(member):
    await sendIfEnabled(sparcli, member.server, 'Joins', member=member)


@sparcli.event
async def on_member_remove(member):
    await sendIfEnabled(sparcli, member.server, 'Leaves', member=member)


@sparcli.event
async def on_channel_update(before, after):
    # Get the changes
    updateChecks = ['topic', 'name', 'bitrate']
    beforeChecksB = [getattr(before, i) for i in updateChecks]
    afterChecksB = [getattr(after, i) for i in updateChecks]

    # Fix up nonetypes
    beforeChecks = []
    afterChecks = []
    for i in beforeChecksB:
        if i == '': 
            i = 'None'
        beforeChecks.append(i)
    for i in afterChecksB:
        if i == '': 
            i = 'None'
        afterChecks.append(i)

    # Return if it's all the same
    if beforeChecks == afterChecks:
        return

    # See exactly what's updated
    changedThings = {}
    for i in range(0, len(updateChecks)):
        if beforeChecks[i] != afterChecks[i]:
            changedThings[updateChecks[i].title()] = '`{}` changed into `{}`'.format(beforeChecks[i], afterChecks[i])

    # Format everything into a nice embed
    em = makeEmbed(name='Channel Update :: {}!'.format(after.name), values=changedThings, user=sparcli.user)
    await sendIfEnabled(sparcli, after, 'Channelupdates', embed=em, overrideChannel=after)


@sparcli.event
async def on_ready():
    print('-----')
    print('User :: {}'.format(sparcli.user))
    print('ID :: {}'.format(sparcli.user.id))
    print('-----')

    # Load the extentions
    for extension in initialExtentions:
        # This is necessary because I'm bad at code
        try:
            sparcli.load_extension(extension)

        # Print out any errors
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    # Load up any changes that would have been made to the configs
    for server in sparcli.servers:
        z = getServerJson(server.id)
        z = fixJson(z)
        saveServerJson(server.id, z)

    z = getServerJson('Globals')
    z = fixJson(z)
    saveServerJson('Globals', z)

    game = '@Spar.cli help'
    await sparcli.change_presence(game=discord.Game(name=game))


sparcli.run(argv[1])
