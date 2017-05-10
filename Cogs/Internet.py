from aiohttp import get
from re import finditer
from random import choice, randint
from collections import OrderedDict
from datetime import timedelta
from discord import Member
from discord.ext import commands
from Cogs.Utils.Configs import getTokens
from Cogs.Utils.Messages import makeEmbed

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


class Internet:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.urbanSite = 'https://api.urbandictionary.com/v0/define?term={}'
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
        self.nounlist = [] # nounstr.split('\\n')

    @commands.command(pass_context=True, aliases=['🐱'])
    async def cat(self, ctx):
        '''
        Gives a random picture of a cat.
        '''

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.channel)

        while True:
            try:
                # async with get('http://thecatapi.com/api/images/get?format=src') as r:
                #     page = r.url
                # break

                async with get('http://random.cat/meow') as r:
                    data = await r.json()
                page = data['file']
                break
            except Exception:
                pass

        # Give the url of the loaded page
        # await self.sparcli.say(page)
        em = makeEmbed(image=page, colour=randint(0, 0xFFFFFF))
        await self.sparcli.say(embed=em)

    @commands.command(pass_context=True)
    async def pun(self, ctx):
        '''
        Gives a random pun from the depths of the internet.
        '''

        # Send typing, so you can see it's being processed
        await self.sparcli.send_typing(ctx.message.channel)

        # Read from page
        async with get('http://www.punoftheday.com/cgi-bin/randompun.pl') as r:
            page = await r.text()

        # Scrape the raw HTML
        r = r'(<div class=\"dropshadow1\">\n<p>).*(</p>\n</div>)'
        foundPun = [i for i in finditer(r, page)][0].group()

        # Filter out the pun
        r = r'(>).*(<)'
        filteredPun = [i for i in finditer(r, foundPun)][0].group()

        # Boop it out
        fullPun = filteredPun[1:-1]
        await self.sparcli.say(fullPun)

    @commands.command(pass_context=True)
    async def trans(self, ctx, langTo: str, *, toChange: str):
        '''
        Translates from one language into another.
        '''

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
        await self.sparcli.send_typing(ctx.message.channel)

        # Make sure that the language is supported
        if langTo not in self.translator.get_languages():
            await self.sparcli.say("The language provided is not supported.")
            return

        # If so, translate it
        translatedText = self.translator.translate(toChange, langTo.lower())
        await self.sparcli.say(translatedText)

    @commands.command(pass_context=True)
    async def wolfram(self, ctx, *, toDo: str):
        '''
        Searches WolframAlpha for the given term. Returns text.
        '''

        # Call the internal search function
        await self.wolframSearch(ctx, toDo, False)

    @commands.command(pass_context=True)
    async def iwolfram(self, ctx, *, toDo: str):
        '''
        Searches WolframAlpha for the given term. Returns images.
        '''

        # Call the internal search function
        await self.wolframSearch(ctx, toDo, True)

    async def wolframSearch(self, ctx, whatToSearch, displayImages):
        '''
        Sends the actual search term to the Wolfram servers.
        '''

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
        await self.sparcli.send_typing(ctx.message.channel)

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
        '''
        Throws a random thing at a user.
        '''

        # Populate list if necessary
        if not self.nounlist:
            nounSite = 'http://178.62.68.157/raw/nouns.txt'
            async with get(nounSite) as r:
                nounstr = await r.text()
            self.nounlist = nounstr.split('\n')

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

    @commands.command(pass_context=True)
    async def urban(self, ctx, *, searchTerm:str):
        '''
        Allows you to search UrbanDictionary for a specific term.
        '''

        CHARACTER_LIMIT = 250

        # Make the url nice and safe
        searchTerm = searchTerm.replace(' ', '%20')
        async with get(self.urbanSite.format(searchTerm)) as r:
            siteData = await r.json()

        # Get the definitions
        definitionList = siteData['list']
        o = OrderedDict()
        counter = 0
        url = None

        if definitionList == []:
            await self.sparcli.say('No definitions found for the search term `{}`.'.format(searchTerm))
            return

        # Go through and get the definitions
        for definitionObject in definitionList:

            # Iterate the counter and setup some temp variables
            counter += 1
            author = definitionObject['author']
            definition = definitionObject['definition']

            # Cut off the end of too-long definitions
            if len(definition) > CHARACTER_LIMIT:
                deflist = []

                # Split it per word
                for q in definition.split(' '):

                    # Check if it's above the limit
                    if len(' '.join(deflist + [q])) > CHARACTER_LIMIT:
                        break 
                    else:
                        deflist.append(q)

                # Plonk some elipsies on the end
                definition = ' '.join(deflist) + '...'

            # Put it into the dictionary
            o['Definition #{} by {}'.format(counter, author)] = definition
            if counter == 3:
                break 

            # Get a working URL
            if url == None:
                v = definitionObject['permalink']
                url = '/'.join(v.split('/')[:-1])

        # Return to user
        em = makeEmbed(fields=o, author_url=url, author='Click here for UrbanDictionary', inline=False)
        await self.sparcli.say(embed=em)

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, comicNumber:int='Latest'):
        '''
        Gets you an xkcd comic strip
        '''

        await self.sparcli.send_typing(ctx.message.channel)

        # Parse the comic input into a URL
        if comicNumber == 'Latest':
            comicURL = 'http://xkcd.com/info.0.json'
        else:
            comicURL = 'https://xkcd.com/{}/info.0.json'.format(comicNumber)

        async with get(comicURL) as r:
            try:
                data = await r.json()
            except Exception:
                await self.sparcli.say('Comic `{}` does not exist.'.format(comicNumber))
                return

        title = data['safe_title']
        alt = data['alt']
        image = data['img']
        number = data['num']
        url = 'https://xkcd.com/{}'.format(number)
        await self.sparcli.say(embed=makeEmbed(author=title, author_url=url, description=alt, image=image))

    @commands.command(pass_context=True, aliases=['poke', 'pkmn'])
    async def pokemon(self, ctx, *, pokemonName:str):
        '''
        Gives you information on a given Pokemon
        '''

        await self.sparcli.send_typing(ctx.message.channel)
        pokeSite = 'http://pokeapi.co/api/v2/pokemon/{}'.format(pokemonName)
        typeColours = {
            'Normal': 11052922, 
            'Fire': 15630640, 
            'Water': 6525168, 
            'Electric': 16240684, 
            'Grass': 8046412, 
            'Ice': 9886166, 
            'Fighting': 12725800, 
            'Poison': 10698401, 
            'Ground': 14860133, 
            'Flying': 11112435, 
            'Psychic': 16340359, 
            'Bug': 10926362, 
            'Rock': 11968822, 
            'Ghost': 7559063, 
            'Dragon': 7288316, 
            'Dark': 7362374, 
            'Steel': 12040142, 
            'Fairy': 14058925
        }

        async with get(pokeSite) as r:
            data = await r.json()

        if data.get('detail', False):
            await self.sparcli.say('That Pokémon could not be found.')
            return

        # Format the information nicely
        o = OrderedDict()
        pokemonName = data['name'].title()
        o['Pokédex Number'] = data['id']
        o['Types'] = ', '.join([i['type']['name'].title() for i in data['types']])
        colour = typeColours.get(data['types'][0]['type']['name'].title(), 0)
        o['Abilities'] = ', '.join([i['ability']['name'].replace('-', ' ').title() for i in data['abilities']])
        o['Height'] = '{}m'.format(data['height']/10.0)
        o['Weight'] = '{}kg'.format(data['weight']/10.0)
        image = 'https://img.pokemondb.net/artwork/{}.jpg'.format(pokemonName.lower())
        e = makeEmbed(author=pokemonName, colour=colour, fields=o, image=image)
        await self.sparcli.say('', embed=e)

    @commands.command(pass_context=True, aliases=['ow'])
    async def overwatch(self, ctx, *, battleTag:str):
        '''
        Gives you an overview of some Overwatch stats for the PC
        '''
        await self.overwatchStats(ctx, battleTag, 'pc')

    @commands.command(pass_context=True)
    async def overwatchps4(self, ctx, *, battleTag:str):
        '''
        Gives you an overview of some Overwatch stats for PSN
        '''
        await self.overwatchStats(ctx, battleTag, 'psn')

    async def overwatchStats(self, ctx, battleTag, platform):

        await self.sparcli.send_typing(ctx.message.channel)

        # Auguste-2993
        url = 'https://owapi.net/api/v3/u/{}/blob?platform={}'.format(battleTag.replace('#', '-'), platform)
        async with get(url, headers={'User-Agent': 'Discord bot Sparcli by Caleb#2831'}) as r:
            data = await r.json()
        if data.get('msg', False):
            await self.sparcli.say('This user could not be found.')
            return

        adata = data['us'] or data['eu'] or data['kr']
        if adata == None:
            adata = data['any']
        data = adata['stats']['quickplay']

        # Get the relevant data from the retrieved stuff
        o = OrderedDict()
        t = data['overall_stats']  # Temp variable
        o['Overall Stats'] = '{wins} wins vs {losses} losses over {games} games ({winrate}% win rate)'.format(
            wins=t['wins'],
            losses=t['losses'],
            games=t['games'],
            winrate=t['win_rate']
        )
        o['Rank'] = t['tier'].title()
        o['Level'] = '{}'.format((int(t['prestige']) * 100) + int(t['level']))
        o['SR'] = int(t['comprank'])

        t = adata['heroes']['playtime']['quickplay']
        v = []
        b = []
        for y, u in t.items():
            v.append(y)
            b.append(u)
        mostUsed = v[b.index(max(b))]
        maxTime = timedelta(hours=max(b))
        o['Most Used Hero'] = '{} ({})'.format(mostUsed.title(), str(maxTime))

        t = data['game_stats']
        o['Total Eliminations'] = int(t['eliminations'])
        o['Total Deaths'] = int(t['deaths'])

        o['Total Solo Kills'] = int(t['solo_kills'])
        o['Total Final Blows'] = int(t['final_blows'])
        o['Total Damage Done'] = int(t['damage_done'])
        o['Total Healing Done'] = int(t['healing_done'])

        o['Most Solo Kills in Game'] = int(t['solo_kills_most_in_game'])
        o['Most Final Blows in Game'] = int(t['final_blows_most_in_game'])
        o['Most Damage Done in Game'] = int(t['damage_done_most_in_game'])
        o['Most Healing Done in Game'] = int(t['healing_done_most_in_game'])

        o['Best Killstreak in Game'] = int(t['kill_streak_best'])

        # Format into an embed
        e = makeEmbed(author='Quickplay Overwatch Stats for {}'.format(battleTag), fields=o)
        await self.sparcli.say('', embed=e)


def setup(bot):
    bot.add_cog(Internet(bot))
