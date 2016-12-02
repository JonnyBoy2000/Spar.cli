from discord.ext import commands
from requests import get
try:
    from microsofttranslator import Translator
    translatorImported = True
except ImportError:
    translatorImported = True
try:
    from cleverbot import Cleverbot
    cleverbotImported = True
except ImportError:
    cleverbotImported = False
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Configs import getTokens


class Internet:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.translator = None
        self.cb = Cleverbot()

        # Set up the translator, if you can
        if translatorImported == False:
            return
        try:
            tokens = getTokens()
            secret = tokens['Microsoft Translate']['Secret']
            transid = tokens['Microsoft Translate']['ID']
            self.translator = Translator(transid, secret)
        except KeyError:
            pass

    @commands.command()
    async def pun(self):
        '''Grabs a random pun form around the internet
        Usage :: pun'''

        pass

    @commands.command()
    async def cat(self):
        '''Gives a random picture of a cat
        Usage :: cat'''

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

    @commands.command()
    async def pun(self):
        '''Gives a random pun from the depths of the internet
        Usage :: pun'''

        # Read from page
        page = get('http://www.punoftheday.com/cgi-bin/randompun.pl')

        # Scrape the raw HTML
        rawPun = page.text.split('dropshadow1')[1][6:].split('<')[0]

        # Boop it out
        await self.sparcli.say(rawPun)

    @commands.command()
    async def trans(self, langTo: str, *, toChange: str):
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

        # Make sure that the language is supported
        if langTo not in self.translator.get_languages():
            await self.sparcli.say("The language provided is not supported.")
            return

        # If so, translate it
        translatedText = self.translator.translate(toChange, langTo.lower())
        await self.sparcli.say(translatedText)

    @commands.command(name='c')
    async def clevertalk(self, *, message:str):
        if cleverbotImported == False:
            await self.sparcli.say('Cleverbot has not been set up for this bot.')
            return 

        # Get the response from Cleverbot
        response = self.cb.ask(message)

        # Respond nicely
        await self.sparcli.say(response)


def setup(bot):
    bot.add_cog(Internet(bot))
