from discord.ext import commands 
from Cogs.Utils.Configs import getServerJson
from Cogs.Utils.Discord import messageToEmbed


class StarboardManagement:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.STAR_EMOJI = '⭐'
        self.starboardCache = {}  # message id: message

    async def starboard(self, reaction):
        '''
        Sends an embedded version of a message to a channel depending on specific enables
        and based on where the configs say to send to.
        '''

        message = reaction.message
        server = message.server 

        # Get the server settings to check if enabled or not
        serverSettings = getServerJson(server.id)

        # Determine whether the event messages are enabled or not
        joinsEnabled = serverSettings['Toggles']['Starboard']
        if joinsEnabled == False:
            return

        # Get the message from the cache if it exists, else None
        createdMessage = self.starboardCache.get(message.id, None)
        if createdMessage == None:
            newPost = True 
        else:
            newPost = False 

        # Make sure that there are enough reactions on the message to keep it
        starReaction = [i for i in message.reactions if i.emoji == self.STAR_EMOJI]
        if len(starReaction) == 0:
            await self.sparcli.delete_message(createdMessage)
            del self.starboardCache[message.id]
            return

        # Generate the string that will be sent with the message
        helpfulString = '**⭐{}** from `{.id}` in {.mention}'.format(starReaction[0].count, message, message.channel)

        # Change the message into an embed
        embeddedMessage = messageToEmbed(message)

        # Get the channel ID
        channelLocation = serverSettings['Channels']['Starboard']
        if channelLocation == '':
            channelLocation = server.id

        # Get the channel object
        channelObject = server.get_channel(channelLocation)
        if channelObject == None:
            return

        # Return to the user
        if newPost:
            said = await self.sparcli.send_message(channelObject, helpfulString, embed=embeddedMessage)
            self.starboardCache[said.id] = said
        else:
            await self.sparcli.edit_message(createdMessage, helpfulString, embed=embeddedMessage)


    async def on_reaction_add(self, reaction, member):

        # See if it applies for the starboard
        if reaction.emoji == self.STAR_EMOJI:
            await self.starboard(reaction)


    async def on_reaction_remove(self, reaction, member):
        # See if it applies for the starboard
        if reaction.emoji == self.STAR_EMOJI:
            await self.starboard(reaction)


def setup(bot):
    bot.add_cog(StarboardManagement(bot))
