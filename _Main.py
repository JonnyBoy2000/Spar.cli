import discord
from discord.ext import commands
from sys import argv


sparcli = command.Bot(command_prefix=';', description='fuck')


@sparcli.command(pass_context=True)
async def ev(ctx, *, content: str):
    if ctx.message.author.id != '141231597155385344':
        await sparcli.say('You are not permitted to use this command.')
        return
    await sparcli.say(eval(content))


sparcli.run(argv[0])
