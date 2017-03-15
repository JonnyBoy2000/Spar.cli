from discord import Object

from discord.ext import commands 
from random import choice
from time import time
from uuid import uuid4
from json import dumps
try:
    import praw
except ImportError:
    raise Exception('You need to install Praw for this class to work.')
from collections import OrderedDict
from Cogs.Utils.Discord import makeEmbed
from Cogs.Utils.Configs import getTokens, getRedditInstances, saveRedditInstances

'''
reddit = praw.Reddit(client_id='SI8pN3DSbt0zor',
                     client_secret='xaxkj7HNh8kwg8e5t4m6KvSrbTI',
                     refresh_token='WeheY7PwgeCZj4S3QgUcLhKE5S2s4eAYdxM',
                     user_agent='testscript by /u/fakebot3')
'''


def generateUUID(amount:int) -> str:
    '''
    Generates a random UUID
    '''

    return str(uuid4())


def generateRedditObject(discordID:str):
    '''
    Generates a reddit instance for a given Discord ID, otherwise None
    '''

    redditToken = getRedditInstances()['Tokens'][str(discordID)]
    tokens = getTokens()['Reddit']
    q = praw.Reddit(
        client_id=tokens['ID'],
        client_secret=tokens['Secret'],
        user_agent=tokens['User Agent'],
        refresh_token=redditToken
    )
    return q


