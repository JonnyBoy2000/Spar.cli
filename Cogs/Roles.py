from discord.ext import commands
from discord import Colour, Member, Permissions
from discord.errors import NotFound as Forbidden
from Cogs.Utils.Discord import getTextRoles
from Cogs.Utils.Configs import getServerJson
from Cogs.Utils.Misc import colourFixer
from Cogs.Utils.Permissions import permissionChecker, botPermission


class RoleManagement:

    def __init__(self, sparcli):
        self.sparcli = sparcli

    @commands.command(aliases=['changecolour', 'changerolecolour', 'changerole', 'rolecolor', 'changecolor', 'changerolecolor'])
    @permissionChecker(check='manage_roles')
    @botPermission(check='manage_roles')
    async def rolecolour(self, ctx, rolecolour: str, *, rolename: str):
        '''Changes the colour of a specified role
        Usage :: rolecolour <HexValue> <RoleName>
              :: rolecolour <HexValue> <RolePing>'''

        # Get the role colour
        rolecolour = colourFixer(rolecolour)

        # Get the role itself
        role = await getTextRoles(ctx)
        if role is 0:
            return

        # Change the role colour
        colour = Colour(int(rolecolour, 16))
        try:
            await role.edit(colour=colour)
        except Forbidden:
            await ctx.send('I was unable to edit the role.')
            return

        # Print to user
        await ctx.send('The colour of the role `{0.name}` has been changed to value `{1.value}`.'.format(role, colour))

    @commands.command()
    @botPermission(check='manage_roles')
    async def iam(self, ctx, *, whatRoleToAdd: str):
        '''If allowed, the bot will give you a mentioned role
        Usage :: iam <RoleName>
              :: iam <RolePing>
              :: iam list'''

        # Get a list if the user wanted to
        if whatRoleToAdd.lower() == 'list':
            await self.iamlist(ctx)
            return

        roleToGive = await getTextRoles(ctx)
        if roleToGive == 0:
            return

        # See what you're allowed to self-assign
        serverSettings = getServerJson(ctx.message.guild.id)
        allowableIDs = serverSettings['SelfAssignableRoles']

        # See if you can add that
        if roleToGive.id not in allowableIDs:
            await self.sparcli.say('You are not allowed to self-assign that role.')
            return

        # See if the user already has the role
        if roleToGive.id in [i.id for i in ctx.message.author.roles]:
            await ctx.send('You already have that role.')
            return

        # You can - add it to the user
        try:
            userRoles = ctx.message.author.roles + [roleToGive]
            await ctx.message.author.edit(roles=userRoles)
            await ctx.send('The role `{0.name}` with ID `{0.id}` has been sucessfully added to you.'.format(roleToGive))
        except Forbidden:
            await ctx.send('I was unable to add that role to you.')

    async def iamlist(self, ctx):
        '''Gives a list of roles that you can self-assign'''

        # Get all the stuff on the server that you can give to yourself
        serverSettings = getServerJson(ctx.message.guild.id)
        allowableIDs = serverSettings['SelfAssignableRoles']

        # Get their role names
        assignableRoles = [i.name for i in ctx.message.guild.roles if i.id in allowableIDs]

        # Print back out the user
        await ctx.send('The following roles are self-assignable: ```\n* {}```'.format('\n* '.join(assignableRoles)))

    @commands.command(pass_context=True, aliases=['makecolor'])
    @permissionChecker(check='manage_roles')
    @botPermission(check='manage_roles')
    async def makecolour(self, ctx, colour:str, user:Member=None):
        '''Creates a new role with a given colour, and assigns it to a user
        Usage :: makecolour <HexValue> <Mention>
              :: makecolour <HexValue>'''

        # Fix up some variables
        server = ctx.message.guild
        user = ctx.message.author if user == None else user

        # Fix the colour string
        colour = colourFixer(colour)
        colourObj = Colour(int(colour, 16))
        # permissions=Permissions(permissions=0)

        # Find the role
        tempRoleFinder = [i for i in server.roles if 'SPARCLI {}'.format(user.id) in i.name]
        if len(tempRoleFinder) > 0:
            role = tempRoleFinder[0]
            await role.edit(colour=colourObj)
            created = False
        else:
            role = await server.create_role(name='SPARCLI {}'.format(user.id), colour=colourObj)
            userRoles = [i for i in user.roles] + [role]
            await user.edit(roles=userRoles)
            created = True

        # Print out to user
        await ctx.send('This role has been successfully {}. \nYou may need to move the positions of other roles to make it work properly.'.format({True:'created',False:'edited'}))


def setup(bot):
    bot.add_cog(RoleManagement(bot))
