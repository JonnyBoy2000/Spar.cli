from time import strftime
from re import finditer
from discord import Embed
from discord.ext import commands


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


async def getTextRoles(ctx, hitString, speak=False, sparcli=None):
    '''Gets non-tagged and tagged roles from a message's ctx'''

    serverRoles = ctx.message.server.roles 
    hits = [i for i in serverRoles if hitString.lower() in i.name.lower()]
    if len(hits) == 1:
        return hits[0]

    if speak:
        await sparcli.send_message(ctx.message.channel, 'There were `{}` hits for that string within this server\'s roles.'.format(len(hits)))
    return len(hits)


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
    Empty = Embed.Empty
    if True:

        # Get the author/title information
        author = kwargs.get('author', Empty)
        author_url = kwargs.get('author_url', Empty)
        author_icon = kwargs.get('author_icon', Empty)
        user = kwargs.get('user', None)

        # Get the colour
        colour = kwargs.get('colour', 0)

        # Get the values
        fields = kwargs.get('fields', {})
        inline = kwargs.get('inline', True)
        description = kwargs.get('description', Empty)

        # Images
        thumbnail = kwargs.get('thumbnail', False)
        image = kwargs.get('image', False)

        # Footer
        footer = kwargs.get('footer', Empty)
        footer_icon = kwargs.get('footer_icon', Empty)

    # Correct the icon and author with the member, if necessary
    if user != None:
        author = user.display_name if author == Empty else author
        author_icon = user.avatar_url if author_icon == Empty else author_icon
        try:
            colour = user.colour.value 
        except AttributeError:
            pass

    # Create an embed object with the specified colour
    embedObj = Embed(colour=colour)

    # Set the normal attributes
    if author != Empty:
        embedObj.set_author(name=author, url=author_url, icon_url=author_icon)
    embedObj.set_footer(text=footer, icon_url=footer_icon)
    embedObj.description = description
    
    # Set the attributes that have no default
    if image: embedObj.set_image(url=image)
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


def messageToEmbed(message):

    # Get some default values that'll be in the embed
    author = message.author 
    description = message.content
    image = False

    # Check to see if any images were added
    regexMatch = r'.+(.png)|.+(.jpg)|.+(.jpeg)|.+(.gif)'
    if len(message.attachments) > 0:
        attachment = message.attachments[0]
        matchList = [i for i in finditer(regexMatch, attachment['filename'])]
        if len(matchList) > 0:
            image = attachment['url']

    # Get the time the message was created
    createdTime = '.'.join(str(message.timestamp).split('.')[:-1])

    # Make and return the embed
    return makeEmbed(user=author, description=description, image=image, footer=createdTime)
