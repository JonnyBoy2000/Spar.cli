from disco.bot import Bot, Plugin
from holster.emitter import Priority
from disco.util.config import Config


class EventListener(Plugin):

    # Is to be run when a channel is updated
    @Plugin.listen('ChannelUpdate', priority=Priority.BEFORE)
    def on_channel_update(self, event):
        preChannel = self.state.channels.get(event.channel.id)
        aftChannel = event.channel
        transition = [preChannel, aftChannel]

        # Currently does nothing

    # Event listener - on message
    # Currently sets the command prefix since config isn't documented
    # This is a very very very bad way of doing things
    @Plugin.listen('MessageCreate')
    def on_message(self, event):
        # Sets the command prefix to ';'
        self.bot.config.commands_prefix = ';'
        self.bot.config.commands_require_mention = False
