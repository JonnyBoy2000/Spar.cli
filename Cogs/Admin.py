from discord.ext import commands


class Admin:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True)
    async def ban(self, ctx):
        '''ban <Mention>
        Bans a user from the server.'''

        # Get the tagged users from the message
        taggedUser = ctx.message.mentions

        # If nobody was tagged
        if ctx.message.mentions == []:
            await self.sparcli.say('You need to tag a user to ban.')
            return

        # If more than one person is tagged
        elif len(ctx.message.mentions) > 1:
            await self.sparcli.say('You can only tag one user to ban.')
            return

        # Get the permissions of the calling user in the channel
        permList = ctx.message.channel.permissions_for(ctx.message.author)
        if permList.ban_members == False:
            await self.sparcli.say('You do not have permission to ban members.')
            return

        # Get the top role of the two users, make sure the user would be able
        # to ban
        topRoles = [ctx.message.author.top_role.position,
                    taggedUser[0].top_role.position]
        if topRoles[0] <= topRoles[1]:
            await self.sparcli.say('Your role is not high enough to ban that user.')
            return

        # Try and ban the user
        try:
            await self.sparcli.ban(taggedUser[0])
        except:
            await self.sparcli.say('I was unable to ban that user.')
            return

        # Todo :: make this print out in a config-determined channel
        await self.sparcli.say('**{}** has been banned.'.format(taggedUser[0]))


def setup(bot):
    bot.add_cog(Admin(bot))
