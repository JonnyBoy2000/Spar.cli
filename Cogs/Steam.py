from discord.ext import commands 
from requests import get
from collections import OrderedDict
from random import choice
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import makeEmbed

# Used so I can fix Steam game descriptions
def descFixer(description:str):
    fixes = [('<strong>', '**'), ('</strong>', '**'), ('<u>', '__'), ('</u>', '__'), ('<i>', '*'), ('</i>', '*'), ('<br>', '\n')]
    for i in fixes:
        description = description.replace(i[0], i[1])
    return description


class Steam:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.gameInfo = 'http://store.steampowered.com/api/appdetails?appids={}&format=json'
        self.steamIcon = 'https://image.freepik.com/free-icon/steam-logo-games-website_318-40350.jpg'
        self.steamGames = []

        everyGame = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
        gameResp = get(everyGame)
        gameDict = gameResp.json()
        self.steamGames = gameDict['applist']['apps']['app']

    def gameFinder(self, gameName:str):
        '''Returns a game ID as found from its name on the game list'''

        for i in self.steamGames:
            if gameName.lower() in i['name'].lower():
                return str(i['appid'])
        return None

    @commands.command(pass_context=True)
    async def steamsearch(self, ctx, *, gameName:str):
        '''Gets the information of a game from Steam
        Usage :: steamsearch watch_dogs
              :: steamsearch papers, please'''

        await self.sparcli.send_typing(ctx.message.server)

        # Try and get the game from the game list
        gameID = self.gameFinder(gameName)
        if gameID == None:
            await self.sparcli.say('I was unable to find the ID of that game on the Steam API.')
            return

        # Send it to the information formatter
        await self.getSteamGameInfo(gameID)

    @commands.command(pass_context=True)
    async def steamgame(self, ctx, *, gameURL:str):
        '''Gets the information of a game from Steam
        Usage :: steamgame http://store.steampowered.com/app/252870/
              :: steamgame steam://store/252870/
              :: steamgame 252870'''

        await self.sparcli.send_typing(ctx.message.server)

        # Try and get the game ID
        gameID = None 
        gameSplit = gameURL.split('/')
        for i in gameSplit:
            try:
                int(i)
                gameID = i
            except ValueError:
                pass
        if gameID == None:
            await self.sparcli.say('I was unable to find the ID of that game on the Steam API.')
            return

        await self.getSteamGameInfo(gameID)

    async def getSteamGameInfo(self, gameID:str=None):
        '''Gets the data of a game on Steam. Can only be done through ID'''

        # Get the data from Steam
        steamData = get(self.gameInfo.format(gameID)).json()
        if steamData[str(gameID)]['success'] == False:
            await self.sparcli.say('I was unable to find the ID of that game on the Steam API.')
            return

        # Get the embed information
        retData = OrderedDict()
        priceFormatter = lambda x: 'GPB{}.{}'.format(str(x)[:-2], str(x)[-2:]) if len(str(x)) > 2 else 'GPB0.' + str(x)
        gameData = steamData[gameID]['data']
        retData['Name'] = gameData['name']
        desc = gameData['short_description']
        desc = descFixer(desc)
        retData['Description'] = (desc, False)
        retData['Game ID'] = gameID
        retData['Categories'] = ', '.join([i['description'] for i in gameData['categories']])
        retData['Platforms'] = ', '.join([i.title() for i in list(gameData['platforms'].keys())])
        retData['Developer'] = ', '.join(gameData['developers'])
        retData['Publisher'] = ', '.join(gameData['publishers'])
        try:
            priceTemp = gameData['price_overview']
            if priceTemp['initial'] != priceTemp['final']:
                retData['Price'] = '~~{}~~ {}'.format(priceFormatter(priceTemp['initial']), priceFormatter(priceTemp['final']))
            else:
                retData['Price'] = priceFormatter(priceTemp['initial'])
        except KeyError:
            # The game is not released/does not have a price
            pass

        retData['Store Link'] = '[Open in Steam](steam://store/{0}/), [open in your browser](http://store.steampowered.com/app/{0}/)'.format(gameID)

        gameImage = choice(gameData['screenshots'])['path_full']

        # Delete stuff that doesn't exist
        for i, o in retData.items():
            if o == '':
                del retData[i]

        # Make it into an embed
        e = makeEmbed(name=retData['Name'], icon=self.steamIcon, colour=1, values=retData, image=gameImage)

        # Return to user
        await self.sparcli.say('', embed=e)


def setup(bot):
    bot.add_cog(Steam(bot))
