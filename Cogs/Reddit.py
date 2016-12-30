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



class Reddit:

    def __init__(self, sparcli):
        self.sparcli = sparcli

        tokens = getTokens()['Reddit']
        self.reddit = praw.Reddit(client_id=tokens['ID'],
                                  client_secret=tokens['Secret'],
                                  user_agent='Spar.cli Discord bot reddit bridge - /u/SatanistSnowflake')

        self.getRedditor = lambda name: self.reddit.redditor(name)
        self.getSubreddit = lambda name: self.reddit.subreddit(name)

    @commands.command()
    async def reddituser(self, username:str):
        '''Gives info on a given redditor
        Usage :: reddituser <Username>'''

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

        redditData['Top Comment'] = '[Click here!]({0.link_url}{0.id}/&context=3)'.format(topComment)
        redditData['Top Post'] = '[Click here!](http://reddit.com{0.permalink})'.format(topLink)

        # Make an embed from it
        e = makeEmbed(name=redditor.name, colour=0xFFFFFF, values=redditData)

        # Print to user
        await self.sparcli.say('', embed=e)



def setup(bot):
    bot.add_cog(Reddit(bot))
