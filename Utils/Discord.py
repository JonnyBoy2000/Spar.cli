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

    # Check if that permission is true
    canGo = permissionDictinoary[permissionCheck.lower()]
    canGo = True if canGo['admin'] and permissionCheck != 'is_owner' else canGo
    canGo = True if canGo['server_owner'] and permissionCheck != 'is_owner' else canGo
    if not canGo:
        return 'not allowed'
    elif secondPerson == None:
        return True

    # Check if the first person's top role is above that of the second person
    secondTop = max([i.position for i in secondPerson.roles])

    # If you're this far, you're pretty okay to just return
    if firstTop > secondTop:
        return True
    else:
        return 'too low'
