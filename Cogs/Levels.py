from math import log
from discord import Member
from discord.ext import commands 
from Cogs.Utils.LevelHandler import LevelHandler
from Cogs.Utils.Configs import getMoneyJson


class Levels:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.levelHandler = LevelHandler()

    @commands.command(pass_context=True)
    async def xp(self, ctx, user:Member=None):
        '''
        Shows you how much experience you have.
        '''

        if user == None:
            user = ctx.message.author

        serverXP = getMoneyJson(str(ctx.message.server.id))
        userXP = serverXP.get(str(user.id), 0)

        await self.sparcli.say('**{}** has **{}**XP on this server.'.format(user.display_name. userXP))

    @commands.command(pass_context=True)
    async def level(self, ctx, user:Member=None):
        '''
        Shows you how much experience you have.
        '''

        if user == None:
            user = ctx.message.author

        serverXP = getMoneyJson(str(ctx.message.server.id))
        userXP = serverXP.get(str(user.id), 0)
        userLevel = userXP/375

        await self.sparcli.say('**{}** is level **{:.2f}** on this server.'.format(user.display_name, userLevel))

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):

        leaderboard = {i: o for o, i in getMoneyJson(str(ctx.message.server.id)).items()}
        xpStains = [i for i in leaderboard.keys()]
        xpStains = sorted(xpStains, reverse=True)

        lads = []
        for i in range(10):
            z = xpStains[i]
            lads.append([leaderboard[z], z])

        ladz = []
        for i in lads:
            if ctx.message.server.get_member(i[0]):
                ladz.append([ctx.message.server.get_member(i[0]), i[1]])

        ret = ''
        for i in ladz:
            ret = ret + i[0].display_name + ' - **Lvl {:.2f}** \n'.format(i[1]/375)

        await self.sparcli.say(ret)


    async def on_message(self, message):
        '''
        Message handler for level and exp increases
        '''

        self.levelHandler.increment(message)


def setup(bot):
    bot.add_cog(Levels(bot))
