from discord.ext import commands
from Cogs.Utils.Configs import getServerJson


class AutoModerator:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    async def on_member_update(self, before, after):
        '''
        Check for any forced nicknames
        '''

        serverSettings = getServerJson(after.server.id)
        automodSettings = serverSettings['AutoModerator']
        forcedNicknames = automodSettings['ForcedNicknames']

        # `forcedNicknames` is a {userID: nickname} pair
        try:
            toChangeTo = forcedNicknames[str(after.id)]
            if after.nick == toChangeTo:
                return
        except KeyError:
            return

        # `toChangeTo` is the nickname to change to
        await self.sparcli.change_nickname(after, toChangeTo)


def setup(bot):
    bot.add_cog(AutoModerator(bot))
