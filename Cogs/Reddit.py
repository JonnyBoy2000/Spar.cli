from discord.ext import commands 
try:
    import praw
except ImportError:
    raise Exception('You need to install Praw for this class to work.')
from collections import OrderedDict
from sys import path
path.append('../')  # Move path so you can get the Utils folder
from Utils.Discord import makeEmbed
from Utils.Configs import getTokens
from random import choice



class Reddit:

    def __init__(self, sparcli):
        self.sparcli = sparcli

        tokens = getTokens()['Reddit']
        self.reddit = praw.Reddit(client_id=tokens['ID'],
                                  client_secret=tokens['Secret'],
                                  user_agent='Spar.cli Discord bot reddit bridge - /u/SatanistSnowflake')

        self.getRedditor = lambda name: self.reddit.redditor(name)
        self.getSubreddit = lambda name: self.reddit.subreddit(name)
        self.redditIcon = 'http://rawapk.com/wp-content/uploads/2016/04/Reddit-The-Official-App-Icon.png'

    @commands.command(pass_context=True)
    async def reddituser(self, ctx, username:str):
        '''Gives info on a given redditor
        Usage :: reddituser <Username>'''

        # Send typing to show that you're doing stuff
        await self.sparcli.send_typing(ctx.message.server)

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
        await self.sparcli.say('', embed=e)

    @commands.command(pass_context=True, aliases=['reddit'])
    async def subreddit(self, ctx, name:str):
        '''Gets a random post from a subreddit
        Usage :: subreddit <Subreddit>'''

        # Send typing to show that you're doing stuff
        await self.sparcli.send_typing(ctx.message.server)

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
        await self.sparcli.say('', embed=e)


def setup(bot):
    bot.add_cog(Reddit(bot))