class Reddit:

    def __init__(self, sparcli):
        self.sparcli = sparcli

        tokens = getTokens()['Reddit']
        self.reddit = praw.Reddit(
            client_id=tokens['ID'],
            client_secret=tokens['Secret'],
            user_agent=tokens['User Agent'],
            redirect_uri=tokens['Redirect URI']
        )

        self.getRedditor = lambda name: self.reddit.redditor(name)
        self.getSubreddit = lambda name: self.reddit.subreddit(name)
        self.discordSays = self.reddit.subreddit('DiscordSays')
        self.redditIcon = 'http://rawapk.com/wp-content/uploads/2016/04/Reddit-The-Official-App-Icon.png'
        self.postHandler = {}

    @commands.command()
    async def reddituser(self, ctx, username:str):
        '''Gives info on a given redditor
        Usage :: reddituser <Username>'''

        # Send typing to show that you're doing stuff
        await ctx.channel.trigger_typing()

        # Get the redditor from using the reddit instance
        redditor = self.getRedditor(username)

        # Store data in a dict
        redditData = OrderedDict()
        redditData['Comment Karma'] = redditor.comment_karma
        redditData['Link Karma'] = redditor.link_karma

        tops = [i for i in redditor.top()]
        topComment = None 
        topLink = None
        for i in tops:
            if type(i) == praw.models.reddit.comment.Comment and topComment == None:
                topComment = i
            if type(i) == praw.models.reddit.submission.Submission and topLink == None:
                topLink = i 
            if topComment != None and topLink != None:
                break

        redditData['Top Comment'] = '[Click here!]({0.link_url}{0.id}/?context=3)'.format(topComment)
        redditData['Top Post'] = '[Click here!](http://reddit.com{0.permalink})'.format(topLink)

        # Make an embed from it
        e = makeEmbed(name=redditor.name, icon=self.redditIcon, colour=0xff4006, values=redditData)

        # Print to user
        await ctx.send('', embed=e)

    @commands.command()
    async def subreddit(self, ctx, name:str):
        '''Gets a random post from a subreddit
        Usage :: subreddit <Subreddit>'''

        # Send typing to show that you're doing stuff
        await ctx.channel.trigger_typing()

        # Get the subreddit from the reddit instance
        subreddit = self.getSubreddit(name)

        # Get a random post
        postGen = subreddit.hot()
        postList = [i for i in postGen]
        post = choice(postList)
        postValues = OrderedDict()

        # Format nicely for the embeds
        title = post.title
        link = post.shortlink
        score = post.score

        # Start formatting the embed
        postValues['Title'] = title 
        postValues['Score'] = score
        postValues['Comments'] = '[Click here!]({})'.format(link)

        # Work out if it's an image or not
        if post.is_self:
            makeThumb = False
            if post.selftext != '':
                postValues['Body Text'] = post.selftext
        elif True in [post.url.endswith(i) for i in['.jpg', '.jpeg', '.png', '.gif']]:
            makeThumb = True
        else:
            makeThumb = True

        # Make the embed
        if makeThumb:
            e = makeEmbed(name=title, icon=self.redditIcon, colour=0xff4006, image=post.url, values=postValues)
        else:
            e = makeEmbed(name=title, icon=self.redditIcon, colour=0xff4006, values=postValues)

        # Return to user
        await ctx.send('', embed=e)

    @commands.group(name='reddit')
    async def redditCommand(self, ctx):
        '''
        Grouping for the reddit handling commands. See `help reddit` for more
        '''

        if ctx.invoked_subcommand is None: 
            await ctx.send('Please refer to this command\'s help for how to use it properly.')

    @redditCommand.command(name='login')
    async def redditLogin(self, ctx):
        '''
        Lets you log into a reddit account so the bot knows who you are
        '''

        # Generate some constants
        author = ctx.message.author
        uuid = generateUUID(100)
        authURL = self.reddit.auth.url(['identity', 'submit', 'vote'], dumps({'DiscordID':author.id, 'UUID':uuid}), 'permanent')

        # Edit and save the reddit instances
        q = getRedditInstances()
        q['UUIDs'][author.id] = uuid
        saveRedditInstances(q)

        # Say to the user
        await author.send(
            'Please click here to authorize your reddit account link :: \n<{}>'.format(authURL)
        )

    @redditCommand.command(name='logout')
    async def redditLogout(self, ctx):
        '''
        Logs you out of a reddit instance
        '''

        # Generate some constants
        author = ctx.message.author
        q = getRedditInstances()

        # Delete the user from the system
        try:
            del q['Tokens'][author.id]
        except KeyError:
            await author.send('You have no authenticated login with Spar.cli.')
            return

        # Save the instances
        saveRedditInstances(q)

        # Say to the user.
        await author.send('Your authentication details have been deleted. \n\
Please manually revoke access to Spar.cli for full recognition that you are diconnected :: \
<https://www.reddit.com/prefs/apps>'
        )

    @commands.group(name='redditpost')
    async def redditSubmit(self, ctx):
        '''
        Handles all reddit posting. See `help reddit post` for details.
        '''

        if ctx.invoked_subcommand is None: 
            await ctx.send('Please refer to this command\'s help for how to use it properly.')

    @redditSubmit.command(name='text')
    async def redditSubmitText(self, ctx):
        '''
        Lets you submit a text post to any given subreddit
        '''

        author = ctx.message.author
        guild = ctx.message.guild
        if not str(author.id) in getRedditInstances()['Tokens']:
            await ctx.send('You do not have a logged in reddit instance - please use `reddit login` to authorize Spar.cli.')
            return

        # Generate some containers so that you can mass-delete the messages later
        botMessages = []
        userMessages = []
        check = lambda m: m.author == author and m.guild == guild

        # Get the messages from the user
        q = await ctx.send('What subreddit would you like to submit to?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        q = await ctx.send('What will the title be?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        q = await ctx.send('What will the body text be?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        # Delete the messages so it doesn't look like spamming
        
        userContent = [i.content for i in userMessages]
        if ctx.message.guild.me.permissions_in(ctx.message.channel).manage_messages:
            await ctx.message.channel.delete_messages(userMessages + botMessages)
        else:
            await ctx.message.channel.delete_messages(botMessages)

        # Make sure that the user didn't leave anything blank
        if '' in [i.content for i in userMessages]:
            await ctx.send('You cannot leave any of the messages blank - aborting.')
            return

        # Generate a local reddit instance
        redditLocal = generateRedditObject(author.id)

        # Actually submit the post to the redditz
        redditLocal.read_only = False
        sub = redditLocal.subreddit(userContent[0])
        try:
            post = sub.submit(userContent[1], selftext=userContent[2])
        except Exception as e:
            await ctx.send('Post submission failed.')
            redditLocal.read_only = True 
            raise(e)
            return
        redditLocal.read_only = True
        mess = await ctx.send('Uploaded :: <{}>'.format(post.shortlink))
        await mess.add_reaction('🔼')
        await mess.add_reaction('🔽')
        self.postHandler[mess] = post

    @redditSubmit.command(name='link')
    async def redditSubmitLink(self, ctx):
        '''
        Lets you submit a text post to any given subreddit
        '''

        author = ctx.message.author
        guild = ctx.message.guild
        if not str(author.id) in getRedditInstances()['Tokens']:
            await ctx.send('You do not have a logged in reddit instance - please use `reddit login` to authorize Spar.cli.')
            return

        # Generate some containers so that you can mass-delete the messages later
        botMessages = []
        userMessages = []
        check = lambda m: m.author == author and m.guild == guild

        # Get the messages from the user
        q = await ctx.send('What subreddit would you like to submit to?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        q = await ctx.send('What will the title be?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        q = await ctx.send('What will the link be?')
        w = await self.sparcli.wait_for('message', check=check)
        botMessages.append(q); userMessages.append(w)

        # Delete the messages so it doesn't look like spamming
        userContent = [i.content for i in userMessages]
        if ctx.message.guild.me.permissions_in(ctx.message.channel).manage_messages:
            await ctx.message.channel.delete_messages(userMessages + botMessages)
        else:
            await ctx.message.channel.delete_messages(botMessages)

        # Make sure that the user didn't leave anything blank
        if '' in [i.content for i in userMessages]:
            await ctx.send('You cannot leave any of the messages blank - aborting.')
            return

        # Generate a local reddit instance
        redditLocal = generateRedditObject(author.id)

        # Actually submit the post to the redditz
        redditLocal.read_only = False
        sub = redditLocal.subreddit(userContent[0])
        try:
            post = sub.submit(userContent[1], url=userContent[2])
        except Exception as e:
            await ctx.send('Post submission failed.')
            redditLocal.read_only = True
            raise(e)
            return
        redditLocal.read_only = True
        mess = await self.sparcli.say('Uploaded :: <{}>'.format(post.shortlink))
        await mess.add_reaction(mess, '🔼')
        await mess.add_reaction(mess, '🔽')
        self.postHandler[mess.id] = post 

    async def on_reaction_add(self, reaction, member):
        '''
        Controls reaction adding as means of upvotes in this class
        '''

        redditPost = None
        for i, o in self.postHandler.items():
            try:
                q = i.id
                w = i 
            except AttributeError:
                q = w = i 
            if reaction.message.id == q:
                redditPost = o
        if redditPost == None:
            return

        if member.id not in getRedditInstances()['Tokens']:
            return

        if reaction.emoji not in ['🔼', '🔽']:
            return

        redditLocal = generateRedditObject(member.id)
        redditLocal.read_only = False
        # redditPost = self.postHandler[reaction.message]
        if reaction.emoji == '🔼':
            q = redditLocal.submission(id=redditPost.id_from_url(redditPost.shortlink))
            q.upvote()

        elif reaction.emoji == '🔽':
            q = redditLocal.submission(id=redditPost.id_from_url(redditPost.shortlink))
            q.downvote()

        redditLocal.read_only = True


def setup(bot):
    bot.add_cog(Reddit(bot))
