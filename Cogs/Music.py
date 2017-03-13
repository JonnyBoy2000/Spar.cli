from discord.ext import commands 
from discord import opus, ClientException
from ctypes.util import find_library
from Cogs.Utils.Discord import makeEmbed
from Cogs.Utils.Permissions import permissionChecker
from Cogs.Utils.VoiceHandler import ServerVoice


class Music:

    def __init__(self, sparcli):
        self.sparcli = sparcli
        self.voice = {}

        # Start OPUS if not loaded
        if not opus.is_loaded():
            opus.load_opus(find_library('opus'))

        # Load what VCs it's already in
        for i in self.sparcli.servers:

            # Set up a nice dictionary for storage of information
            voiceClientInServer = self.sparcli.voice_client_in(i)
            self.voice[i] = ServerVoice(bot=self.sparcli, server=i, voiceClient=voiceClientInServer)


    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, *, nameOfSong:str):
        '''
        Plays a song from a YouTube search or URL.
        '''

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel
        if serverHandler.voiceClient == None:
            z = await serverHandler.joinVC(ctx.message.author)
            if z == False:
                return
        await serverHandler.addToQueue(nameOfSong)
        if serverHandler.looping == False: await serverHandler.loop()

    @commands.command(pass_context=True)
    async def bestsong(self, ctx):
        '''Plays the best song.'''

        nameOfSong = 'https://www.youtube.com/watch?v=miomuSGoPzI'

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel
        if serverHandler.voiceClient == None:
            z = await serverHandler.joinVC(ctx.message.author)
            if z == False:
                return
        await serverHandler.addToQueue(nameOfSong)
        if serverHandler.looping == False: await serverHandler.loop()

    @commands.command(pass_context=True, aliases=['disconnect', 'dc'])
    async def leave(self, ctx):
        '''
        Makes a bot on the server leave the joined voice channel.
        '''

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel
        if serverHandler.voiceClient == None:
            await self.sparcli.say('I\'m not currently in a voice channel.')
        else:
            await serverHandler.disconnect()
            await self.sparcli.say('Disconnected from the VC.')
        if serverHandler.looping == False: await serverHandler.loop()

    @commands.command(pass_context=True, aliases=['v'])
    async def volume(self, ctx, volume:int=20):
        '''
        Changes the volume of the currently playing music stream.
        '''

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel

        z = serverHandler.setVolume(volume)

        await self.sparcli.say('The volume has been set to {}%.'.format(z))
        if serverHandler.looping == False: await serverHandler.loop()

    @commands.command(pass_context=True)
    async def queued(self, ctx):
        '''
        Gets you a list of what is currently queued.
        '''

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel

        queuedTitles = [i.title for i in serverHandler.queue]
        if len(queuedTitles) > 0:
            out = 'Here is a list of the currently queued items: ```\n{}```'.format('\n'.join(queuedTitles))
        else:
            out = 'There is currently nothing queued to be played :c'
        await self.sparcli.say(out)

        if serverHandler.looping == False: await serverHandler.loop()

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def forceskip(self, ctx):
        '''
        Forces the bot to skip to the next song.
        '''

        serverHandler = self.voice[ctx.message.server]
        serverHandler.lastChannel = ctx.message.channel

        if serverHandler.voiceClient == None:
            await self.sparcli.say('I\'m not currently in a voice channel.')
        else:
            await serverHandler.skipChecker(ctx.message, force=True)

        if serverHandler.looping == False: await serverHandler.loop()

    async def on_reaction_add(self, reaction, user):
        '''
        Checks reactions and etc
        '''

        serverHandler = self.voice[reaction.message.server]
        if serverHandler.songInfoMessage == reaction.message.id:
            await serverHandler.skipChecker(reaction.message)

        if serverHandler.looping == False: await serverHandler.loop()


def setup(bot):
    bot.add_cog(Music(bot))

