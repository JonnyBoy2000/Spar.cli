from discord.ext import commands
from discord import Game, Status
from requests import get
from random import choice
from sys import path, exit
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getPermissions


class OwnerOnly:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(pass_context=True, hidden=True, aliases=['playing'])
    async def game(self, ctx, *, game: str=None):
        '''Change what the bot is playing
        Usage :: game <Content>'''

        # Check if the owner is calling the command
        permReturn = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Change the game
        await self.sparcli.change_presence(game=Game(name=game))
        await self.sparcli.say('Game changed to **{}**.'.format(game))

    @commands.command(pass_context=True, hidden=True)
    async def ev(self, ctx, *, content: str):
        # Check if the owner is calling the command
        permReturn = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Eval and print the answer
        await self.sparcli.say(eval(content))

    @commands.command(pass_context=True, hidden=True)
    async def av(self, ctx, *, avatarUrl: str=None):
        '''Changes the bot's avatar to a set URL
        Usage :: av <ImageLink>
              :: av <ImageUpload>'''

        # Check if the owner is calling the command
        permReturn = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Checks for the URL - either passed as argument or embed
        try:
            if avatarUrl == None:
                avatarUrl = ctx.message.attachments[0]['url']
        except IndexError:
            # If you get to this point, there's no image
            await self.sparcli.say('You need to pass an image or url to set the avatar to.')
            return

        # Load up the image
        imageData = get(avatarUrl).content

        # Set profile picture
        await self.sparcli.edit_profile(avatar=imageData)
        await self.sparcli.say("Profile picture successfully changed.")

    @commands.command(pass_context=True, hidden=True)
    async def kill(self, ctx):
        '''Kills the bot. Makes it deaded.
        Usage :: kill'''

        # Check if the owner is calling the command
        permReturn = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # If it is, tell the user the bot it dying
        killMessages = ['I am deded. Rip me.',
                        'Killing.',
                        'And with this, I am ending.',
                        '*Finally*.',
                        '\'Bout time, mate.',
                        'At least it\'s better than how Snape went out.',
                        'Dead or not, I\'m still more loved than BlackBox.',
                        'In my culture, this is called "delayed abortion".']
        toSay = choice(killMessages)
        await self.sparcli.say(toSay)
        await self.sparcli.change_presence(status=Status.invisible, game=None)
        exit()

    @commands.command(pass_context=True, hidden=True)
    async def loadmessage(self, ctx, messageID:str):
        '''Loads a message into the bot chache
        Usage :: loadmessage <MessageID>'''

        # Check if the owner is calling the command
        permReturn = getPermissions(
            ctx.message.channel, 'is_owner', ctx.message.author)
        if type(permReturn) == str:
            await self.sparcli.say(permReturn)
            return

        # Find and add the message
        messageToAdd = await self.sparcli.get_message(ctx.message.channel, messageID)
        self.sparcli.messages.append(messageToAdd)
        await self.sparcli.say('This message has been added to the bot\'s cache.')



def setup(bot):
    bot.add_cog(OwnerOnly(bot))
