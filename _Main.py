import discord
from discord.ext import commands
from sys import argv

sparcli = command.Bot(command_prefix=';', description='fuck')


@sparcli.command(pass_context=True)
async def ban(ctx):
    taggedUser = ctx.message.mentions
    if ctx.message.mentions == []:
        await sparcli.say('You need to tag a user to ban.')
        return
    elif len(ctx.message.mentions) > 1:
        await sparcli.say('You can only tag one user to ban.')
        return

    permList = ctx.message.channel.permissions_for(ctx.message.author)
    if permList.ban_members == False:
        await sparcli.say('You do not have permission to ban members.')
        return

    topRoles = [ctx.message.author.top_role.position,
                taggedUser.top_role.permission]
    if topRoles[0] <= topRoles[1]:
        await sparcli.say('Your role is not high enough to ban that user.')
        return

    try:
        await sparcli.ban(taggedUser)
    except:
        await sparcli.say('I was unable to ban that user.')
        return
    await sparcli.say('**{}** has been banned.'.format(taggedUser))


@sparcli.command()
async def invite():
    await sparcli.say('https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=sparcli&permissions=0')


@sparcli.command()
async def git():
    await sparcli.say('https://github.com/4Kaylum/Spar.cli/')


@sparcli.command()
async def echo(*, content: str):
    await sparcli.say(content)


@sparcli.command(pass_context=True)
async def ev(ctx, *, content: str):
    if ctx.message.author.id != '141231597155385344':
        await sparcli.say('You are not permitted to use this command.')
        return
    await sparcli.say(eval(content))


sparcli.run(argv[0])
