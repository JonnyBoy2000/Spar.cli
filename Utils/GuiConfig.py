from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getMentions


async def addEmojiList(sparcli, message, emojiList):
    '''Adds a list of emoji to a given message'''

    # Split emoji into a list if it is a string
    if type(emojiList) == str:
        emojiList = list(emojiList)

    # Add the reactions
    for i in emojiList:
        await sparcli.add_reaction(message, i)


async def updateFromEmoji(sparcli, ctx, serverSettings, thingToEnable, whatPresentlyIs):
    '''Configures a serverconfig depending on a given emoji'''

    # Shorten a line
    author = ctx.message.author
    thumbs = ['👍', '👎']

    # Print out message to user
    mes = await sparcli.say('Enable {0}? (Presently `{1}`)'.format(thingToEnable, whatPresentlyIs))

    # Add emoji to it
    await addEmojiList(sparcli, mes, thumbs)

    # See what the user gives back
    ret, usr = await sparcli.wait_for_reaction(thumbs, user=author, message=mes)

    # Set it up to save
    serverSettings['Toggles'][thingToEnable] = {'👍': True, '👎': False}[ret.emoji]

    # Delete the message
    await sparcli.delete_message(mes)

    return serverSettings


async def updateFromMessage(sparcli, ctx, serverSettings, thingToSet):
    '''Configures a serverconfig depending on a given message'''

    # Shorten a line
    author = ctx.message.author
    channel = ctx.message.channel

    # Say out to user
    mes = [await sparcli.say('What channel should {0} be set to?'.format(thingToSet))]

    # Wait for response from user
    while True:
        ret = await sparcli.wait_for_message(author=author, channel=channel)

        # Check if there's a tagged channel
        mentioned = getMentions(ret, 1, 'channel')
        if type(mentioned) == str:
            z = await sparcli.say('You need to tag a channel in your message.')
            mes.append(z)
            mes.append(ret)
        else:
            for q in mes:
                await sparcli.delete_message(q)
            await sparcli.delete_message(ret)
            serverSettings['Channels'][thingToSet] = mentioned[0].id
            break

    return serverSettings
