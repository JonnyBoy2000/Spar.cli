import discord
from discord.ext import commands
from sys import argv
from Cogs.Utils.Configs import *
from Cogs.Utils.Updates import *
from Cogs.Utils.Discord import messageToStarboard, makeEmbed
from Cogs.Utils.Extentions import q as initialExtentions
from Cogs.Utils.Exceptions import *


def getCommandPrefix(bot, message):
    # Returns the command prefix of the server
    # Get the settings for the server
    try:
        serverSettings = getServerJson(message.server.id)
        serverPrefix = serverSettings['CommandPrefix']
    except AttributeError:
        return [';', '<@252880131540910080> ']

    # Load the server prefix as defined
    return [serverPrefix + ' ', serverPrefix, '<@252880131540910080> ']


sparcli = commands.Bot(
    command_prefix=getCommandPrefix, description='ApplePy 2.0, pretty much.', pm_help=True, formatter=commands.formatter.HelpFormatter(show_check_failure=True))



@sparcli.event 
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    server = ctx.message.server

    if isinstance(error, BotPermissionsTooLow):
        # This should run if the bot doesn't have permissions to do a thing to a user
        await sparcli.send_message(channel, 'That user is too high ranked for me to perform that action on them.')
        
    elif isinstance(error, MemberPermissionsTooLow):
        # This should run if the member calling a command doens't have permission to call it
        await sparcli.send_message(channel, 'That user is too high ranked for you to run that command on them.')
        
    elif isinstance(error, MemberMissingPermissions):
        # This should be run should the member calling the command not be able to run it
        await sparcli.send_message(channel, 'You are missing the permissions required to run that command.')

    elif isinstance(error, BotMissingPermissions):
        # This should be run if the bot can't run what it needs to
        await sparcli.send_message(channel, 'I\'m missing the permissions required to run this command.')

    elif isinstance(error, DoesntWorkInPrivate):
        # This is to be run if the command is sent in PM
        await sparcli.send_message(channel, 'This command does not work in PMs.')
        
    if isinstance(error, commands.errors.CheckFailure):
        # This should never really occur
        # This is if the command check fails
        await sparcli.send_message(channel, 'Command check failed. Unknown error; please mention `Caleb#2831`.')
        
    else:
        # Who knows what happened? Not me. Raise the error again, and print to console
        print('Error on message :: Server{0.server.id} Author{0.author.id} Message{0.id} Content'.format(ctx.message), end='')
        try: print(ctx.message.content + '\n')
        except: print('Could not print.' + '\n')
        raise(error)


@sparcli.event
async def on_server_join(server):
    # Runs when the bot joins a server
    # Create a config file for the server it joined
    z = getServerJson(server.id)
    z = fixJson(z)
    saveServerJson(server.id, z)

    # Say hi
    await sparcli.send_message(server, 'Hey! I\'ve just been added to this server. I\'m Spar.cli, and I\'ll try and do a good job c;')


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
    
    # See if it's a PM
    if message.server != None:
        f = '{0.timestamp} :: {0.server.id} :: {0.author.id} :: {0.id}'
    else:
        f = '{0.timestamp} ::  Private Message   :: {0.author.id} :: {0.id}'

    # Print out to console
    print(f.format(message))

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
    await updateSender(before, after, ['topic', 'name', 'bitrate'], 'Channel Update :: {}!', 'Channelupdates', True)


@sparcli.event 
async def on_server_update(before, after):
    await updateSender(before, after, ['name', 'icon'], 'Server update!', 'Serverupdates')


async def updateSender(before, after, updateChecks, embedName, sendEnable, override=False):
    # Get the changes    
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
    em = makeEmbed(name=embedName.format(after.name), values=changedThings, user=sparcli.user)
    await sendIfEnabled(sparcli, after, sendEnable, embed=em, overrideChannel={True:after,False:None}[override])


@sparcli.event
async def on_ready():
    print('-----')
    print('User :: {}'.format(sparcli.user))
    print('ID :: {}'.format(sparcli.user.id))
    print('-----')

    # Load the extentions
    for extension in initialExtentions:
        # This is necessary because I'm bad at code lol
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

