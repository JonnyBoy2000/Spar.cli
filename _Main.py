import discord
from discord.ext import commands
from sys import argv


initialExtentions = ['Cogs.Admin',
                     'Cogs.Misc',
                     'Cogs.OwnerOnly',
                     'Cogs.Internet']


sparcli = commands.Bot(command_prefix=['👌', ';'], description='ApplePy 2.0, pretty much.')


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


args = {'--token': None}
del argv[0]  # Delete the name from the cli


# Format the args into a dictionary
for i in range(0, len(argv), 2):
    args[argv[i]] = argv[i+1]


sparcli.run(args['--token'])
