import discord
from discord.ext import commands
from sys import argv
from Utils.Configs import *
from Utils.Updates import *
from Utils.Discord import messageToStarboard
from Utils.Extentions import q as initialExtentions


def getCommandPrefix(bot, message):
    # Returns the command prefix of the server
    # Get the settings for the server
    try:
        serverSettings = getServerJson(message.server.id)
        serverPrefix = serverSettings['CommandPrefix']
    except AttributeError:
        return ';'

    # Load the server prefix as defined
    return serverPrefix


sparcli = commands.Bot(
    command_prefix=getCommandPrefix, description='ApplePy 2.0, pretty much.', pm_help=True)


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


@sparcli.event
async def on_reaction_add(reaction, member):
    # See if it applies for the starboard
    if reaction.emoji != '⭐':
        return

    # See if the message is already in the starboard
    whereTo = serverEnables(reaction.message.server.id, 'Starboard')[1]
    channel = [i for i in reaction.message.server.channels if i.id == whereTo][0]

    toEdit = None
    async for message in sparcli.logs_from(channel, limit=10):
        if reaction.message.id in message.content:
            toEdit = message 

    # Create the embed if it does want to be sent
    starMes, starEmb = messageToStarboard(reaction.message)

    # Ping a message to the starboard channel
    await sendIfEnabled(sparcli, reaction.message.server, 'Starboard', overrideMessage=starMes, embed=starEmb, edit=toEdit)


@sparcli.event
async def on_reaction_remove(reaction, member):
    if reaction.emoji != '⭐':
        return

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
async def on_message(message):
    # Make the bot not respond to itself
    if message.author.bot:
        return

    # Process commands
    await sparcli.process_commands(message)


@sparcli.event
async def on_member_join(member):
    await sendIfEnabled(sparcli, member.server, 'Joins')


@sparcli.event
async def on_member_remove(member):
    await sendIfEnabled(sparcli, member.server, 'Leaves')


@sparcli.event
async def on_ready():
    print('-----')
    print('User :: {}'.format(sparcli.user))
    print('ID :: {}'.format(sparcli.user.id))
    print('-----')

    game = ';help'
    await sparcli.change_presence(game=discord.Game(name=game))

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


sparcli.run(argv[1])
