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

# Import WolframAlpha
try:
    from wolframalpha import Client
    wolframalphaImported = True
except ImportError:
    wolframalphaImported = False

from sys import path
from Cogs.Utils.Configs import getTokens


class Internet:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.translator = None
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

    @commands.command()
    async def cat(self, ctx):
        '''Gives a random picture of a cat
        Usage :: cat'''

        # Send typing, so you can see it's being processed
        await ctx.channel.trigger_typing()

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
        await ctx.send(returnUrl)

    @commands.command(pass_context=True)
    async def pun(self, ctx):
        '''Gives a random pun from the depths of the internet
        Usage :: pun'''

        # Send typing, so you can see it's being processed
        await ctx.channel.trigger_typing()

        # Read from page
        page = get('http://www.punoftheday.com/cgi-bin/randompun.pl')

        # Scrape the raw HTML
        rawPun = page.text.split('dropshadow1')[1][6:].split('<')[0]

        # Boop it out
        await ctx.send(rawPun)

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
                await ctx.send('Translation has not been set up for this bot.')
                return

        # Send typing, so you can see it's being processed
        await ctx.channel.trigger_typing()

        # Make sure that the language is supported
        if langTo not in self.translator.get_languages():
            await ctx.send("The language provided is not supported.")
            return

        # If so, translate it
        translatedText = self.translator.translate(toChange, langTo.lower())
        await ctx.send(translatedText)

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
                await ctx.send('WolframAlpha has not been set up for this bot.')
                return

        # Send typing, so you can see it's being processed
        await ctx.channel.trigger_typing()

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
        await ctx.send(' '.join(wolfList[0:6]))

    @commands.command()
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
            await ctx.send('Nice try.')
            return

        # Throw the object
        atUser = '.' if member == None else ' at {}.'.format(member.mention)
        await ctx.send('Thrown {} {}{}'.format(aOrAn, toThrow, atUser))


def setup(bot):
    bot.add_cog(Internet(bot))
