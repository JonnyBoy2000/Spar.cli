from discord.ext import commands
from discord import Colour
from discord.errors import NotFound as Forbidden
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions, getMentions, getNonTaggedMentions
from Utils.Configs import getServerJson


class RoleManagement:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(pass_context=True, aliases=['changecolour', 'changerolecolour', 'changerole', 'rolecolor', 'changecolor', 'changerolecolor'])
    async def rolecolour(self, ctx, rolecolour: str, *, rolename: str):
        '''Changes the colour of a specified role
        Usage :: rolecolour <HexValue> <RoleName>
              :: rolecolour <HexValue> <RolePing>'''

        # Make sure that the calling user is allowed to manage roles
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
            role = getNonTaggedMentions(ctx.message.server, rolename, 'role')
            if type(role) == str:
                await self.sparcli.say(role)
                return
        role = tempRole[0]

        # Change the role colour
        colour = Colour(int(rolecolour, 16))
        try:
            await self.sparcli.edit_role(ctx.message.server, role, colour=colour)
        except Forbidden:
            await self.sparcli.say('I was unable to edit the role.')
            return

        # Print to user
        await self.sparcli.say('The colour of the role `{0.name}` has been changed to value `{1.value}`.'.format(role, colour))

    @commands.command(pass_context=True)
    async def iam(self, ctx, *, whatRoleToAdd: str):
        '''If allowed, the bot will give you a mentioned role
        Usage :: iam <RoleName>
              :: iam <RolePing>'''

        # Try and see if the role was pinged
        roleToGive = getMentions(ctx.message, 1, 'role')
        if type(roleToGive) == str:

            # If wasn't pinged - see if it exists
            roleToGive = getNonTaggedMentions(
                ctx.message.server, whatRoleToAdd, 'role')
            if type(roleToGive) == str:

                # The user hates us
                await self.sparcli.say(roleToGive)
                return

        # Get the role from the list
        roleToGive = roleToGive[0]

        # See what you're allowed to self-assign
        serverSettings = getServerJson(ctx.message.server.id)
        allowableIDs = serverSettings['SelfAssignableRoles']

        # See if you can add that
        if roleToGive.id not in allowableIDs:
            await self.sparcli.say('You are not allowed to self-assign that role.')
            return

        # You can - add it to the user
        try:
            await self.sparcli.add_roles(ctx.message.author, roleToGive)
            await self.sparcli.say('The role `{0.name}` with ID `{0.id}` has been sucessfully added to you.'.format(roleToGive))
        except Forbidden:
            await self.sparcli.say('I was unable to add that role to you.')


def setup(bot):
    bot.add_cog(RoleManagement(bot))
