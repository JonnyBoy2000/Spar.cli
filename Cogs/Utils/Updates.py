from discord import Object, Server, Channel
from .Configs import getServerJson


def serverEnables(serverID, typeOfEnable):
    '''Gets the enabled and disabled things on the server'''

    # Get the server configuration
    serverConfig = getServerJson(serverID)

    # See if the response is enabled
    ifEnabled = serverConfig['Toggles'][typeOfEnable]
    if ifEnabled == '':
        ifEnabled = None

    # See if there's a channel that the bot should send to
    try:
        ifSendTo = serverConfig['Channels'][typeOfEnable]
    except KeyError:
        ifSendTo = None
    if ifSendTo == '':
        ifSendTo = None

    # Get the message said by the server
    try:
        sendMessage = serverConfig['Messages'][typeOfEnable]
    except KeyError:
        sendMessage = None
    if sendMessage == '':
        sendMessage = None

    # Return what the bot should do
    # [ifYouShouldSend=TrueFalseNone, whereToSendTo=SnowflakeNone, sendMessage=StringNone]
    return [ifEnabled, ifSendTo, sendMessage]


async def sendIfEnabled(sparcli, serverOrChannel, typeOfEnable, *, embed=None, overrideMessage=None, overrideEnable=False, overrideChannel=None, edit=None, member=None):
    '''Sends a message if the server wants it to happen'''

    # Set up some stuff
    argType = type(serverOrChannel)
    if argType == Server:
        serverID = serverOrChannel.id
        channel = serverOrChannel
    elif argType == Channel:
        serverID = serverOrChannel.server.id
        channel = serverOrChannel
    else:
        raise Exception("You don't know how to code you knob.")

    # Get the enabled devices on the server
    ifShouldSend = serverEnables(serverID, typeOfEnable)

    # Return if it's disabled
    if ifShouldSend[0] == False and overrideEnable == False:
        return

    # Get where the bot should send to
    toSendTo = channel
    if ifShouldSend[1] == None:
        pass
    else:
        toSendTo = Object(ifShouldSend[1])

    # Reformat a send message, if it has one
    messageToSend = ifShouldSend[2]
    try:
        messageToSend = messageToSend.replace('{mention}', member.mention).replace(
            '{name}', str(member))
    except AttributeError:
        pass

    # Fill in the overrides
    toSendTo = overrideChannel if overrideChannel != None else toSendTo
    messageToSend = overrideMessage if overrideMessage != None else messageToSend

    # Send the specified message
    messageToSend = '' if messageToSend == None else messageToSend
    if edit == None:
        await sparcli.send_message(toSendTo, messageToSend, embed=embed)
    else:
        await sparcli.edit_message(edit, messageToSend, embed=embed)
