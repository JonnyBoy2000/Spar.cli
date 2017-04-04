from discord.ext import commands
from discord import Embed, Member, Emoji, Object
from datetime import datetime
from collections import OrderedDict
from asyncio import sleep
from random import randint
from requests import get
from Cogs.Utils.Discord import makeEmbed
from Cogs.Utils.Misc import colourFixer
from Cogs.Utils.Permissions import botPermission


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
        # em = makeEmbed(user=self.sparcli.user, fields={'Invite me!':'[Click here!]({})'.format(inviteLink)})
        await self.sparcli.say(inviteLink)

    @commands.command()
    async def git(self):
        '''Gives the link to the bot's GitHub page/code
        Usage :: git'''

        await self.sparcli.say('https://github.com/4Kaylum/Spar.cli/')

    @commands.command()
    async def echo(self, *, content: str):
        await self.sparcli.say(content)

    @commands.command(pass_context=True)
    async def echoin(self, ctx, channel:str, *, content: str):
        if channel.isdigit():
            channel = Object(channel)
        elif channel.startswith('<#') and channel.endswith('>'):
            channel = Object(channel[2:-1])
        else:
            channel = [i for i in ctx.message.server.channels if i.name.lower() == channel.lower()][0]
        await self.sparcli.send_message(channel, content)

    @commands.command(pass_context=True)
    async def echoserver(self, ctx, serverName:str, channelName:str, *, content:str):
        server = [i for i in self.sparcli.servers if i.name.lower() == serverName.lower()][0]

        if channelName.isdigit():
            channel = Object(channelName)
        elif channelName.startswith('<#') and channelName.endswith('>'):
            channel = Object(channelName[2:-1])
        else:
            channel = [i for i in server.channels if i.name.lower() == channelName.lower()][0]
        await self.sparcli.send_message(channel, content)

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
        embedMessage = makeEmbed(user=u, fields=userInfo, image=userIcon, colour=topColour)

        # Send it out to the user
        await self.sparcli.say('', embed=embedMessage)

    @commands.command(pass_context=True, aliases=['clear'])
    async def clean(self, ctx, amount: int=50, user: Member=None):
        '''Checks a given amount of messages, and removes ones from a certain user
        Defaults to 50, with the user being the bot
        Usage :: clean
              :: clean <Number>
              :: clean <Number> <UserMention>'''

        # Default to itself
        if user == None:
            user = self.sparcli.user 

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
        await self.sparcli.say('', embed=makeEmbed(colour=intColour, author='#'+fixColour.upper()))

    @commands.command(pass_context=True, aliases=['mycolor'])
    async def mycolour(self, ctx):
        '''Gives you the hex colour that your user is displayed as
        Usage :: mycolour'''

        user = ctx.message.author 
        colour = user.colour.value 

        # Fix the hex to an int
        hexColour = hex(colour)[2:].upper()

        # Actually print it out
        await self.sparcli.say('', embed=makeEmbed(colour=colour, author='#'+hexColour))

    @commands.command(pass_context=True)
    @botPermission(check='attach_files')
    async def meme(self, ctx, topText:str=None, bottomText:str=None, imageLink:str=None):
        '''
        Creates a meme from a top and bottom text with a given image
        '''

        # Create some shorthand
        author = ctx.message.author
        sentMessages = []
        userMessages = []

        # Fill any blank spots
        if None in [topText, bottomText, imageLink]:
            z = await self.sparcli.say('What is the top text for your image?')
            sentMessages.append(z)
            z = await self.sparcli.wait_for_message(author=author)
            topText = z.content
            userMessages.append(z)

            z = await self.sparcli.say('What is the bottom text for your image?')
            sentMessages.append(z)
            z = await self.sparcli.wait_for_message(author=author)
            bottomText = z.content
            userMessages.append(z)

            z = await self.sparcli.say('What is the image URL to add the text to?')
            sentMessages.append(z)
            z = await self.sparcli.wait_for_message(author=author)
            imageLink = z.content
            userMessages.append(z)

        # Delete the user/bot messages that were prompted for
        if sentMessages:
            await self.sparcli.delete_messages(sentMessages)
            if ctx.message.server.me.permissions_in(ctx.message.channel).manage_messages:
                await self.sparcli.delete_messages(userMessages)

        if '' in [topText, bottomText, imageLink]:
            await self.sparcli.say('You can\'t have empty content fields. Aborting command.')
            return

        # Get the meme image from the site
        siteURL = 'https://memegen.link/custom/{}/{}.jpg?alt={}'.format(topText, bottomText, imageLink)
        site = get(siteURL)
        image = site.content
        with open('SPARCLI_RAW_IMAGE_DOWNLOAD.png', 'wb') as a: a.write(image)
        await self.sparcli.send_file(ctx.message.channel, 'SPARCLI_RAW_IMAGE_DOWNLOAD.png', content=author.mention)

    @commands.command(pass_context=True)
    async def permissions(self, ctx, member:Member=None):
        '''
        Checks what permissions a given user has in the mentioned channel
        '''

        # Checks for a tagged member
        if member == None:
            member = ctx.message.author 

        # ✅ TICK
        # ❎ CROSS
        # 💚 ❤

        w = {True:'💚', False:'❤'}

        # Store the channel
        channel = ctx.message.channel
        p = channel.permissions_for(member)
        o = OrderedDict()
        o['Read Messages'] = w[p.read_messages]
        o['Send Messages'] = w[p.send_messages]
        o['TTS'] = w[p.send_tts_messages]
        o['Manage Messages'] = w[p.manage_messages]
        o['Embed Links'] = w[p.embed_links]
        o['Attach Files'] = w[p.attach_files]
        o['Read Message History'] = w[p.read_message_history]
        o['Mention Everyone'] = w[p.mention_everyone]
        o['Mute Members'] = w[p.mute_members]
        o['Deafen Members'] = w[p.deafen_members]
        o['Move Members'] = w[p.move_members]
        o['Change Nickanme'] = w[p.change_nickname]
        o['Manage Nicknames'] = w[p.manage_nicknames]
        o['Manage Roles'] = w[p.manage_roles]
        o['Manage Emoji'] = w[p.manage_emojis]
        o['Manage Channels'] = w[p.manage_channels]
        o['Kick Members'] = w[p.kick_members]
        o['Ban Members'] = w[p.ban_members]
        o['Administrator'] = w[p.administrator]

        e = makeEmbed(fields=o)
        await self.sparcli.say('', embed=e)

    @commands.command(pass_context=True)
    async def vote(self, ctx, *, whatToVoteFor:str):
        '''
        Lets you vote on an item.
        '''

        q = await self.sparcli.say('A vote has been started for subject `{}`.'.format(whatToVoteFor))
        await self.sparcli.add_reaction(q, '👍')
        await self.sparcli.add_reaction(q, '👎')

    @commands.command(pass_context=True)
    async def addreaction(self, ctx, postID:str, emoji:Emoji):
        q = await self.sparcli.get_message(ctx.message.channel, postID)
        await self.sparcli.add_reaction(q, emoji)


def setup(bot):
    bot.add_cog(Misc(bot))
