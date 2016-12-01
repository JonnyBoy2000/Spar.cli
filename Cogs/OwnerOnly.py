from discord.ext import commands
from discord import Game
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions


class OwnerOnly:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True, hidden=True, aliases=['playing'])
    async def game(self, ctx, *, game: str=None):
        '''Change what the bot is playing
        Usage :: game <Content>'''

        # Check if the owner is calling the command
        permReturn = getPermissions(ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Change the game
        await self.sparcli.change_presence(game=Game(name=game))
        await self.sparcli.say('Game changed to **{}**.'.format(game))

    @commands.command(pass_context=True)
    async def ev(self, ctx, *, content: str):
        # Check if the owner is calling the command
        permReturn = getPermissions(ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Eval and print the answer
        await self.sparcli.say(eval(content))


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
