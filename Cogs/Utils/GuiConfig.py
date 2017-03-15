async def addEmojiList(message, emojiList):
    '''Adds a list of emoji to a given message'''

    # Split emoji into a list if it is a string
    if type(emojiList) == str:
        emojiList = list(emojiList)

    # Add the reactions
    for i in emojiList:
        await message.add_reaction(i)


async def updateFromEmoji(sparcli, ctx, serverSettings, thingToEnable, whatPresentlyIs):
    '''Configures a serverconfig depending on a given emoji'''

    # Shorten a line
    author = ctx.message.author
    thumbs = ['👍', '👎']

    # Print out message to user
    mes = await ctx.send('Enable {0}? (Presently `{1}`)'.format(thingToEnable, whatPresentlyIs))

    # Add emoji to it
    await addEmojiList(mes, thumbs)

    # See what the user gives back
    def check(reaction, user):
        c = []
        c.append(reaction.message.id == mes.id)
        c.append(user.id == author.id)
        c.append(reaction.emoji in thumbs)
        return c == [True, True, True]

    ret, usr = await sparcli.wait_for('reaction_add', check=check)

    # Set it up to save
    serverSettings['Toggles'][thingToEnable] = {'👍': True, '👎': False}[ret.emoji]

    # Delete the message
    await mes.delete()

    return serverSettings


async def updateFromMessage(sparcli, ctx, serverSettings, thingToSet):
    '''Configures a serverconfig depending on a given message'''

    # Shorten a line
    author = ctx.message.author
    channel = ctx.message.channel

    def check(mes):
        return mes.author == author and mes.channel == channel

    # Say out to user
    mes = [await ctx.send('What channel should {0} be set to?'.format(thingToSet))]

    # Wait for response from user
    while True:

        ret = await sparcli.wait_for('message', check=check)
        mes.append(ret)

        # Check if there's a tagged channel
        mentioned = ret.channel_mentions
        if mentioned == []:
            z = await ctx.send('You need to tag a channel in your message.')
            mes.append(z)
        else:
            await ctx.channel.delete_messages(mes)
            serverSettings['Channels'][thingToSet] = mentioned[0].id
            break

    return serverSettings
