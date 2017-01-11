class BotPermissionsTooLow(Exception):
    '''
    This is the exception to be thrown when the bot's permissions are too low
    to perform the given action
    '''
    
    pass


class MemberPermissionsTooLow(Exception):
    '''
    This will be thrown when a given member is trying to perform an action
    on another member but doens't have a high enough top role
    '''

    pass


class MemberMisingPermissions(Exception):
    '''
    This will be thrown when a member is missing permissions to perform an action
    that they are trying to do a command with
    '''

    pass


class BotMissingPermissions(Exception):
    '''
    This will be thrown when the bot is missing permissions for an action
    that a cog has specified
    '''

    pass

