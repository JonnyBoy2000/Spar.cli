from disco.bot import Bot, Plugin
from holster.emitter import Priority


class EventListener(Plugin):

    # Is to be run when a channel is updated
    @Plugin.listen('ChannelUpdate', priority=Priority.BEFORE)
    def on_channel_create(self, event):
        preChannel = self.state.channels.get(event.channel.id)
        aftChannel = event.channel
        transition = [preChannel, aftChannel]

        # Currently does nothing
