def getPermissions(channel, permissionCheck, firstPerson, secondPerson=None):
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
        'is_owner': firstPerson.id in ['141231597155385344']
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


def getMentions(message, numberOfMentions, tagType='user'):
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
