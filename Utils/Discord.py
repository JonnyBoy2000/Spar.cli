from discord import Embed
from time import strftime


def getPermissions(channel, permissionCheck, firstPerson, secondPerson=None):
    '''Gives the permissions in a channel for a user, 
    and returns the bool of whether the user has that permission.
    This will also give whether a certain role is above that of a second person's'''

    # Get the first user's permissions and top role
    firstPermissions = channel.permissions_for(firstPerson)
    firstTop = max([i.position for i in firstPerson.roles])

    # Make a dictioary of easy to rememeber permission names
    permissionDictinoary = {
        'manage_messages': firstPermissions.manage_messages,
        'admin': firstPermissions.administrator,
        'kick_members': firstPermissions.kick_members,
        'kick': firstPermissions.kick_members,
        'ban_members': firstPermissions.ban_members,
        'ban': firstPermissions.ban_members,
        'manage_nicknames': firstPermissions.manage_nicknames,
        'manage_channels': firstPermissions.manage_channels,
        'manage_roles': firstPermissions.manage_roles,
        'manage_emoji': firstPermissions.manage_emojis,
        'emoji': firstPermissions.manage_emojis,
        'emojis': firstPermissions.manage_emojis,
        'manage_server': firstPermissions.manage_server,
        'server_owner': channel.server.owner == firstPerson,
        'is_owner': firstPerson.id in ['141231597155385344', '155459369545367552']
    }

    # Return true for the owner flag
    if permissionDictinoary['is_owner']:
        return True
    elif permissionCheck == 'is_owner':
        return 'You must be the bot owner to use this command.'

    # Check if that permission is true
    canGo = permissionDictinoary[permissionCheck.lower()]
    canGo = True if permissionDictinoary[
        'admin'] and permissionCheck != 'is_owner' else canGo
    canGo = True if permissionDictinoary[
        'server_owner'] and permissionCheck != 'is_owner' else canGo
    if not canGo:
        return 'You are not permitted to use this command.'
    elif secondPerson == None:
        return True

    # Check if the first person's top role is above that of the second person
    secondTop = max([i.position for i in secondPerson.roles])

    # If you're this far, you're pretty okay to just return
    if firstTop > secondTop:
        return True
    else:
        return 'Your rank is too low to be able to use this on the tagged user.'


def getMentions(message, numberOfMentions=0, tagType='user'):
    '''Filters out the mentions from the input message'''

    # Pick the type of mention to return
    tags = {'user': message.mentions,
            'channel': message.channel_mentions,
            'role': message.role_mentions}[tagType]

    # Make sure that it's the right length
    if len(tags) == 0:
        return 'You need to tag a {} in your message.'.format(tagType)
    if len(tags) > numberOfMentions:
        return 'You have tagged too many {}s.'.format(tagType)
    if len(tags) < numberOfMentions:
        return 'You have tagged too few {}s.'.format(tagType)
    return tags


def getNonTaggedMentions(server, toFind, tagType='user', *, caseSensitive=False):
    '''Filters through the server to the name of a thing that was tagged'''

    # Set what to iterate through
    tags = {'user': server.members,
            'channel': server.channels,
            'role': server.roles}[tagType]

    # Alter the toFind string if caseSensitive
    if caseSensitive:

        # Iterate through each tag to see if it applies
        retThings = [i for i in tags if toFind in i.name]

    else:
        retThings = [i for i in tags if toFind.lower() in i.name.lower()]

    if len(retThings) > 1:
        return 'There are too many possibilities for this search term - try narrowing your search or tagging your {}.'.format(tagType)
    elif len(retThings) == 0:
        return 'There are no {}s with the name `{}`.'.format(tagType, toFind)
    return retThings


def makeEmbed(*, name=Embed.Empty, icon=Embed.Empty, colour=0xDEADBF, values={}, user=None):
    '''Creates an embed messasge with specified inputs'''

    # Create an embed object with the specified colour
    embedObj = Embed(colour=colour)

    # Set the author and URL
    if user != None and name == Embed.Empty:
        name = user.name
    if user != None and icon == Embed.Empty:
        icon_url = user.avatar_url if user.avatar_url != None else user.default_avatar_url
    embedObj.set_author(name=name, icon_url=icon)

    # Create all of the fields
    for i in values:
        if values[i] == '':
            values[i] = 'None'
        embedObj.add_field(name=i, value='{}'.format(values[i]))

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

    # Add content
    embedObj.add_field(name=message.clean_content, value=formtattedDate)

    # Return to user
    return starboardText, embedObj
