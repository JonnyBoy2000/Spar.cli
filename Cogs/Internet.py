from discord.ext import commands
from discord import Member
from requests import get
from random import choice

# Import translator
try:
    from microsofttranslator import Translator
    translatorImported = True
except ImportError:
    translatorImported = True

# Import Cleverbot
try:
    from cleverbot import Cleverbot
    cleverbotImported = True
except ImportError:
    cleverbotImported = False

# Import WolframAlpha
try:
    from wolframalpha import Client
    wolframalphaImported = True
except ImportError:
    wolframalphaImported = False

from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Configs import getTokens
from Utils.Discord import getMentions


class Internet:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.translator = None
        self.cb = None
        self.wolfClient = None
        self.nounlist = []

        # Set up the translator, if you can
        if translatorImported != False:
            try:
                tokens = getTokens()
                secret = tokens['Microsoft Translate']['Secret']
                transid = tokens['Microsoft Translate']['ID']
                self.translator = Translator(transid, secret)
            except KeyError:
                pass

        # Set up Cleverbot
        if cleverbotImported == True:
            self.cb = Cleverbot()

        # Set up Wolfram
        if wolframalphaImported == True:
            try:
                tokens = getTokens()
                secret = tokens['WolframAlpha']['Secret']
                self.wolfClient = Client(secret)
            except KeyError:
                pass

        # Set up noun list
        nounstr = str(get('http://www.desiquintans.com/downloads/nounlist/nounlist.txt').content)[2:]
        self.nounlist = nounstr.split('\\n')

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        '''Gives a random picture of a cat
        Usage :: cat'''

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.server)

        # Loop to keep track of rate limiting
        while True:
            # Try to load the page
            try:
                page = get('http://thecatapi.com/api/images/get?format=src')
                break
            except:
                pass

        # Give the url of the loaded page
        returnUrl = page.url
        await self.sparcli.say(returnUrl)

    @commands.command(pass_context=True)
    async def pun(self, ctx):
        '''Gives a random pun from the depths of the internet
        Usage :: pun'''

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.server)

        # Read from page
        page = get('http://www.punoftheday.com/cgi-bin/randompun.pl')

        # Scrape the raw HTML
        rawPun = page.text.split('dropshadow1')[1][6:].split('<')[0]

        # Boop it out
        await self.sparcli.say(rawPun)

    @commands.command(pass_context=True)
    async def trans(self, ctx, langTo: str, *, toChange: str):
        '''Translates from one language into another
        Usage :: trans <LanguageShorthand> <Content>
              :: trans en Wie geht es?'''

        # See if the translator has been logged into
        if self.translator == None:
            try:
                if translatorImported == False:
                    raise KeyError
                tokens = getTokens()
                secret = tokens['Microsoft Translate']['Secret']
                transid = tokens['Microsoft Translate']['ID']
                self.translator = Translator(transid, secret)
            except KeyError:
                await self.sparcli.say('Translation has not been set up for this bot.')
                return

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.server)

        # Make sure that the language is supported
        if langTo not in self.translator.get_languages():
            await self.sparcli.say("The language provided is not supported.")
            return

        # If so, translate it
        translatedText = self.translator.translate(toChange, langTo.lower())
        await self.sparcli.say(translatedText)

    @commands.command(pass_context=True, name='c')
    async def clevertalk(self, ctx, *, message: str):
        '''Sends a query to Cleverbot.
        Usage :: c <Query>'''

        # Return if Cleverbot isn't imported
        if cleverbotImported == False:
            await self.sparcli.say('Cleverbot has not been set up for this bot.')
            return

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.server)

        # Get the response from Cleverbot
        response = self.cb.ask(message)

        # Respond nicely
        await self.sparcli.say(response)

    @commands.command(pass_context=True)
    async def wolfram(self, ctx, *, toDo: str):
        '''Searches WolframAlpha for the given term. Returns text
        Usage :: wolfram <SearchTerm>'''

        # Call the internal search function
        await self.wolframSearch(ctx, toDo, False)

    @commands.command(pass_context=True)
    async def iwolfram(self, ctx, *, toDo: str):
        '''Searches WolframAlpha for the given term. Returns images
        Usage :: iwolfram <SearchTerm>'''

        # Call the internal search function
        await self.wolframSearch(ctx, toDo, True)

    async def wolframSearch(self, ctx, whatToSearch, displayImages):
        '''Sends the actual search term to the Wolfram servers'''

        # See if the Wolfram API has been loaded
        if self.wolfClient == None:
            try:
                if wolframalphaImported == False:
                    raise KeyError
                tokens = getTokens()
                secret = tokens['WolframAlpha']['Secret']
                self.wolfClient = Client(secret)
            except KeyError:
                await self.sparcli.say('WolframAlpha has not been set up for this bot.')
                return

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.server)

        # Sends query to Wolfram
        wolfResults = self.wolfClient.query(whatToSearch)

        # Set up a filter to remove Nonetype values
        removeNone = lambda x: [i for i in x if x != None]

        # Fix the results into a list - text or link
        if displayImages == False:
            u = '```\n{}```'
            wolfList = [u.format(i.text) for i in wolfResults.pods]
            wolfList = removeNone(wolfList)
        else:
            wolfList = [i.img for i in wolfResults.pods]

        # Return to user
        await self.sparcli.say(' '.join(wolfList[0:6]))

    @commands.command(pass_context=True)
    async def throw(self, ctx, *, member: Member=None):
        '''Throws a random thing at a user
        Usage :: throw
              :: throw <@User>'''

        # Get a tagged user, if there is one
        # member will either me membertype or nonetype

        # Get thrown object
        toThrow = choice(self.nounlist)
        aOrAn = 'an' if toThrow[0] in 'aeiou' else 'a'

        # See if the user is the bot
        if member == None:
            pass
        elif member.id == self.sparcli.user.id:
            await self.sparcli.say('Nice try.')
            return

        # Throw the object
        atUser = '.' if member == None else ' at {}.'.format(member.mention)
        await self.sparcli.say('Thrown {} {}{}'.format(aOrAn, toThrow, atUser))




def setup(bot):
    bot.add_cog(Internet(bot))
