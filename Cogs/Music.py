from discord.ext import commands 
from discord import opus, ClientException
from time import time as currentTime
from datetime import timedelta
from ctypes.util import find_library


class Music:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.voice = {}
        self.allowed = lambda x: self.voice[x]['LastCalled'] > currentTime() - 5

        # Start OPUS if not loaded
        if not opus.is_loaded():
            opus.load_opus(find_library('opus'))

        # Load what VCs it's already in
        for i in self.sparcli.servers:

            # Set up a nice dictionary for storage of information
            self.voice[i] = {
                'VoiceClient': self.sparcli.voice_client_in(i),
                'StreamClient': None,
                'Volume': 0.2,
                'LastCalled': 0
            }

    async def joinVC(self, *, member=None, channel=None):
        '''Joins a given voice channel.
        Will join the VC of a member if a member is passed'''

        # Join a channel if specified
        if channel != None:
            loadedVC = self.sparcli.join_voice_channel(channel)
            return loadedVC

        # No channel specified, join the user's VC
        memberVC = member.voice.voice_channel
        if memberVC == None:
            await self.sparcli.say('You aren\'t currently in a voice channel.')
            return False

        # Join the member's VC
        try:
            # Try to join
            loadedVC = await self.sparcli.join_voice_channel(memberVC)
            return loadedVC

        except ClientException:
            # You're already in it
            loadedVC = self.sparcli.voice_client_in(member.server)
            return loadedVC

        else:
            # You can't join it
            await self.sparcli.say('I am unable to join that voice channel.')
            return False

    async def youtubeBridge(self, server, songName):
        '''Plays a song through a voice client via YTDL'''

        # Make sure it filters through ytdl properly
        if 'http://' in songName.lower() or 'https://' in songName.lower():
            searchTerm = songName
        else:
            searchTerm = 'ytsearch:' + songName

        voiceClient = self.voice[server]['VoiceClient']
        
        # Create the streamclient
        try:
            streamClient = await voiceClient.create_ytdl_player(searchTerm)
        except Exception as e:
           
           # Could not create the stream client
           await self.sparcli.say('I was unable to create the voice client against this search term.')
           await self.sparcli.say(e + str(e))
           return

        # Check the blacklist for the thinamawhatsit
        if not self.handleBlacklist(streamClient):
            await self.sparcli.say('Your search term\'s first result returns a video with a blacklisted title.')
            return

        # Stop the old streamclient
        oldStreamClient = self.voice[server]['StreamClient']
        try:
            oldStreamClient.stop()
        except:
            # It was probably nonetype
            pass

        # Start the new one
        streamClient.volume = self.voice[server]['Volume']
        streamClient.start()
        self.voice[server]['LastCalled'] = currentTime()
        self.voice[server]['StreamClient'] = streamClient

        # Print out to user
        duration = timedelta(seconds=streamClient.duration)
        title = streamClient.title
        await self.sparcli.say('Now playing `{0}` :: `[{1}]`'.format(title, duration))

    def handleBlacklist(self, streamClient):
        '''Sets a blacklist for certain terms - earrape, etc'''

        # Get the song title
        title = streamClient.title

        # Sets up the blacklist
        blacklistedTerms = [
            'ear rape',
            'earrape',
            'rip headphone',
            'ripheadphone',
            'thomas the pain'
        ]

        # Make check if it can filter through
        if title.lower() in blacklistedTerms:
            return False

        # It *should* be fine I think
        return True

    @commands.command(pass_context=True)
    async def play(self, ctx, *, nameOfSong:str):
        '''Gets a song from YouTube and plays it through the bot
        Usage :: play <SongName>
              :: play <YouTube Link>
              :: play <SoundCloud Link>'''

        member = ctx.message.author
        server = member.server

        # Join voice channel
        voiceClient = await self.joinVC(member=member)
        if voiceClient == False: return
        self.voice[server]['VoiceClient'] = voiceClient

        # Go play the stuff
        await self.youtubeBridge(server, nameOfSong)

def setup(bot):
    bot.add_cog(Music(bot))

