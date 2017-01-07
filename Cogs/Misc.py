from discord.ext import commands
from discord import Embed, Member
from datetime import datetime
from collections import OrderedDict
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import getMentions, makeEmbed
from Utils.Misc import colourFixer


class Misc:

    def __init__(self, bot):
        self.sparcli = bot

    @commands.command()
    async def invite(self):
        '''Gives the bot's invite link
        Usage :: invite'''

        # https://discordapi.com/permissions.html
        clientID = '252880131540910080'
        permissionsID = '469888119'
        baseLink = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'
        inviteLink = baseLink.format(clientID, permissionsID)
        em = makeEmbed(user=self.sparcli.user, values={'Invite me!':'[Click here!]({})'.format(inviteLink)})
        await self.sparcli.say(inviteLink, embed=em)

    @commands.command()
    async def git(self):
        '''Gives the link to the bot's GitHub page/code
        Usage :: git'''

        await self.sparcli.say('https://github.com/4Kaylum/Spar.cli/')

    @commands.command()
    async def echo(self, *, content: str):
        '''Makes the bot print back what the user said
        Usage :: echo <Content>'''

        await self.sparcli.say(content)

    @commands.command(pass_context=True)
    async def info(self, ctx, user:Member=None):
        '''Gives info on the mentioned user
        Usage :: info <UserPing>
              :: info'''

        # Get the user who was pinged
        u = user if user != None else ctx.message.author

        # Generate a dictionary of their information
        userInfo = OrderedDict()
        userIcon = u.avatar_url if u.avatar_url != None else u.default_avatar_url
        userInfo['Username'] = u.name 
        userInfo['Discriminator'] = u.discriminator 
        userInfo['Icon'] = '[Click here!]({})'.format(userIcon)
        userInfo['Nickname'] = '{}'.format(u.display_name)
        userInfo['ID'] = u.id
        userInfo['Bot'] = u.bot 
        userInfo['Join Date'] = str(u.joined_at)[:-10] + ' (' + str(datetime.now() - u.joined_at).split(',')[0] + ' ago)'
        userInfo['Creation Date'] = str(u.created_at)[:-10] + ' (' + str(datetime.now() - u.created_at).split(',')[0] + ' ago)'
        userInfo['Roles'] = ', '.join([g.name for g in u.roles][1:])

        # Fix a possibly blank thing
        userInfo['Roles'] = 'None' if userInfo['Roles'] == '' else userInfo['Roles']

        # Get top role colour
        topColour = u.colour.value

        # Create an embed out of it
        embedMessage = makeEmbed(user=u, values=userInfo, image=userIcon, colour=topColour)

        # Send it out to the user
        await self.sparcli.say('', embed=embedMessage)

    @commands.command(pass_context=True, aliases=['clear'])
    async def clean(self, ctx, amount: int=50, user: str=None):
        '''Checks a given amount of messages, and removes ones from a certain user
        Defaults to 50, with the user being the bot
        Usage :: clean
              :: clean <Number>
              :: clean <Number> <UserMention>'''

        # Check if the user has mentioned anyone
        messagePings = getMentions(ctx.message, 1)
        if type(messagePings) == str:
            user = self.sparcli.user
        else:
            user = messagePings[0]

        # Set up the check
        cleanCheck = lambda m: m.author.id == user.id

        # Purge accurately
        deleted = await self.sparcli.purge_from(ctx.message.channel, limit=amount, check=cleanCheck)
        await self.sparcli.say('Cleaned `{}` messages from the channel.'.format(len(deleted)))

    @commands.command(aliases=['color'])
    async def colour(self, colour:str):
        '''Gives the colour of a hex code in an embed
        Usage :: colour <Hex>
              :: color <Hex>'''

        # Fix up the hex code, if necessary
        fixColour = colourFixer(colour)

        # Fix the hex to an int
        intColour = int(fixColour, 16)

        # Actually print it out
        await self.sparcli.say('', embed=makeEmbed(colour=intColour, name='#'+fixColour.upper()))

    @commands.command(pass_context=True, aliases=['mycolor'])
    async def mycolour(self, ctx):
        '''Gives you the hex colour that your user is displayed as
        Usage :: mycolour'''

        user = ctx.message.author 
        colour = user.colour.value 

        # Fix the hex to an int
        hexColour = hex(colour)[2:].upper()

        # Actually print it out
        await self.sparcli.say('', embed=makeEmbed(colour=colour, name='#'+hexColour))


def setup(bot):
    bot.add_cog(Misc(bot))
