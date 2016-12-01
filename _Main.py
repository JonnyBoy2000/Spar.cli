import discord
from discord.ext import commands
from Utils.Configs import *


initialExtentions = ['Cogs.Admin',
                     'Cogs.Misc',
                     'Cogs.OwnerOnly',
                     'Cogs.Internet',
                     'Cogs.Tags',
                     'Cogs.Random',
                     'Cogs.Roles']


sparcli = commands.Bot(
    command_prefix=['👌', ';'], description='ApplePy 2.0, pretty much.', pm_help=True)


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
    async for message in sparcli.logs_from(after.channel, limit=1):
        pass

    # Check if the edited message and the last message are the same;
    # if they are you can process that as a command
    if message.id == after.id:
        await sparcli.process_commands(after)


@sparcli.event
async def on_message(message):
    # Make the bot not respond to itself
    if message.author.bot:
        return

    # Process commands
    await sparcli.process_commands(message)


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


sparcli.run(getArguments()['--token'])
