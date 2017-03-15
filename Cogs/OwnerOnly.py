from discord.ext import commands
from discord import Game, Status
from requests import get
from random import choice
from sys import exit
from os import execl
from sys import exit, executable, argv
from Cogs.Utils.Permissions import permissionChecker
from Cogs.Utils.Extentions import q as initialExtentions


class OwnerOnly:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command(hidden=True, aliases=['playing'])
    @permissionChecker(check='is_owner')
    async def game(self, ctx, *, game: str=None):
        '''Change what the bot is playing
        Usage :: game <Content>'''

        # Change the game
        await self.sparcli.change_presence(game=Game(name=game))
        await ctx.send('Game changed to **{}**.'.format(game))

    @commands.command(hidden=True)
    @permissionChecker(check='is_owner')
    async def ev(self, ctx, *, content: str):
        '''Evaluates a given Python expression
        Usage :: ev <Python>'''

        # Eval and print the answer
        await ctx.send(eval(content))

    @commands.command(hidden=True)
    @permissionChecker(check='is_owner')
    async def av(self, ctx, *, avatarUrl: str=None):
        '''Changes the bot's avatar to a set URL
        Usage :: av <ImageLink>
              :: av <ImageUpload>'''

        # Checks for the URL - either passed as argument or embed
        try:
            if avatarUrl == None:
                avatarUrl = ctx.message.attachments[0]['url']
        except IndexError:
            # If you get to this point, there's no image
            await ctx.send('You need to pass an image or url to set the avatar to.')
            return

        # Load up the image
        imageData = get(avatarUrl).content

        # Set profile picture
        await self.sparcli.user.edit(avatar=imageData)
        await ctx.send("Profile picture successfully changed.")

    @commands.command(hidden=True)
    @permissionChecker(check='is_owner')
    async def kill(self, ctx):
        '''Kills the bot. Makes it deaded.
        Usage :: kill'''

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
        await ctx.send(toSay)
        await self.sparcli.change_presence(status=Status.invisible, game=None)
        exit()

    @commands.command(hidden=True)
    @permissionChecker(check='is_owner')
    async def rld(self, ctx, extention: str=None, doFully:str=False):
        '''Reload an extention on the bot
        Usage :: rld <Extention>'''

        # Get list of loaded extentions
        if extention == None:
            await ctx.send("Currently loaded extentions :: \n```\n{}```".format("\n".join(self.sparcli.cogs)))
            return

        # Decides whether to be a smartbot
        if doFully:
            extention = 'Cogs.' + extention 

        else:

            # Load a nicer way of sorting out the extentions
            # Plonk the initial extentions into a dictionary
            eF = {i.split('.')[1].lower(): i for i in initialExtentions}
            # Finish finish them off to be actual real extentions
            extention = [eF[i] for i in eF.keys() if extention.lower() in i][0]

        # Unload the extention
        await ctx.send("Reloading extension **{}**...".format(extention))
        try:
            self.sparcli.unload_extension(extention)
        except:
            pass

        # Load the new one
        try:
            self.sparcli.load_extension(extention)
        except ImportError:
            await ctx.send("That extention does not exist.")
            return

        # Boop the user
        await ctx.send("Done!")

    @commands.command(hidden=True)
    @permissionChecker(check='is_owner')
    async def loadmessage(self, ctx, messageID: int):
        '''Loads a message into the bot chache
        Usage :: loadmessage <MessageID>'''

        # Find and add the message
        try:
            messageToAdd = await self.sparcli.user.get_message(messageID)
            self.sparcli.messages.append(messageToAdd)
            await ctx.send('This message has been added to the bot\'s cache.')
        except Exception:
            await ctx.send('I was unable to find that message.')

    @commands.command(hidden=True, aliases=['rs'])
    @permissionChecker(check='is_owner')
    async def restart(self, ctx):
        '''Restarts the bot. Literally everything.
        Usage :: restart'''

        # If it is, tell the user the bot it dying
        await ctx.send('Now restarting.')
        await self.sparcli.change_presence(status=Status.dnd, game=None)
        execl(executable, *([executable] + argv))


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
