from discord.ext import commands 
from discord import Colour
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, getMentions


class RoleManagement:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True, aliases=['changecolour','changerolecolour','changerole'])
    async def rolecolour(self, ctx, rolecolour:str, *, rolename:str):
        '''Changes the colour of a specified role
        Usage :: rolecolour <HexValue> <RoleName>
                 rolecolour <HexValue> <RolePing>'''

        # Make sure that the calling user is allowed to manage messages
        permReturn = getPermissions(
            ctx.message.channel, 'manage_roles', ctx.message.author)

        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Get the role colour
        if len(rolecolour) == 7:
            rolecolour = rolecolour.replace('#', '')
        if len(rolecolour) != 6:
            await self.sparcli.say('Give the colour of the role to change in the form of a hex code.')

        # Get the role itself
        role = getMentions(ctx.message, 1, 'role')
        if role == 'You need to tag a role in your message.':
            tempRole = [i for i in ctx.message.server.roles if rolename.lower() in i.name.lower()]
            if len(tempRole) == 0:
                await self.sparcli.say(role)
                return
            if len(tempRole) > 1:
                await self.spacli.say('There are multiple roles by this name - try tagging one.')
                return
            role = tempRole[0]

        # Change the role colour
        colour = Colour(int(rolecolour, 16))
        await self.sparcli.edit_role(ctx.message.server, role, colour=colour)

        # Print to user
        await self.sparcli.say('The colour of the role `{0.name}` has been changed to value `{1.value}`.'.format(role, colour))


def setup(bot):
    bot.add_cog(RoleManagement(bot))
