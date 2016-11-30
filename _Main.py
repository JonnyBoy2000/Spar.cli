import discord
from discord.ext import commands
from sys import argv


initialExtentions = ['Cogs.Admin',
                     'Cogs.Misc',
                     'Cogs.OwnerOnly']


sparcli = commands.Bot(command_prefix=';', description='fuck')


@sparcli.command(pass_context=True)
async def ev(ctx, *, content: str):
    if ctx.message.author.id != '141231597155385344':
        await sparcli.say('You are not permitted to use this command.')
        return
    await sparcli.say(eval(content))


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
