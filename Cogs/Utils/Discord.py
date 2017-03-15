from discord import Embed
from discord.ext import commands
from time import strftime


def checkPerm(**check):
    def predicate(ctx):
        return getPermissions(errReturn=bool, ctx=ctx, check=check['check'])
    return commands.check(predicate)


def getPermissions(channel=None, permissionCheck=None, firstPerson=None, secondPerson=None, *, errReturn=str, **kwargs):
    '''Gives the permissions in a channel for a user, 
    and returns the bool of whether the user has that permission.
    This will also give whether a certain role is above that of a second person's'''

    # Loads from kwargs
    if firstPerson == None:
        channel = kwargs['ctx'].message.channel 
        firstPerson = kwargs['ctx'].message.author 
        permissionCheck = kwargs['check']
        try: 
            secondPerson = kwargs['person']
        except: 
            secondPerson = None

    # Check if you're looking for the owner
    ownerIDs = ['141231597155385344', '155459369545367552']
    try:
        ownerIDs = ownerIDs + kwargs['owners']
    except KeyError:
        pass

    # Run the actual owner checks
    if permissionCheck == 'is_owner':
        isOwner = firstPerson.id in ownerIDs
        if errReturn == bool:
            return isOwner
        return isOwner if isOwner else 'You need to be an owner to use this command.'
    if firstPerson.id in ownerIDs:
        return True 

    # Otherwise, just get the permissions
    perms = channel.permissions_for(firstPerson)
    
    # Let admins do everything
    if perms.administrator:
        return True

    # Get the intended permission 
    canGo = getattr(perms, permissionCheck)
    if secondPerson == None:
        if errReturn == bool:
            return canGo
        return canGo if canGo else 'You do not have permission to use this command.'

    # See if you can run the role on the selected user
    isAbove = firstPerson.top_role.position > secondPerson.top_role.position
    if errReturn == bool:
        return isAbove
    return isAbove if isAbove else 'You do not have permission to use this command against this user.'


async def getTextRoles(ctx):
    '''Gets non-tagged and tagged roles from a message's ctx'''

    # Try and see if the role was pinged
    roleToGive = ctx.message.role_mentions
    if roleToGive == []:

        # Find it from the names of the roles on the server
        serverRoleObjects = ctx.message.guild.roles
        serverRoleNames = [i.name for i in serverRoleObjects]
        results = []

        for i, n in enumerate(serverRoleNames):
            # i is index, n is name
            if whatToChange.lower() in n.lower():
                results.append(i)

        # Check if there was more than one relevant result
        if len(results) == 0:
            await self.sparcli.say('There were no results for roles with that name on this server.')
            return 0
        elif len(results) > 1:
            await self.sparcli.say('There were too many results for roles with that name on this server.')
            return 0
        else:
            roleToGive = [serverRoleObjects[results[0]]]

    return roleToGive[0]


def makeEmbed(**kwargs):
    '''
    Creates an embed messasge with specified inputs.

    Parameters
    ----------
        author
        author_url
        author_icon
        user
        colour
        values
        inline
        thumbnail
        image
        footer
        footer_icon
    '''

    # Get the attributes from the user
    empty = Embed.Empty
    if True:

        # Get the author/title information
        author = kwargs.get('author', None)
        author_url = kwargs.get('author_url', empty)
        author_icon = kwargs.get('author_icon', empty)
        user = kwargs.get('user', None)

        # Get the colour
        colour = kwargs.get('colour', 0)

        # Get the values
        values = kwargs.get('values', {})
        inline = kwargs.get('inline', True)

        # Images
        thumbnail = kwargs.get('thumbnail', False)
        image = kwargs.get('image', False)

        # Footer
        footer = kwargs.get('footer', empty)
        footer_icon = kwargs.get('footer_icon', empty)

    # Correct the icon and author with the member, if necessary
    if user == None:
        author = user.display_name
        author_icon = user.avatar_url
        try:
            colour = user.colour.value 
        except AttributeError:
            pass

    # Create an embed object with the specified colour
    embedObj = Embed(colour=colour)

    # Set the normal attributes
    embedObj.set_author(name=author, url=author_url, icon_url=author_icon)
    embedObj.set_footer(text=footer, icon_url=footer_icon)
    
    # Set the attributes that have no default
    if image: embedObj.set_icon(url=image)
    if thumbnail: embedObj.set_thumbnail(url=thumbnail)

    # Set the fields
    for i, o in fields.items():
        p = inline
        if type(o) in [tuple, list]:
            p = o[1]
            o = o[0]
        embedObj.add_field(name=i, value=o, inline=p)

    # Return to user
    return embedObj


def messageToStarboard(message):
    '''Created an embeddable message as a quote for use of the starboard event reference'''

    # Get the amount of stars on the message
    starAmount = [i.count for i in message.reactions if i.emoji == '⭐']
    try:
        starAmount = starAmount[0]
    except IndexError:
        return False, False

    # Thus, make the text from the message
    starboardText = '⭐ **{0}** from `{1.id}` in {2.mention}'.format(
        starAmount, message, message.channel)

    # From here, make the embed
    embedObj = Embed(colour=0xFFA930)
    user = message.author
    embedIcon = user.avatar_url if user.avatar_url != None else user.default_avatar_url
    embedObj.set_author(name=str(user), icon_url=embedIcon)

    # Get timestamp
    date = message.timestamp
    formtattedDate = date.strftime('%c')
    con = message.clean_content if message.clean_content != '' else 'None'

    atch = message.attachments
    if len(atch) > 0:
        if atch[0]['url'][-4:] in ['.png','.jpg']:
            embedObj.set_image(url=atch[0]['url'])

    # Add content
    if con != 'None':
        embedObj.add_field(name='Message :: ', value=con)
    embedObj.set_footer(text=formtattedDate)

    # Return to user
    return starboardText, embedObj

def getServerDefaultChannel(server):
    '''
    Gets the default channel of a server in order to use `.send()` etc on
    '''

    return [i for i in server.channels if i.id == server.id][0]
