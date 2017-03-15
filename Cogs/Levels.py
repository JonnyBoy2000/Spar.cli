from discord.ext import commands 
from Cogs.Utils.LevelHandler import LevelHandler


class Levels:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.levelHandler = LevelHandler()

    async def on_message(self, message):
        '''
        Message handler for level and exp increases
        '''

        if message.guild == None: return
        self.levelHandler.increment(message)


def setup(bot):
    bot.add_cog(Levels(bot))
